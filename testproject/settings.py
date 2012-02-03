
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
    'user_streams.backends.single_table',
    'user_streams.backends.many_to_many',
    'user_streams.backends.redis',
]
