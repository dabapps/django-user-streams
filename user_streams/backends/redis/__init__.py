try:
    from redis import Redis
except ImportError:
    raise ImportError('Please install the redis-py module (pip install redis)')


from datetime import datetime
import time


KEY_PREFIX_SETTING_NAME = 'USER_STREAMS_REDIS_KEY_PREFIX'
DEFAULT_KEY_PREFIX = 'user_streams'


redis_client = Redis() # TODO support overriding arguments


def create_key(key):
    from django.conf import settings
    prefix = getattr(settings, KEY_PREFIX_SETTING_NAME, DEFAULT_KEY_PREFIX)
    return "%s:%s" % (prefix, key)


class RedisBackend(object):

    def add_stream_item(self, users, content, created_at):
        for user in users:
            key = create_key('user:%s' % user.pk)
            timestamp = time.mktime(created_at.timetuple())
            redis_client.zadd(key, content, timestamp)

    def get_stream_items(self, user):
        return LazyResultSet(user)


class LazyResultSet(object):

    def __init__(self, user):
        self.key = create_key('user:%s' % user.pk)

    def __len__(self):
        return redis_client.zcard(self.key)

    def __getitem__(self, item):
        if isinstance(item, slice):
            start = item.start or 0
            stop = item.stop or -1
        else:
            start = item
            stop = item

        result = redis_client.zrange(self.key, start, stop, desc=True, withscores=True)
        for content, timestamp in result:
            created_at = datetime.fromtimestamp(timestamp)
            return StreamItem(content, created_at)


class StreamItem(object):

    def __init__(self, content, created_at):
        self.content = content
        self.created_at = created_at
