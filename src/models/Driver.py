from django.db import models
from django.utils import timezone


class Driver(models.Model):
    id = models.UUIDField(primary_key=True)
    user_name = models.TextField()
    email = models.TextField()
    avatar = models.TextField(null=True)
    date_of_birth = models.DateTimeField(null=True)
    company = models.TextField(null=True)
    license = models.TextField(null=True)
    bus_number = models.TextField(null=True)
    phone_number = models.TextField(null=True)
    language = models.TextField(null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_verify = models.BooleanField(default=False)

    class Meta:
        db_table = 'Driver'

