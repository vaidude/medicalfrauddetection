# Generated by Django 4.2 on 2024-04-10 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sampleapp', '0010_rename_email_patient_beneficiaryid_patient_provider_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='agemail',
            field=models.EmailField(default=1, max_length=40),
            preserve_default=False,
        ),
    ]