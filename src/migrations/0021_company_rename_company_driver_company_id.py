# Generated by Django 5.0.4 on 2024-05-16 02:04

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('src', '0020_admin'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('name_en', models.CharField(max_length=255)),
                ('name_cn', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'Company',
            },
        ),
        migrations.RenameField(
            model_name='driver',
            old_name='company',
            new_name='company_id',
        ),
    ]