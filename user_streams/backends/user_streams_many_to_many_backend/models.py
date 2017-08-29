from django.conf import settings
from django.db import models


class StreamItem(models.Model):

    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='+')
    content = models.TextField()
    created_at = models.DateTimeField()

    class Meta:
        ordering = ['-created_at']
