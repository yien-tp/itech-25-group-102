# Generated by Django 5.1.6 on 2025-02-28 01:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("trails_web", "0002_alter_userprofile_personal_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="personal_bio",
            field=models.TextField(blank=True),
        ),
    ]
