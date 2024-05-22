from django.db import models
from django.utils import timezone

class Admin(models.Model):
    id = models.UUIDField(primary_key=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    user_name = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    class Meta:
        db_table = 'Admin'