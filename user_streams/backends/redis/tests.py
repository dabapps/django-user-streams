from user_streams import BACKEND_SETTING_NAME
from user_streams.tests import StreamStorageTestMixin
from user_streams.utils import TestCase, override_settings

from . import Redis, KEY_PREFIX_SETTING_NAME


KEY_PREFIX = 'redis_backend_tests'
BACKEND_SETTINGS = {
    BACKEND_SETTING_NAME: 'user_streams.backends.redis.RedisBackend',
    KEY_PREFIX_SETTING_NAME: KEY_PREFIX,
}


@override_settings(**BACKEND_SETTINGS)
class RedisBackendTestCase(TestCase, StreamStorageTestMixin):

    def tearDown(self):
        client = Redis()
        keys = client.keys('%s*' % KEY_PREFIX)
        if keys:
            client.delete(*keys)
