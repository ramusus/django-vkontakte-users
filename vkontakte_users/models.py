# -*- coding: utf-8 -*-
from datetime import timedelta, date
import logging

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.utils import timezone, six
from django.utils.encoding import python_2_unicode_compatible
from vkontakte_api.api import api_call, VkontakteError
from vkontakte_api.decorators import fetch_all, atomic
from vkontakte_api.models import VkontakteManager, VkontaktePKModel
from vkontakte_api.fields import JSONField
from vkontakte_places.models import City, Country

log = logging.getLogger('vkontakte_users')

USERS_INFO_TIMEOUT_DAYS = getattr(settings, 'VKONTAKTE_USERS_INFO_TIMEOUT_DAYS', 14)

USER_FIELDS = 'id,first_name,last_name,nickname,screen_name,sex,bdate,city,country,timezone,photo,photo_medium,' \
              'photo_big,has_mobile,rate,contacts,education,activity,relation,wall_comments,relatives,interests,' \
              'movies,tv,books,games,about,connections,universities,schools'
USER_SEX_CHOICES = ((0, u'не ук.'), (1, u'жен.'), (2, u'муж.'))
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


def list_chunks_iterator(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i + n]


class ParseUsersMixin(object):
    """
    Manager mixin for parsing response with extra cache 'profiles'. Used in vkontakte_wall,vkontakte_board applications
    """
    def parse_response_users(self, response, items_field='profiles'):
        # TODO: refactor to parsing only
        users = User.remote.parse_response_list(response.get(items_field, []), {'fetched': timezone.now()})

        instances = []
        for instance in users:
            instances += [User.remote.get_or_create_from_instance(instance)]
        return instances


class UsersManager(models.Manager):

    def deactivated(self):
        return self.filter(is_deactivated=True)

    def active(self):
        return self.filter(is_deactivated=False)

    def with_avatar(self):
        return self.filter(has_avatar=True)

    def without_avatar(self):
        return self.filter(has_avatar=False)


