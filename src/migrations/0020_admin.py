# Generated by Django 5.0.4 on 2024-05-15 07:54

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('src', '0019_driver_is_verify'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user_name', models.CharField(max_length=30)),
                ('email', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'Admin',
            },
        ),
    ]
