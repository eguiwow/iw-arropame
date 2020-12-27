from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms import ModelForm
from django.forms.utils import ValidationError
from .models import User, Oferta, Coleccion, Item, Producto, Carrito, Tarjeta, Cliente, Pedido
from datetime import date

class ClientSignUpForm(UserCreationForm):
    mail = forms.CharField(label = "Introduce el correo electronico", max_length=50)

    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_client = True
        if commit:
            user.save()
        return user

# class ItemForm(ModelForm):
#     class Meta:
#         model = Item
#         fields = '__all__'


class ItemForm(forms.Form):
    nombre = forms.CharField(label = "Introduce el nombre del producto", max_length=50)
    descripcion = forms.CharField(label = "Descripcion del producto", max_length=50) 
    
    ETIQUETAS = (
        ('Chaquetas', 'Chaquetas'),
        ('Jerséis', 'Jerséis'),
        ('Sudaderas', 'Sudaderas'),
        ('Camisas', 'Camisas'),
		('Camisetas', 'Camisetas'),
        ('Pantalones', 'Pantalones'),
        ('Bañadores y ropa de baño', 'Bañadores y ropa de baño'),										
    )

    categoria = forms.ChoiceField(label = "Categoría", choices=ETIQUETAS)

    precio = forms.IntegerField(label = "Introduce el precio")   
    imagen = forms.ImageField(required= False) # Imagen del item          
    COLORES = (
        ('Bl', 'Blanco'),
        ('N', 'Negro'),
        ('Rj', 'Rojo'),
        ('Rs', 'Rosa'),
        ('Am', 'Amarillo'),
        ('Nj', 'Naranja'),
        ('Az', 'Azul'),
        ('Mrr', 'Marrón'),
        ('Mor', 'Morado'),
        ('V', 'Verde'),
        ('Gr', 'Gris'),
        )
    
    color = forms.ChoiceField(label = "Color del producto", choices=COLORES) # Color del item
    

    GENEROS = (      # Mirar documentación de 'choices' en https://docs.djangoproject.com/en/3.1/topics/db/models/
        ('M', 'Hombre'), 
        ('F', 'Mujer'),
        ('U', 'Unisex'),
        )
    genero = forms.ChoiceField(choices=GENEROS)
    
    stock_talla_xs = forms.IntegerField(label= "Numero de XS:")
    stock_talla_s = forms.IntegerField(label= "Numero de S:")
    stock_talla_m = forms.IntegerField(label= "Numero de M:")
    stock_talla_l = forms.IntegerField(label= "Numero de L:")
    stock_talla_xl = forms.IntegerField(label= "Numero de XL:")
    stock_talla_xxl = forms.IntegerField(label= "Numero de XXL:")
 