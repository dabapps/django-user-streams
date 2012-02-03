from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module


BACKEND_SETTING_NAME = 'USER_STREAM_BACKEND'


def get_backend():
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


def add_stream_item():
    backend = get_backend()
