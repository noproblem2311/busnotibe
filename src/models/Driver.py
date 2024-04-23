from django.db import models


class Driver(models.Model):
    id = models.UUIDField(primary_key=True)
    user_name = models.TextField()
    email = models.TextField()
    password = models.TextField()
    avatar = models.TextField(null=True)
    date_of_birth = models.DateTimeField(null=True)
    company = models.TextField()
    license = models.TextField()
    bus_number = models.TextField()
    class Meta:
        db_table = 'Driver'
