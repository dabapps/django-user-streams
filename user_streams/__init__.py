from datetime import datetime
from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module


BACKEND_SETTING_NAME = 'USER_STREAMS_BACKEND'
USE_UTC_SETTING_NAME = 'USER_STREAMS_USE_UTC'


def get_backend():
    """
    Return the stream storage backend configured in the settings
    """
    from django.conf import settings
    backend_path = getattr(settings, BACKEND_SETTING_NAME, None)
    if not backend_path:
        raise ImproperlyConfigured('No user stream storage backend has been configured. Please set %s correctly' % BACKEND_SETTING_NAME)

    try:
        module_name, class_name = backend_path.rsplit('.', 1)
    except ValueError:
        raise ImproperlyConfigured('%s is not a valid value for the %s setting' % (backend_path, BACKEND_SETTING_NAME))

    try:
        module = import_module(module_name)
    except ImportError, e:
        raise ImproperlyConfigured('Error importing user stream backend %s: %s' % (backend_path, e))

    try:
        cls = getattr(module, class_name)
    except AttributeError:
        raise ImproperlyConfigured('Error importing user stream backend class %s' % backend_path)

    return cls()


def create_iterable(item_or_iterable):
    """
    If the argument is iterable, just return it. Otherwise, return a list
    containing the item.
    """
    try:
        iter(item_or_iterable)
        return item_or_iterable
    except TypeError:
        return [item_or_iterable]


def now():
    """
    Return a datetime object representing the current time
    """
    from django.conf import settings
    use_utc = getattr(settings, USE_UTC_SETTING_NAME, False)
    if use_utc:
        return datetime.utcnow()
    else:
        return datetime.now()


def add_stream_item(user_or_users, content, created_at=None):
    """
    Add a single message to the stream of one or more users.
    """
    backend = get_backend()
    users = create_iterable(user_or_users)
    created_at = created_at or now()
    backend.add_stream_item(users, content, created_at)


def get_stream_items(user):
    """
    Retrieve the stream for a single user.
    """
    backend = get_backend()
    return backend.get_stream_items(user)
