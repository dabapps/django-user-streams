
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    },
}

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'user_stream',
    'user_stream.backends.single_table',
    'user_stream.backends.many_to_many',
]
