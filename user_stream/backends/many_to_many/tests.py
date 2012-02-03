from user_stream import BACKEND_SETTING_NAME
from user_stream.tests import StreamStorageTestMixin
from user_stream.utils import TestCase, override_settings


BACKEND_SETTINGS = {BACKEND_SETTING_NAME: 'user_stream.backends.many_to_many.ManyToManyDatabaseBackend'}


class ManyToManyDatabaseBackendTestCase(TestCase, StreamStorageTestMixin):
    pass


ManyToManyDatabaseBackendTestCase = override_settings(**BACKEND_SETTINGS)(ManyToManyDatabaseBackendTestCase)
