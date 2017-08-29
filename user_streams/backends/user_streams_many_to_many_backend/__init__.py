from .models import MultiUserStreamItem


class ManyToManyDatabaseBackend(object):

    def add_stream_item(self, users, content, created_at):
        item = MultiUserStreamItem.objects.create(content=content, created_at=created_at)
        item.users.add(*[user.pk for user in users])

    def get_stream_items(self, user):
        return MultiUserStreamItem.objects.filter(users=user)
