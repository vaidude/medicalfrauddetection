# Generated by Django 4.2 on 2024-04-10 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sampleapp', '0014_alter_patient_renaldiseaseindicator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adminreg',
            name='password',
            field=models.CharField(max_length=10),
        ),
    ]