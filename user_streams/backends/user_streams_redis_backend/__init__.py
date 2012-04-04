try:
    from redis import Redis
except ImportError:
    raise ImportError('Please install the redis-py module (pip install redis)')


from datetime import datetime
from django.utils.encoding import smart_str, smart_unicode
import time
from uuid import uuid4


KEY_PREFIX_SETTING_NAME = 'USER_STREAMS_REDIS_KEY_PREFIX'
DEFAULT_KEY_PREFIX = 'user_streams'
CLIENT_ARGUMENTS_SETTING_NAME = 'USER_STREAMS_REDIS_CLIENT_ARGUMENTS'


def get_redis_client():
    from django.conf import settings
    client_arguments = getattr(settings, CLIENT_ARGUMENTS_SETTING_NAME, {})
    return Redis(**client_arguments)


def create_key(key):
    from django.conf import settings
    prefix = getattr(settings, KEY_PREFIX_SETTING_NAME, DEFAULT_KEY_PREFIX)
    return "%s:%s" % (prefix, key)


def add_header(content):
    """
    We need to add a unique header to each message, as duplicate items
    will otherwise be overwritten
    """
    return uuid4().hex + smart_str(content)


def remove_header(content):
    return smart_unicode(content[32:])


class RedisBackend(object):

    def __init__(self):
        self.redis_client = get_redis_client()

    def add_stream_item(self, users, content, created_at):
        content = add_header(content)
        for user in users:
            key = create_key('user:%s' % user.pk)
            timestamp = time.mktime(created_at.timetuple())
            self.redis_client.zadd(key, content, timestamp)

    def get_stream_items(self, user):
        return LazyResultSet(user)


class LazyResultSet(object):

    def __init__(self, user):
        self.user = user
        self.start = 0
        self.stop = -1
        self._results = None

    @property
    def key(self):
        return create_key('user:%s' % self.user.pk)

    def clone(self):
        cloned = LazyResultSet(self.user)
        cloned.start = self.start
        cloned.stop = self.stop
        return cloned

    def load_results(self):
        client = get_redis_client()
        self._results = client.zrange(
            self.key,
            self.start,
            self.stop,
            desc=True,
            withscores=True
        )

    def get_results(self):
        if self._results is None:
            self.load_results()
        return self._results

    def __len__(self):
        if self._results is not None:
            return len(self._results)

        if self.start == 0 and self.stop == -1:
            client = get_redis_client()
            return client.zcard(self.key)

        results = self.get_results()
        return len(results)

    def create_item(self, result):
        content, timestamp = result
        content = remove_header(content)
        created_at = datetime.fromtimestamp(timestamp)
        return StreamItem(content, created_at)

    def __getitem__(self, item):
        if isinstance(item, slice):
            clone = self.clone()
            clone.start = item.start or 0
            clone.stop = item.stop or  0
            clone.stop -= 1
            return clone
        else:
            return self.create_item(self.get_results()[item])


class StreamItem(object):

    def __init__(self, content, created_at):
        self.content = content
        self.created_at = created_at
