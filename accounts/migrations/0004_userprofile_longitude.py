# Generated by Django 4.1.6 on 2023-03-10 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0003_alter_user_role"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="longitude",
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
