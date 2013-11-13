# -*- coding: utf-8 -*-
from django.db import models
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from datetime import datetime
from vkontakte_api.utils import api_call, VkontakteError
from vkontakte_api import fields
from vkontakte_api.models import VkontakteManager, VkontakteIDModel
from vkontakte_places.models import City, Country
from dateutil import parser
from datetime import timedelta, datetime
import logging

log = logging.getLogger('vkontakte_users')

VKONTAKTE_USERS_INFO_TIMEOUT_DAYS = getattr(settings, 'VKONTAKTE_USERS_INFO_TIMEOUT_DAYS', 0)

USER_FIELDS = 'uid,first_name,last_name,nickname,screen_name,sex,bdate,city,country,timezone,photo,photo_medium,photo_big,has_mobile,rate,contacts,education,activity,relation,wall_comments,relatives,interests,movies,tv,books,games,about,connections,universities,schools'
USER_SEX_CHOICES = ((1, u'жен.'),(2, u'муж.'))
USER_RELATION_CHOICES = (
    (1, u'Не женат / замужем'),
    (2, u'Есть друг / подруга'),
    (3, u'Помолвлен / помолвлена'),
    (4, u'Женат / замужем'),
    (5, u'Всё сложно'),
    (6, u'В активном поиске'),
    (7, u'Влюблён / влюблена'),
)

USER_PHOTO_DEACTIVATED_URL = 'http://vk.com/images/deactivated_'
USER_NO_PHOTO_URL = 'http://vkontakte.ru/images/camera_'

class ParseUsersMixin(object):
    '''
    Manager mixin for parsing response with extra cache 'profiles'. Used in vkontakte_wall,vkontakte_board applications
    '''
    def parse_response_users(self, response_list):
        users = User.remote.parse_response_list(response_list.get('profiles', []), {'fetched': datetime.now()})
        instances = []
        for instance in users:
            instances += [User.remote.get_or_create_from_instance(instance)]
        return instances

class UsersManager(models.Manager):

    def deactivated(self):
        return self.filter(photo_big__startswith=USER_PHOTO_DEACTIVATED_URL)

    def active(self):
        return self.exclude(photo_big__startswith=USER_PHOTO_DEACTIVATED_URL)

    def has_avatars(self):
        return self.filter(photo_big__contains='userapi.com')

    def no_avatars(self):
        return self.filter(photo_big__startswith=USER_NO_PHOTO_URL)

class UsersRemoteManager(VkontakteManager):

    def fetch(self, **kwargs):
        # TODO: remove here restriction to fetch no more then 1000 users per time
        if 'only_expired' in kwargs and kwargs.pop('only_expired'):
            ids = kwargs['ids']
            expired_at = datetime.now() - timedelta(VKONTAKTE_USERS_INFO_TIMEOUT_DAYS)
            ids_actual = list(self.model.objects.filter(fetched__gte=expired_at, remote_id__in=ids).values_list('remote_id', flat=True))
            kwargs['ids'] = set(ids).difference(set(ids_actual))
            if len(kwargs['ids']):
                super(UsersRemoteManager, self).fetch(**kwargs)
            return self.model.objects.filter(remote_id__in=ids)
        else:
            return super(UsersRemoteManager, self).fetch(**kwargs)

    def api_call(self, method='get', **kwargs):
        '''
        Override parent behaviour without namespace property
        TODO: move all kwargs manipulations to fetch method
        '''
        if 'fields' not in kwargs:
            kwargs['fields'] = USER_FIELDS
        if 'ids' in kwargs:
            kwargs['uids'] = ','.join(map(lambda i: str(i), kwargs.pop('ids')))

        return super(UsersRemoteManager, self).api_call(method, **kwargs)

    def get_by_slug(self, slug):
        '''
        Return active user by slug
        '''
        try:
            return super(UsersRemoteManager, self).get_by_slug(slug)
        except self.model.MultipleObjectsReturned:
            # fetch again all users with this slug and return only active one
            self.model.remote.fetch(ids=[u.remote_id for u in self.model.objects.filter(screen_name=slug)])
            return self.model.objects.active().get(screen_name=slug)

    def parse_response_list(self, response_list, extra_fields=None):
        if extra_fields and 'only_ids' in extra_fields:
            return self.model.objects.filter(remote_id__in=response_list)
        else:
            return super(UsersRemoteManager, self).parse_response_list(response_list, extra_fields)

