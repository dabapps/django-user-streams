from django.db import models
from django.conf import settings


class StreamItem(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+')
    content = models.TextField()
    created_at = models.DateTimeField()

    class Meta:
        ordering = ['-created_at']
