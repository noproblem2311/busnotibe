from django.db import models
from django.utils import timezone
class Request(models.Model):
    id = models.UUIDField(primary_key=True)
    parent_id = models.UUIDField()
    status = models.TextField()
    admin_id = models.UUIDField(null=True)
    address = models.TextField(null=True)
    template_id = models.UUIDField(null=True)
    email = models.TextField(null=True)
    zip_postal = models.TextField(null=True)
    note = models.TextField(null=True)
    phone_number = models.TextField(null=True)
    shipping_by= models.TextField(null=True)
    shipping_code= models.TextField(null=True)
    name = models.TextField(null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'Request'