# Generated by Django 4.2.7 on 2024-01-22 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Reservations_Reviews_Contact', '0014_alter_contactus_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='created_at',
            field=models.DateField(blank=True, null=True),
        ),
    ]
