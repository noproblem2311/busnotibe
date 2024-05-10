from django.utils import timezone
from django.db import models

class Parent(models.Model):
    id = models.UUIDField(primary_key=True, default=models.UUIDField())
    user_name = models.TextField()
    email = models.TextField()
    avatar = models.TextField(null=True)
    date_of_birth = models.DateTimeField(null=True)
    language = models.TextField(null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    device = models.TextField(null=True)
    class Meta:
        db_table = 'Parent'
