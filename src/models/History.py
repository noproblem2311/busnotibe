from django.db import models
from django.utils import timezone

class History(models.Model):
    id = models.UUIDField(primary_key=True)
    driver_id = models.UUIDField()
    child_id = models.UUIDField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    # add location when user tab
    location = models.TextField(null=True)
    type = models.TextField(null=True)
    class Meta:
        db_table = 'History'