from django.db import models
from django.utils import timezone

class Child(models.Model):
    id = models.UUIDField(primary_key=True)
    parent_id = models.UUIDField()
    child_name = models.TextField()
    nickname = models.TextField()
    gender = models.TextField()
    date_of_birth = models.DateTimeField(null=True)
    card_number = models.TextField(null=True)
    avatar = models.TextField(null=True)
    name = models.TextField()
    school_id = models.UUIDField(null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'Child'