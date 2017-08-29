from .models import SingleUserStreamItem


class SingleTableDatabaseBackend(object):

    def add_stream_item(self, users, content, created_at):
        for user in users:
            SingleUserStreamItem.objects.create(user=user, content=content, created_at=created_at)

    def get_stream_items(self, user):
        return SingleUserStreamItem.objects.filter(user=user)
