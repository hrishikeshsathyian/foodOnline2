# Generated by Django 4.1.6 on 2023-03-15 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("menu", "0002_alter_category_category_name_alter_category_slug"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="category",
            options={"verbose_name": "Category", "verbose_name_plural": "ategories"},
        ),
        migrations.AlterField(
            model_name="category",
            name="slug",
            field=models.SlugField(max_length=90, unique=True),
        ),
    ]