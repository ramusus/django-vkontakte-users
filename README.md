Django Vkontakte Users
======================

[![PyPI version](https://badge.fury.io/py/django-vkontakte-users.png)](http://badge.fury.io/py/django-vkontakte-users) [![Build Status](https://travis-ci.org/ramusus/django-vkontakte-users.png?branch=master)](https://travis-ci.org/ramusus/django-vkontakte-users) [![Coverage Status](https://coveralls.io/repos/ramusus/django-vkontakte-users/badge.png?branch=master)](https://coveralls.io/r/ramusus/django-vkontakte-users)

Приложение позволяет взаимодействовать с профилями пользователей Вконтакте через Вконтакте API используя стандартные модели Django

Установка
---------

    pip install django-vkontakte-users

В `settings.py` необходимо добавить:

    INSTALLED_APPS = (
        ...
        'oauth_tokens',
        'taggit',
        'vkontakte_api',
        'vkontakte_places',
        'vkontakte_users',
    )

    # oauth-tokens settings
    OAUTH_TOKENS_HISTORY = True                                         # to keep in DB expired access tokens
    OAUTH_TOKENS_VKONTAKTE_CLIENT_ID = ''                               # application ID
    OAUTH_TOKENS_VKONTAKTE_CLIENT_SECRET = ''                           # application secret key
    OAUTH_TOKENS_VKONTAKTE_SCOPE = ['ads,wall,photos,friends,stats']    # application scopes
    OAUTH_TOKENS_VKONTAKTE_USERNAME = ''                                # user login
    OAUTH_TOKENS_VKONTAKTE_PASSWORD = ''                                # user password
    OAUTH_TOKENS_VKONTAKTE_PHONE_END = ''                               # last 4 digits of user mobile phone

Покрытие методов API
--------------------

* [users.get](http://vk.com/dev/users.get) - возвращает расширенную информацию о пользователях;
* [friends.get](http://vk.com/dev/friends.get) – возвращает список id друзей пользователя;
* [likes.getList](http://vk.com/dev/likes.getList) – возвращает список пользователей, которые добавили объект в список «Мне нравится»;

Примеры использования
---------------------

### Получение пользователей по ID

    >>> from vkontakte_users.models import User
    >>> User.remote.fetch(ids=[1,2,6])
    [<User: Павел Дуров>,
     <User: Александра Владимирова>,
     <User: Николай Дуров>]

### Получение пользователя по адресу страницы

    >>> from vkontakte_users.models import User
    >>> user = User.remote.get_by_slug('durov')
    >>> user
    <User: Павел Дуров>
    >>> user.__dict__
    {'_state': <django.db.models.base.ModelState at 0xb2eba8c>,
     'about': u'Steve Dogs',
     'activity': u'',
     'albums': 3,
     'audios': 111,
     'bdate': u'10.10.1984',
     'books': u'',
     'city_id': 380,
     'counters_updated': datetime.datetime(2012, 3, 14, 0, 13, 14, 819693),
     'country_id': 160,
     'facebook': u'',
     'facebook_name': u'',
     'faculty': 15,
     'faculty_name': u'Филологический',
     'fetched': datetime.datetime(2013, 2, 14, 15, 13, 46, 673793),
     'first_name': u'Павел',
     'followers': 3437985,
     'friends': 524,
     'friends_count': 0,
     'games': u'',
     'graduation': 2006,
     'has_mobile': True,
     'home_phone': u'',
     'id': 2765,
     'interests': u'',
     'last_name': u'Дуров',
     'livejournal': u'durov',
     'mobile_phone': u'',
     'movies': u"Flying Over Cuckoo's Nest, Rainman, Fight Club, Matrix, Equilibrium, Watchmen",
     'mutual_friends': 0,
     'notes': 6,
     'photo': u'http://cs7003.userapi.com/v7003815/22a1/xgG9fb-IJ3Y.jpg',
     'photo_big': u'http://cs7003.userapi.com/v7003685/1ddd/jZ8LZcwYN20.jpg',
     'photo_medium': u'http://cs7003.userapi.com/v7003793/2184/qgHVkPyWj6A.jpg',
     'photo_medium_rec': u'',
     'photo_rec': u'',
     'rate': None,
     'relation': 1,
     'remote_id': 1L,
     'screen_name': u'durov',
     'sex': 2,
     'skype': u'',
     'subscriptions': 1,
     'sum_counters': 3438644,
     'timezone': 3,
     'tv': u'',
     'twitter': u'durov',
     'university': 1,
     'university_name': u'СПбГУ',
     'user_photos': 4,
     'user_videos': 1,
     'videos': 9,
     'wall_comments': False}

### Получение друзей пользователя

    >>> from vkontakte_users.models import User
    >>> user = User.remote.fetch(ids=[1])[0]
    >>> user.fetch_friends()
    [<User: Александра Владимирова>, <User: Илья Перекопский>, <User: Николай Дуров>, '...(remaining elements truncated)...']

Друзья пользователя доступны через менеджер

    >>> user.friends_users.count()
    668

### Получение сообщений со стены пользователя через метод пользователя

Для этого необходимо установить дополнительно приложение
[`django-vkontakte-wall`](http://github.com/ramusus/django-vkontakte-wall/) и добавить его в `INSTALLED_APPS`

    >>> from vkontakte_users.models import User
    >>> user = User.remote.fetch(ids=[1])[0]
    >>> user.fetch_posts()
    [<Post: ...>, <Post: ...>, <Post: ...>, '...(remaining elements truncated)...']

Сообщения пользователя доступны через менеджер

    >>> user.wall_posts.count()
    432

Комментарии всех сообщений пользователя доступны через менеджер

    >>> user.wall_comments.count()
    73637