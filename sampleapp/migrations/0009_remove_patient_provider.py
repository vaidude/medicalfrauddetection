# Generated by Django 4.2 on 2024-04-09 03:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sampleapp', '0008_providers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='provider',
        ),
    ]
