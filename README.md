### Вступление

Приложение позволяет взаимодействовать с профилями пользователей Вконтакте через Вконтакте API используя стандартные модели Django

### Установка

    pip install django-vkontakte-users

В `settings.py` необходимо добавить:

    INSTALLED_APPS = (
        ...
        'vkontakte_api',
        'vkontakte_users',
    )

### Примеры использования

#### Получение пользователей по ID

    >>> from vkontakte_users.models import User
    >>> User.remote.fetch(ids=[1,2,6])
    [<User: Павел Дуров>,
     <User: Александра Владимирова>,
     <User: Николай Дуров>]

#### Получение пользователя по адресу страницы

    >>> User.remote.get_by_slug('durov')
    <User: Павел Дуров>

#### Получение друзей пользователя

    >>> users = User.remote.fetch(ids=[1])
    >>> users[0].fetch_friends()
    [<User: Александра Владимирова>, <User: Илья Перекопский>, <User: Николай Дуров>, '...(remaining elements truncated)...']
    >>> users[0].friends_users.count()
    668
