from django.db import models


class StreamItem(models.Model):

    user = models.ForeignKey('auth.User', related_name='+')
    content = models.TextField()
    created_at = models.DateTimeField()

    class Meta:
        ordering = ['-created_at']
