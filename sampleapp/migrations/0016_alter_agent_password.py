# Generated by Django 4.2 on 2024-04-10 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sampleapp', '0015_alter_adminreg_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agent',
            name='password',
            field=models.CharField(max_length=10),
        ),
    ]
