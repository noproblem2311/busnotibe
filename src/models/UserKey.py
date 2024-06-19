from django.db import models
from django.utils import timezone

class UserKey(models.Model):
    id = models.UUIDField(primary_key=True)
    user_id = models.UUIDField()
    key = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'UserKey'