# Generated by Django 5.0.4 on 2024-06-11 05:26

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('src', '0024_notification_is_read_alter_notification_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserKey',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('user_id', models.UUIDField()),
                ('key', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]