#    def get_or_create_from_instance(self, instance):
#        #DatabaseError: invalid byte sequence for encoding "UTF8": 0xeda0bc
#        #HINT:  This error can also happen if the byte sequence does not match the encoding expected by the server, which is controlled by "client_encoding".
#        # u.activity = u'\u041d\u0430\u0448 \u043e\u0431\u0443\u0447\u0430\u044e\u0449\u0438\u0439 \u043a\u0443\u0440\u0441 &quot;\u041a\u0430\u043a \u0438\u0437\u0431\u0430\u0432\u0438\u0442\u044c\u0441\u044f \u043e\u0442 \u0438\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u0437\u0430\u0432\u0438\u0441\u0438\u043c\u043e\u0441\u0442\u0438&quot; - \u0442\u0435\u043f\u0435\u0440\u044c \u0438 \u0432 \u043e\u043d\u043b\u0430\u0439\u043d \u0432\u0430\u0440\u0438\u0430\u043d\u0442\u0435\ud83c\u2708\ud83d\U0001f4a8'
#        if instance.remote_id != 59930666:
#            try:
#                super(UsersRemoteManager, self).get_or_create_from_instance(instance)
#            except DatabaseError, e:
#                log.error("Error while creating user with fields %s. Error: %s" % (instance.__dict__, e))
#
#        return instance

#    def get(self, *args, **kwargs):
#        '''
#        Apply country param request to all instances in reponse
#        '''
#        country = None
#
#        if 'country' in kwargs and self.model._meta.get_field('country'):
#            if isinstance(kwargs['country'], Country):
#                country = kwargs['country']
#            else:
#                country = Country.objects.get(remote_id=kwargs['country'])
#
#        instances = super(VkontaktePlacesManager, self).get(*args, **kwargs)
#
#        if country:
#            for instance in instances:
#                instance.country = country
#
#        return instances

class UserRelative(models.Model):

    TYPE_CHOICES = (
        ('grandchild', u'внук/внучка'),
        ('grandparent',u'дедушка/бабушка'),
        ('child', u'сын/дочка'),
        ('sibling',u'брат/сестра'),
        ('parent',u'мама/папа'),
    )

    user1 = models.ForeignKey('User', related_name='user_relatives1')
    user2 = models.ForeignKey('User', related_name='user_relatives2')
    type = models.CharField(u'Тип родственной связи', max_length=20, choices=TYPE_CHOICES)

