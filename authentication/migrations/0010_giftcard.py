# Generated by Django 5.1.1 on 2024-10-09 22:03

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authentication", "0009_order_order_type"),
    ]

    operations = [
        migrations.CreateModel(
            name="GiftCard",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("heading", models.CharField(max_length=400)),
                ("description", ckeditor.fields.RichTextField()),
                ("image", models.ImageField(upload_to="Gift-Card/")),
                ("created_at", models.DateTimeField(auto_now=True)),
                ("updated_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