class UsersRemoteManager(VkontakteManager, ParseUsersMixin):

    fetch_users_limit = 1000

    @atomic
    def fetch_friends(self, user, only_existing_users=False, **kwargs):

        # send extra_fields with only_ids key for special mode of parsing response, used only in vkontakte_users.models
        if only_existing_users:
            kwargs = {'fields': '', 'extra_fields': {'only_ids': True}}

        if 'fields' not in kwargs:
            kwargs['fields'] = 'id,first_name,last_name,nickname,screen_name,sex,bdate,city,country,timezone,photo'

        return self.fetch(method='friends', user_id=user.remote_id, **kwargs)

    @atomic
    def fetch(self, **kwargs):
        """
        Additional attributes:
         * only_expired - flag to fetch only users, fetched earlie than VKONTAKTE_USERS_INFO_TIMEOUT_DAYS days ago
        """
        if 'only_expired' in kwargs and kwargs.pop('only_expired'):
            ids = kwargs['ids']
            expired_at = timezone.now() - timedelta(USERS_INFO_TIMEOUT_DAYS)
            ids_non_expired = self.model.objects.filter(
                fetched__gte=expired_at, remote_id__in=ids).values_list('remote_id', flat=True)

            kwargs['ids'] = list(set(ids).difference(set(ids_non_expired)))
            users = None
            if len(kwargs['ids']):
                users = self._fetch(**kwargs)
            return self._renew_queryset(users, ids)
        else:
            return self._fetch(**kwargs)

    def _fetch(self, **kwargs):
        """
        Method gives ability to fetch more than 1000 users at once
        """
        ids = kwargs.pop('ids', None)
        if ids:
            kwargs_sliced = dict(kwargs)
            users = []
            for chunk in list_chunks_iterator(ids, self.fetch_users_limit):
                kwargs_sliced['ids'] = chunk
                users = super(UsersRemoteManager, self).fetch(**kwargs_sliced)

            return self._renew_queryset(users, ids)
        else:
            return super(UsersRemoteManager, self).fetch(**kwargs)

    def _renew_queryset(self, users, ids):
        """
        Return argument `users` if ammount of `users` is equal to ammount `ids` we need to fetch
        """
        if users is not None and len(ids) == users.count():
            return users
        else:
            return self.model.objects.filter(remote_id__in=ids)

    def api_call(self, method='get', **kwargs):
        """
        Override parent behaviour without namespace property
        TODO: move all kwargs manipulations to fetch method
        :param method:
        """
        if 'fields' not in kwargs:
            kwargs['fields'] = USER_FIELDS
        if 'ids' in kwargs:
            kwargs['user_ids'] = ','.join(map(str, kwargs.pop('ids')))

        return super(UsersRemoteManager, self).api_call(method, **kwargs)

    def get_by_slug(self, slug):
        """
        Return active user by slug
        :param slug:
        """
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

    @fetch_all(default_count=1000)
    def fetch_likes_user_ids(self, likes_type, owner_id, item_id, offset=0, count=1000, filter='likes', **kwargs):
        if count > 1000:
            raise ValueError("Parameter 'count' can not be more than 1000")
        if filter not in ['likes', 'copies']:
            raise ValueError("Parameter 'filter' should be equal to 'likes' or 'copies'")
        if likes_type is None:
            raise ImproperlyConfigured("'likes_type' attribute should be specified")

        # type
        # тип Like-объекта. Подробнее о типах объектов можно узнать на странице Список типов Like-объектов.
        kwargs['type'] = likes_type
        # owner_id
        # идентификатор владельца Like-объекта (id пользователя или id приложения). Если параметр type равен sitepage,
        # то в качестве owner_id необходимо передавать id приложения. Если параметр не задан, то считается, что он
        # равен либо идентификатору текущего пользователя, либо идентификатору текущего приложения (если type равен
        # sitepage).
        kwargs['owner_id'] = owner_id
        # item_id
        # идентификатор Like-объекта. Если type равен sitepage, то параметр item_id может содержать значение параметра
        # page_id, используемый при инициализации виджета «Мне нравится».
        kwargs['item_id'] = item_id
        # page_url
        # url страницы, на которой установлен виджет «Мне нравится». Используется вместо параметра item_id.

        # filter
        # указывает, следует ли вернуть всех пользователей, добавивших объект в список "Мне нравится" или только тех,
        # которые рассказали о нем друзьям. Параметр может принимать следующие значения:
        # likes – возвращать всех пользователей
        # copies – возвращать только пользователей, рассказавших об объекте друзьям
        # По умолчанию возвращаются все пользователи.
        kwargs['filter'] = filter
        # friends_only
        # указывает, необходимо ли возвращать только пользователей, которые являются друзьями текущего пользователя.
        # Параметр может принимать следующие значения:
        # 0 – возвращать всех пользователей в порядке убывания времени добавления объекта
        # 1 – возвращать только друзей текущего пользователя в порядке убывания времени добавления объекта
        # Если метод был вызван без авторизации или параметр не был задан, то считается, что он равен 0.
        kwargs['friends_only'] = 0
        # offset
        # смещение, относительно начала списка, для выборки определенного подмножества. Если параметр не задан, то
        # считается, что он равен 0.
        kwargs['offset'] = int(offset)
        # count
        # количество возвращаемых идентификаторов пользователей.
        # Если параметр не задан, то считается, что он равен 100, если не задан параметр friends_only, в противном
        # случае 10. Максимальное значение параметра 1000, если не задан параметр friends_only, в противном случае 100.
        kwargs['count'] = int(count)

        log.debug('Fetching like users ids of %s %s_%s, offset %d' % (likes_type, owner_id, item_id, offset))

        response = api_call('likes.getList', **kwargs)
        return response['users']

    @atomic
    def fetch_instance_likes(self, instance, *args, **kwargs):
        """
        DEPRECATED. will be removed in next release, after updating vkontakte_photos app
        """
        m2m_field_name = kwargs.pop('m2m_field_name', 'like_users')
        m2m_model = getattr(instance, m2m_field_name).through
        try:
            rel_field_name = [
                field.name for field in m2m_model._meta.local_fields if field.name not in ['id', 'user']][0]
        except IndexError:
            raise ImproperlyConfigured(
                "Impossible to find name of relation attribute for instance %s in m2m like users table" % instance)

        ids = self.fetch_likes_user_ids(*args, **kwargs)
        if not ids:
            return self.none()

        # fetch users
        users = self.fetch(ids=ids, only_expired=True)

        ids_current = m2m_model.objects.filter(**{rel_field_name: instance}).values_list('user_id', flat=True)
        ids_new = users.values_list('pk', flat=True)
        ids_left = set(ids_current).difference(set(ids_new))
        ids_entered = set(ids_new).difference(set(ids_current))

        # delete left
        m2m_model.objects.filter(**{'user_id__in': ids_left, rel_field_name: instance}).delete()
        # make entered
        m2m_model.objects.bulk_create(
            [m2m_model(**{'user_id': user_pk, rel_field_name: instance}) for user_pk in ids_entered])

        return users


