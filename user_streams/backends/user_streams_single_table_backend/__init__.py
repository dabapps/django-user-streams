from .models import StreamItem


class SingleTableDatabaseBackend(object):

    def add_stream_item(self, users, content, created_at):
        for user in users:
            StreamItem.objects.create(user=user, content=content, created_at=created_at)

    def get_stream_items(self, user):
        return StreamItem.objects.filter(user=user)
