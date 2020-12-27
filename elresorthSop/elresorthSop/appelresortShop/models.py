from django.db import models
from django.contrib.auth.models import AbstractUser

# Modelo de datos de ARopa&Me

# Clase abstracta User
class User(AbstractUser):
    is_staff = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)

# Clase Oferta: ofertas que se aplican a los diferentes precios
class Oferta(models.Model): # TODO: a esta hay que darle una vuelta porq no sé muy bien cómo lo queremos tener
        descuento = models.IntegerField(default = 1)
        

# Clase Coleccion: grupos de items que salen una temporada/por un evento en concreto
class Coleccion(models.Model):
        nombre = models.CharField(max_length=50)
        fecha_introducido = models.DateField()
        descripcion = models.TextField(default="")
        ofertas = models.ManyToManyField(Oferta, blank=True) # blank nos pertmite meter o no ofertas a las colecciones
        def __str__(self):
                return self.nombre   
        

# Clase Item: cada artículo que se ponga a la venta será un Item
class Item(models.Model):
        #ID viene por defecto
        nombre = models.CharField(max_length=50) #ATENCIÓN!! cada item subido tiene que estar en una colección
        descripcion = models.TextField(default="")
        categoria = models.CharField(max_length=50) # Pantalón, Falda, Camiseta, Camisa...
        precio = models.IntegerField()    
        oferta = models.ForeignKey(Oferta, on_delete=models.CASCADE)              
        fecha_insertado = models.DateField() # Fecha en la que fue insertado         
        imagen = models.ImageField(upload_to ='uploads/') # Imagen del item
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
        GENEROS = (      # Mirar documentación de 'choices' en https://docs.djangoproject.com/en/3.1/topics/db/models/
        ('M', 'Hombre'), 
        ('F', 'Mujer'),
        ('U', 'Unisex'),
        )
        color = models.CharField(max_length=3, choices=COLORES) # Color del item
        genero = models.CharField(max_length=1, choices=GENEROS)

        # TODO: campo de Puntuación ??
        def __str__(self):
                return self.nombre



# Clase Producto: relaciona Tallas con Items (cada item tiene >=1 talla con un stock q indica el numero de productos)
class Producto(models.Model):
        item = models.ForeignKey(Item, on_delete=models.CASCADE)
        TALLAS = (      # Mirar documentación de 'choices' en https://docs.djangoproject.com/en/3.1/topics/db/models/
        ('XS', 'Extra Small'), 
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', 'ExtraExtra Large'),
        )
        talla = models.CharField(max_length=3, choices = TALLAS)
        stock = models.IntegerField(default=0)
        

class Carrito(models.Model):
        productos = models.ManyToManyField(Producto, blank=True)


class Tarjeta(models.Model):
        nombre = models.CharField(max_length=50, blank=True)
        apellidos = models.CharField(max_length=50, blank=True)
        num_tarjeta = models.IntegerField(blank = True)
        cvv = models.IntegerField(blank = True)
        fecha_caducidad = models.DateField(blank = True)
    
        def __str__(self):
                return self.nombre


# class Cliente(models.User): No sé si va aquí o en django.contrib.auth
class Cliente(models.Model):
        user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
        mail = models.EmailField(unique=True, blank=True)
        carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, blank = True)
        tarjeta = models.ForeignKey(Tarjeta, on_delete=models.CASCADE, blank = True)

        def __str__(self):
                return self.nombre

class Pedido(models.Model):
        numEnvio = id
        cliente = models.ForeignKey(Cliente,on_delete=models.CASCADE)
        carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
        tarjeta = models.ForeignKey(Tarjeta, on_delete=models.CASCADE)
        direccion = models.CharField(max_length=100)
        precio = models.IntegerField()
        
        def __str__(self):
                return self.numEnvio


#Decisión de diseño: Cliente van a ser tanto usuario como invitado. Ambos pueden navegar libremente por 
#la página lo unico que para el usuario tiene unos datos asociados y el invitado es por defecto vacio
#A la hora de gestionar la compra el invitado tendrá que poner datos de facturación.
#  usuario(admin, invitado, usuario) --> TODO : mirar clase User (permissions / groups)  https://docs.djangoproject.com/en/3.1/topics/auth/ 


#De aquí surgen nuevas dudas. Cliente asociado con Carrito para crear clase Pedido (numEnvio, etc)

