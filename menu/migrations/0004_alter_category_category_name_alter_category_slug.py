# Generated by Django 4.1.6 on 2023-03-15 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("menu", "0003_alter_category_options_alter_category_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="category_name",
            field=models.TextField(max_length=500, unique=True),
        ),
        migrations.AlterField(
            model_name="category",
            name="slug",
            field=models.SlugField(max_length=500, unique=True),
        ),
    ]