class User(VkontakteIDModel):
    '''
    TODO: implement relatives, schools and universities connections
    '''
    class Meta:
        verbose_name = u'Пользователь Вконтакте'
        verbose_name_plural = u'Пользователи Вконтакте'
        ordering = ['remote_id']

    remote_pk_field = 'uid'

    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    screen_name = models.CharField(max_length=100, db_index=True)

    sex = models.IntegerField(null=True, choices=USER_SEX_CHOICES)
    bdate = models.CharField(max_length=100)
    timezone = models.IntegerField(null=True)
    city = models.ForeignKey(City, null=True, on_delete=models.SET_NULL)
    country = models.ForeignKey(Country, null=True, on_delete=models.SET_NULL)
    rate = models.PositiveIntegerField(null=True)

    activity = models.TextField()
    relation = models.SmallIntegerField(null=True, choices=USER_RELATION_CHOICES)
    wall_comments = models.BooleanField()

    graduation = models.PositiveIntegerField(u'Дата окончания вуза', null=True)
    university = models.PositiveIntegerField(null=True)
    university_name = models.CharField(max_length=500)
    faculty = models.PositiveIntegerField(null=True)
    faculty_name = models.CharField(max_length=500)

    has_mobile = models.BooleanField()
    home_phone = models.CharField(max_length=50)
    mobile_phone = models.CharField(max_length=50)

    photo_fields = 'photo,photo_big,photo_medium,photo_medium_rec,photo_rec'
    photo = models.URLField()
    photo_big = models.URLField()
    photo_medium = models.URLField()
    photo_medium_rec = models.URLField()
    photo_rec = models.URLField()

    # social networks
    twitter = models.CharField(max_length=500)
    facebook = models.CharField(max_length=500)
    facebook_name = models.CharField(max_length=500)
    skype = models.CharField(max_length=500)
    livejournal = models.CharField(max_length=500)

    # profile info
    interests = models.TextField()
    movies = models.TextField()
    tv = models.TextField()
    books = models.TextField()
    games = models.TextField()
    about = models.TextField()

    friends_users = models.ManyToManyField('User', related_name='followers_users')
    friends_count = models.PositiveIntegerField(u'Друзей', default=0)

#    relatives = models.ManyToManyField('User', through=UserRelative)

    # counters
    counters = ['albums','audios','followers','friends','mutual_friends','notes','subscriptions','user_photos','user_videos','videos']
    sum_counters = models.PositiveIntegerField(default=0, help_text=u'Сумма всех счетчиков')
    counters_updated = models.DateTimeField(null=True, help_text=u'Счетчики были обновлены')

    albums = models.PositiveIntegerField(u'Фотоальбомов', default=0)
    videos = models.PositiveIntegerField(u'Видеозаписей', default=0)
    audios = models.PositiveIntegerField(u'Аудиозаписей', default=0)
    followers = models.PositiveIntegerField(u'Подписчиков', default=0)
    friends = models.PositiveIntegerField(u'Друзей', default=0)
    mutual_friends = models.PositiveIntegerField(u'Общих друзей', default=0)
    notes = models.PositiveIntegerField(u'Заметок', default=0)
    subscriptions = models.PositiveIntegerField(u'Подписок (только пользователи)', default=0)
    user_photos = models.PositiveIntegerField(u'Фотографий с пользователем', default=0)
    user_videos = models.PositiveIntegerField(u'Видеозаписей с пользователем', default=0)

    objects = UsersManager()
    remote = UsersRemoteManager(remote_pk=('remote_id',), methods={
        'get': 'users.get',
        'friends': 'friends.get',
    })

    slug_prefix = 'id'

    @property
    def age(self):
        try:
            return int((datetime.today() - parser.parse(self.bdate)).days / 365.25)
        except:
            pass

    def save(self, *args, **kwargs):
        # check strings for good encoding
        # there is problems to save users with bad encoded activity strings like ID=88798245, ID=143523733
        for field in ['activity','games','movies','tv','books','about','interests','mobile_phone','home_phone','faculty_name','university_name']:
            try:
                getattr(self, field).encode('utf-16').decode('utf-16')
            except UnicodeDecodeError:
                setattr(self, field, '')

        if self.relation and self.relation not in dict(USER_RELATION_CHOICES).keys():
            self.relation = None

        try:
            return super(User, self).save(*args, **kwargs)
        except Exception, e:
            log.error("Error while saving user ID=%s with fields %s" % (self.remote_id, self.__dict__))
            raise e

    def _substitute(self, old_instance):
        '''
        Save counters fields while updating user
        '''
        for counter in self.counters:
            setattr(self, counter, getattr(old_instance, counter))

        self.sum_counters = old_instance.sum_counters
        self.counters_updated = old_instance.counters_updated
        self.friends_count = old_instance.friends_count
        super(User, self)._substitute(old_instance)

    def parse(self, response):

        if response.get('city'):
            self.city = City.objects.get_or_create(remote_id=response.pop('city'))[0]
        if response.get('country'):
            self.country = Country.objects.get_or_create(remote_id=response.pop('country'))[0]
        if response.get('relatives'):
            relatives = response.pop('relatives')
            # doesn't work becouse of self.id will be set lately
            if self.id:
                for relative in relatives:
                    try:
                        user_relative = UserRelative(type=relative.type, user1=self, user2=User.objects.get(remote_id=relative.uid))
                        user_relative.save()
                        self.relative.add(user_relative)
                    except User.DoesNotExist:
                        continue

        super(User, self).parse(response)

