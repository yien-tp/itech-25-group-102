# Generated by Django 5.1.6 on 2025-02-28 00:57

import trails_web.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("trails_web", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userprofile",
            name="personal_image",
            field=models.ImageField(
                blank=True, null=True, upload_to=trails_web.models.ProfileImagePath()
            ),
        ),
    ]
