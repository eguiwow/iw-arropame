# Generated by Django 3.1.3 on 2020-11-29 17:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appelresortShop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='carrito',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='appelresortShop.carrito'),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='tarjeta',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='appelresortShop.tarjeta'),
        ),
    ]
