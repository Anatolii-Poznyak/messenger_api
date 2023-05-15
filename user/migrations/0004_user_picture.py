# Generated by Django 4.2 on 2023-04-23 21:02

from django.db import migrations, models
import user.models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0003_user_bio"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="picture",
            field=models.ImageField(
                null=True, upload_to=user.models.user_picture_file_path
            ),
        ),
    ]