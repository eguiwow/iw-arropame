# Generated by Django 3.1.2 on 2020-12-26 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appelresortShop', '0002_auto_20201129_1827'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='imagen',
            field=models.ImageField(upload_to='uploads/'),
        ),
    ]