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
        self.key = create_key('user:%s' % user.pk)
        self.redis_client = get_redis_client()

    def __len__(self):
        return self.redis_client.zcard(self.key)

    def __getitem__(self, item):
        multi = isinstance(item, slice)

        if multi:
            start = item.start or 0
            stop = item.stop - 1
        else:
            start = item
            stop = item

        result = self.redis_client.zrange(self.key, start, stop, desc=True, withscores=True)

        stream_items = []
        for content, timestamp in result:
            created_at = datetime.fromtimestamp(timestamp)
            content = remove_header(content)
            stream_items.append(StreamItem(content, created_at))

        if multi:
            return stream_items
        else:
            return stream_items[0]


class StreamItem(object):

    def __init__(self, content, created_at):
        self.content = content
        self.created_at = created_at
