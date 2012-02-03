from .models import StreamItem


class ManyToManyDatabaseBackend(object):

    def add_stream_item(self, users, content, created_at):
        item = StreamItem.objects.create(content=content, created_at=created_at)
        item.users.add(*[user.pk for user in users])

    def get_stream_items(self, user):
        return StreamItem.objects.filter(users=user)
