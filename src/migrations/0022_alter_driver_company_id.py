# Generated by Django 5.0.4 on 2024-05-16 02:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('src', '0021_company_rename_company_driver_company_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driver',
            name='company_id',
            field=models.UUIDField(null=True),
        ),
    ]