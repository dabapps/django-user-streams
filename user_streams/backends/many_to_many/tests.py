from user_streams import BACKEND_SETTING_NAME
from user_streams.tests import StreamStorageTestMixin
from user_streams.utils import TestCase, override_settings


BACKEND_SETTINGS = {BACKEND_SETTING_NAME: 'user_streams.backends.many_to_many.ManyToManyDatabaseBackend'}


@override_settings(**BACKEND_SETTINGS)
class ManyToManyDatabaseBackendTestCase(TestCase, StreamStorageTestMixin):
    pass
