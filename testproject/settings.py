
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
}

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'user_streams',
    'user_streams.backends.user_streams_single_table_backend',
    'user_streams.backends.user_streams_many_to_many_backend',
    'user_streams.backends.user_streams_redis_backend',
]

SECRET_KEY = 'foobar'
