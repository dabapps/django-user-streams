from django.db import models


class StreamItem(models.Model):

    users = models.ManyToManyField('auth.User', related_name='+')
    content = models.TextField()
    created_at = models.DateTimeField()

    class Meta:
        ordering = ['-created_at']