class UserRelative(models.Model):

    TYPE_CHOICES = (
        ('grandchild', u'внук/внучка'),
        ('grandparent', u'дедушка/бабушка'),
        ('child', u'сын/дочка'),
        ('sibling', u'брат/сестра'),
        ('parent', u'мама/папа'),
    )

    user1 = models.ForeignKey('User', related_name='user_relatives1')
    user2 = models.ForeignKey('User', related_name='user_relatives2')
    type = models.CharField(u'Тип родственной связи', max_length=20, choices=TYPE_CHOICES)


@python_2_unicode_compatible
class User(VkontaktePKModel):
    """
    Model of vkontakte user
    TODO: implement relatives
    """
    resolve_screen_name_types = ['user']
    slug_prefix = 'id'

    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    screen_name = models.CharField(max_length=32, db_index=True)
    nickname = models.CharField(max_length=32)

    sex = models.PositiveSmallIntegerField(null=True, choices=USER_SEX_CHOICES, db_index=True)
    age = models.PositiveSmallIntegerField(null=True, db_index=True)
    timezone = models.IntegerField(null=True)
    city = models.ForeignKey(City, null=True, on_delete=models.SET_NULL)
    country = models.ForeignKey(Country, null=True, on_delete=models.SET_NULL)
    rate = models.PositiveIntegerField(null=True, db_index=True)
    bdate = models.CharField(max_length=10)

    activity = models.TextField()
    relation = models.SmallIntegerField(null=True, choices=USER_RELATION_CHOICES, db_index=True)
    wall_comments = models.NullBooleanField()

    graduation = models.PositiveIntegerField(u'Дата окончания вуза', null=True)
    university = models.PositiveIntegerField(null=True)
    faculty = models.PositiveIntegerField(null=True)
    university_name = models.CharField(max_length=255)
    faculty_name = models.CharField(max_length=255)

    has_mobile = models.NullBooleanField(db_index=True)
    home_phone = models.CharField(max_length=24)
    mobile_phone = models.CharField(max_length=24)

    photo_fields = ['photo', 'photo_big', 'photo_medium', 'photo_medium_rec', 'photo_rec']
    photo = models.URLField()
    photo_big = models.URLField()
    photo_medium = models.URLField()
    photo_medium_rec = models.URLField()
    photo_rec = models.URLField()

    # social networks
    twitter = models.CharField(max_length=15)
    instagram = models.CharField(max_length=30)
    facebook = models.CharField(max_length=18)
    facebook_name = models.CharField(max_length=50)
    skype = models.CharField(max_length=32)  # in vk max_length=60
    livejournal = models.CharField(max_length=31)

    # profile info
    interests = models.TextField()
    movies = models.TextField()
    tv = models.TextField()
    books = models.TextField()
    games = models.TextField()
    about = models.TextField()

    # education
    universities = JSONField(blank=True, null=True)
    schools = JSONField(blank=True, null=True)

    friends_users = models.ManyToManyField('User', related_name='followers_users')
    friends_count = models.PositiveIntegerField(u'Друзей', default=0)

    # relatives = models.ManyToManyField('User', through=UserRelative)

    # counters
    # TODO: migrate all counter fields to *_count = models.PositiveIntegerField(u'Фотоальбомов', null=True)
    counters = ['albums', 'audios', 'followers', 'friends', 'mutual_friends',
                'notes', 'subscriptions', 'user_photos', 'user_videos', 'videos']

    sum_counters = models.PositiveIntegerField(default=0, help_text=u'Сумма всех счетчиков')
    counters_updated = models.DateTimeField(null=True, help_text=u'Счетчики были обновлены', db_index=True)

    albums = models.PositiveIntegerField(u'Фотоальбомов', default=0)
    videos = models.PositiveIntegerField(u'Видеозаписей', default=0)
    audios = models.PositiveIntegerField(u'Аудиозаписей', default=0)
    followers = models.PositiveIntegerField(u'Подписчиков', default=0)
    friends = models.PositiveIntegerField(u'Друзей', default=0, db_index=True)
    mutual_friends = models.PositiveIntegerField(u'Общих друзей', default=0)
    notes = models.PositiveIntegerField(u'Заметок', default=0)
    subscriptions = models.PositiveIntegerField(u'Подписок (только пользователи)', default=0)
    user_photos = models.PositiveIntegerField(u'Фотографий с пользователем', default=0)
    user_videos = models.PositiveIntegerField(u'Видеозаписей с пользователем', default=0)

    # extra fields, based on self.photo_fields and api
    is_deactivated = models.BooleanField(u'Деактивирован', default=False, db_index=True)
    has_avatar = models.BooleanField(u'Есть аватар', default=True, db_index=True)
    is_deleted = models.BooleanField(u'Удален', default=False)
    is_banned = models.BooleanField(u'Забанен', default=False)

    objects = UsersManager()
    remote = UsersRemoteManager(remote_pk=('remote_id',), version=5.8, methods={
        'get': 'users.get',
        'friends': 'friends.get',
    })

    class Meta:
        verbose_name = u'Пользователь Вконтакте'
        verbose_name_plural = u'Пользователи Вконтакте'

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def save(self, *args, **kwargs):

        # cut all CharFields to max allowed length
        for field in self._meta.local_fields:
            if isinstance(field, (models.CharField, models.TextField)):
                value = getattr(self, field.name)
                if isinstance(value, six.string_types):
                    # check strings for bad symbols in string encoding
                    # there is problems to save users with bad encoded activity strings like ID=88798245, ID=143523733
                    try:
                        value.encode('utf-16').decode('utf-16')
                    except UnicodeDecodeError:
                        value = ''
                if isinstance(field, models.CharField) and value:
                    value = value[:field.max_length]
                setattr(self, field.name, value)

        if self.relation and self.relation not in dict(USER_RELATION_CHOICES).keys():
            self.relation = None

        self.update()

        try:
            return super(User, self).save(*args, **kwargs)
        except Exception:
            log.error("Error while saving user ID=%s with fields %s" % (self.remote_id, self.__dict__))
            raise

    def update(self):
        self.update_age()
        self.update_deactivated_status()
        self.update_avatar_presence()
        self.check_sex()
        self.check_graduation()

    def check_sex(self):
        if self.sex not in [pair[0] for pair in USER_SEX_CHOICES]:
            self.sex = None

    def check_graduation(self):
        if self.graduation == 0:
            self.graduation = None

    def update_age(self):
        parts = self.bdate.split('.')
        if len(parts) == 3:
            try:
                parts = map(int, parts)
                born = date(parts[2], parts[1], parts[0])
            except ValueError:
                return
            # Using solution from here
            # http://stackoverflow.com/questions/2217488/age-from-birthdate-in-python/9754466#9754466
            today = date.today()
            self.age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))

    def update_deactivated_status(self):
        self.is_deactivated = False
        for field_name in self.photo_fields:
            if USER_PHOTO_DEACTIVATED_URL in getattr(self, field_name):
                self.is_deactivated = True
                return

    def update_avatar_presence(self):
        self.has_avatar = True
        for field_name in self.photo_fields:
            if USER_NO_PHOTO_URL in getattr(self, field_name):
                self.has_avatar = False
                return

    def _substitute(self, old_instance):
        """
        Save counters fields while updating user
        """
        for counter in self.counters:
            setattr(self, counter, getattr(old_instance, counter))

        self.sum_counters = old_instance.sum_counters
        self.counters_updated = old_instance.counters_updated
        self.friends_count = old_instance.friends_count
        super(User, self)._substitute(old_instance)

    def parse(self, response):
        if 'id' in response: # api version >= 5.23
            self.remote_id = response['id']

        if 'city' in response:
            city = response.pop('city')

            if isinstance(city, dict): # api version >= 5.23
                self.city = City.objects.get_or_create(remote_id=city['id'], defaults={'name': city['title']})[0]
            else:
                self.city = City.objects.get_or_create(remote_id=city)[0]
        if 'country' in response:
            country = response.pop('country')
            if isinstance(country, dict): # api version >= 5.23
                self.country = Country.objects.get_or_create(remote_id=country['id'], defaults={'name': country['title']})[0]
            else:
                self.country = Country.objects.get_or_create(remote_id=country)[0]
        if 'relatives' in response:
            relatives = response.pop('relatives')
            # doesn't work becouse of self.pk will be set lately
            # if self.pk:
            #     for relative in relatives:
            #         try:
            #             user_relative = UserRelative(
            #                 type=relative.type, user1=self, user2=User.objects.get(remote_id=relative.id))
            #             user_relative.save()
            #             self.relative.add(user_relative)
            #         except User.DoesNotExist:
            #             continue
        if 'deactivated' in response:
            response['is_deactivated'] = True
            response['is_deleted'] = response['deactivated'] == 'deleted'
            response['is_banned'] = response['deactivated'] == 'banned'
            response.pop('deactivated')

        for field_name in ['status_audio', 'online', 'relation_partner', 'type']:
            response.pop(field_name, None)

        super(User, self).parse(response)

    @property
    def refresh_kwargs(self):
        return {'ids': [self.remote_id]}

    def update_counters(self):
        """
        Update counters for user with special query and calculate sum of them
        """
        try:
            response = api_call('users.get', ids=self.remote_id, fields='counters')
        except VkontakteError, e:
            log.warning("There is vkontakte error [code=%d] while updating user [id=%d] counters: %s" % (
                e.code, self.remote_id, e.description))
            return False

        if 'counters' not in response[0]:
            log.info("There is no counters field in response %s" % response)
        else:
            for counter in self.counters:
                if counter in response[0]['counters']:
                    setattr(self, counter, response[0]['counters'][counter])

            self.sum_counters = sum([getattr(self, counter) for counter in self.counters])
        self.counters_updated = timezone.now()
        self.save()

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

    @atomic
    def fetch_friends(self, **kwargs):
        log.debug("Start updating friends of user %s" % self)
        if self.is_deactivated:
            return False

        try:
            log.debug("Fetch friends for user %s" % self)
            users = User.remote.fetch_friends(user=self, **kwargs)
        except VkontakteError, e:
            if e.code == 15:
                # update current user, make him deactivated
                User.remote.fetch(id=self.remote_id)
                return False
            else:
                raise e

        log.debug("Clear friends of user %s" % self)
        self.friends_users.clear()

        log.debug("Attach new friends to user %s" % self)
        m2m = self.friends_users.through
        m2m.objects.bulk_create([m2m(from_user_id=self.pk, to_user_id=user_id)
                                 for user_id in users.values_list('pk', flat=True)])

        log.debug("Update friends count of user %s" % self)
        self.friends_count = self.friends_users.count()
        self.save()

        return self.friends_users.all()

    def get_sex(self):
        return dict(USER_SEX_CHOICES).get(self.sex)

#    TODO: Solve naming, dublicate with boolean wall_comments
#    @property
#    def wall_comments(self):
#        if 'vkontakte_wall' not in settings.INSTALLED_APPS:
#            raise ImproperlyConfigured("Application 'vkontakte_wall' not in INSTALLED_APPS")
#        from vkontakte_wall.models import Comment
#        return Comment.objects.filter(remote_id__startswith='%s_' % self.remote_id)
