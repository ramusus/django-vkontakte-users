# Django Vkontakte Users

Приложение позволяет взаимодействовать с профилями пользователей Вконтакте через Вконтакте API используя стандартные модели Django

## Установка

    pip install django-vkontakte-users

В `settings.py` необходимо добавить:

    INSTALLED_APPS = (
        ...
        'vkontakte_api',
        'vkontakte_users',
    )

## Примеры использования

### Получение пользователей по ID

    >>> from vkontakte_users.models import User
    >>> User.remote.fetch(ids=[1,2,6])
    [<User: Павел Дуров>,
     <User: Александра Владимирова>,
     <User: Николай Дуров>]

### Получение пользователя по адресу страницы

    >>> from vkontakte_users.models import User
    >>> User.remote.get_by_slug('durov')
    <User: Павел Дуров>

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