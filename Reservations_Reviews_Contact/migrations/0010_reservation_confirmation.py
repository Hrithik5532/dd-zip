# Generated by Django 4.2.7 on 2023-12-19 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Reservations_Reviews_Contact', '0009_alter_reservation_date_alter_reservation_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='confirmation',
            field=models.BooleanField(default=False),
        ),
    ]
