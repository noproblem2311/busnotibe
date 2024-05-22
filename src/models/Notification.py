from django.db import models
from django.utils import timezone


class Notification(models.Model):
    id = models.UUIDField(primary_key=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.TextField()
    subtitle= models.TextField(null=True)
    body = models.TextField()
    parent_id = models.UUIDField()
    is_read= models.BooleanField(default=False)
    class Meta:
        db_table = 'Notification'