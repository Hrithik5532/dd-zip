# Generated by Django 4.2.7 on 2023-12-17 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0007_rename_veg_nonveg_product_veg_or_nonveg'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='img',
            field=models.ImageField(upload_to='Products/', verbose_name='Image'),
        ),
    ]
