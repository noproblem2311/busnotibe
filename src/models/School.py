from django.db import models
from django.utils import timezone

class School(models.Model):
    id = models.UUIDField(primary_key=True)
    name_en = models.CharField(max_length=255)
    name_cn = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'School'