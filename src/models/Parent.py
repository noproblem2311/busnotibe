from django.db import models

class Parent(models.Model):
    id = models.UUIDField(primary_key=True, default=models.UUIDField())
    user_name = models.TextField()
    email = models.TextField()
    password = models.TextField()
    avatar = models.TextField(null=True)
    date_of_birth = models.DateTimeField(null=True)

    class Meta:
        db_table = 'Parent'
