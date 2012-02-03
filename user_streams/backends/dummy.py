
class DummyStreamItem(object):

    def __init__(self, content, created_at):
        self.content = content
        self.created_at = created_at


class MemoryStorage(object):

    def __init__(self):
        self.streams = {}

    def add_stream_item(self, users, content, created_at):
        stream_item = DummyStreamItem(content, created_at)
        for user in users:
            if user in self.streams:
                self.streams[user].insert(0, stream_item)
            else:
                self.streams[user] = [stream_item]

    def get_stream_items(self, user):
        return self.streams.get(user, [])

    def flush(self):
        self.streams = {}


storage = MemoryStorage()


class DummyBackend(object):

    """
    A dummy storage backend that stores user streams in memory.
    Only used for testing purposes.
    """

    def add_stream_item(self, users, content, created_at):
        storage.add_stream_item(users, content, created_at)

    def get_stream_items(self, user):
        return storage.get_stream_items(user)

    def flush(self):
        storage.flush()