#        if 'uid' in response:
#            self.remote_id = response['uid']

        if self.graduation == 0:
            self.graduation = None

    def update_counters(self):
        '''
        Update counters for user with special query and calculate sum of them
        '''
        try:
            response = api_call('users.get', uids=self.remote_id, fields='counters')
        except VkontakteError, e:
            log.warning("There is vkontakte error [code=%d] while updating user [id=%d] counters: %s" % (e.code, self.remote_id, e.description))
            return False

        if 'counters' not in response[0]:
            log.info("There is no counters field in response %s" % response)
        else:
            for counter in self.counters:
                if counter in response[0]['counters']:
                    setattr(self, counter, response[0]['counters'][counter])

            self.sum_counters = sum([getattr(self, counter) for counter in self.counters])
        self.counters_updated = datetime.now()
        self.save()

    def __unicode__(self):
        return self.first_name + ' ' + self.last_name

    def set_name(self, name):
        name_parts = name.split()
        self.first_name = name_parts[0]
        if len(name_parts) > 1:
            self.last_name = ' '.join(name_parts[1:])

    def fetch_posts(self, *args, **kwargs):
        if 'vkontakte_wall' not in settings.INSTALLED_APPS:
            raise ImproperlyConfigured("Application 'vkontakte_wall' not in INSTALLED_APPS")

        from vkontakte_wall.models import Post
        return Post.remote.fetch_wall(owner=self, *args, **kwargs)

    def fetch_friends(self, only_existing_users=False, **kwargs):
        log.debug("Start updating friends of user %s" % self)
        if self.is_deactivated:
            return False

        # send extra_fields with only_ids key for special mode of parsing response, used only in vkontakte_users.models
        kwargs = {'fields': '', 'extra_fields': {'only_ids': True}} if only_existing_users else {'fields': 'uid,first_name,last_name,nickname,screen_name,sex,bdate,city,country,timezone,photo'}
        try:
            users = User.remote.fetch(method='friends', uid=self.remote_id, **kwargs)
            log.debug("Found %d friends of user %s" % (len(users), self))
        except VkontakteError, e:
            if e.code == 15:
                # update current user, make him deactivated
                User.remote.fetch(uid=self.remote_id)
                return False
            else:
                raise e

        self.friends_users.clear()
        log.debug("Cleared friends of user %s" % (self))

        for user in users:
            self.friends_users.add(user)
        log.debug("New friends to user %s attached" % (self))

        self.friends_count = self.friends_users.count()
        self.save()
        log.debug("Friends count %s of user %s updated" % (self.friends_count, self))

        return self.friends_users.all()

    @property
    def is_deactivated(self):
        for field_name in self.photo_fields.split(','):
            if USER_PHOTO_DEACTIVATED_URL in getattr(self, field_name):
                return True
        return False

    @property
    def has_avatar(self):
        for field_name in self.photo_fields.split(','):
            if USER_NO_PHOTO_URL in getattr(self, field_name):
                return False
        return True

    def get_sex(self):
        return dict(USER_SEX_CHOICES).get(self.sex)

#    TODO: Solve naming, dublicate with boolean wall_comments
#    @property
#    def wall_comments(self):
#        if 'vkontakte_wall' not in settings.INSTALLED_APPS:
#            raise ImproperlyConfigured("Application 'vkontakte_wall' not in INSTALLED_APPS")
#        from vkontakte_wall.models import Comment
#        return Comment.objects.filter(remote_id__startswith='%s_' % self.remote_id)