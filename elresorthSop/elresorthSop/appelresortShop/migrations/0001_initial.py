# Generated by Django 3.1.3 on 2020-11-29 16:44

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_staff', models.BooleanField(default=False)),
                ('is_client', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.TextField(default='')),
                ('categoria', models.CharField(max_length=50)),
                ('precio', models.IntegerField()),
                ('fecha_insertado', models.DateField()),
                ('imagen', models.ImageField(blank=True, upload_to='')),
                ('color', models.CharField(choices=[('Bl', 'Blanco'), ('N', 'Negro'), ('Rj', 'Rojo'), ('Rs', 'Rosa'), ('Am', 'Amarillo'), ('Nj', 'Naranja'), ('Az', 'Azul'), ('Mrr', 'Marrón'), ('Mor', 'Morado'), ('V', 'Verde'), ('Gr', 'Gris')], max_length=3)),
                ('genero', models.CharField(choices=[('M', 'Hombre'), ('F', 'Mujer'), ('U', 'Unisex')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Oferta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descuento', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Tarjeta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=50)),
                ('apellidos', models.CharField(blank=True, max_length=50)),
                ('num_tarjeta', models.IntegerField(blank=True)),
                ('cvv', models.IntegerField(blank=True)),
                ('fecha_caducidad', models.DateField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='appelresortShop.user')),
                ('nombre', models.CharField(blank=True, max_length=50)),
                ('password', models.CharField(blank=True, max_length=50)),
                ('mail', models.EmailField(blank=True, max_length=254, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('talla', models.CharField(choices=[('XS', 'Extra Small'), ('S', 'Small'), ('M', 'Medium'), ('L', 'Large'), ('XL', 'Extra Large'), ('XXL', 'ExtraExtra Large')], max_length=3)),
                ('stock', models.IntegerField(default=0)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appelresortShop.item')),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='oferta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appelresortShop.oferta'),
        ),
        migrations.CreateModel(
            name='Coleccion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('fecha_introducido', models.DateField()),
                ('descripcion', models.TextField(default='')),
                ('ofertas', models.ManyToManyField(blank=True, to='appelresortShop.Oferta')),
            ],
        ),
        migrations.CreateModel(
            name='Carrito',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productos', models.ManyToManyField(blank=True, to='appelresortShop.Producto')),
            ],
        ),
        
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('direccion', models.CharField(max_length=100)),
                ('precio', models.IntegerField()),
                ('carrito', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appelresortShop.carrito')),
                ('tarjeta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appelresortShop.tarjeta')),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appelresortShop.cliente')),
            ],
        ),
        migrations.AddField(
            model_name='cliente',
            name='carrito',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appelresortShop.carrito'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='tarjeta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appelresortShop.tarjeta'),
        ),
    ]
