from django.db import models
from django.utils import timezone

class Template(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.TextField()
    image = models.TextField()
    price = models.FloatField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'Template'