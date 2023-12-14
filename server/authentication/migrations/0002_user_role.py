# Generated by Django 4.2.7 on 2023-12-14 06:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("authentication", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="role",
            field=models.CharField(
                choices=[("admin", "Administrator"), ("user", "User")],
                default="user",
                max_length=5,
            ),
        ),
    ]
