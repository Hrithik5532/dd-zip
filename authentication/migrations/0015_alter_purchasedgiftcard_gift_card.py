# Generated by Django 5.1.1 on 2024-10-10 15:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authentication", "0014_remove_giftcarddesigns_description"),
    ]

    operations = [
        migrations.AlterField(
            model_name="purchasedgiftcard",
            name="gift_card",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="authentication.giftcarddesigns",
            ),
        ),
    ]
