from django.db import models

# Modelo de datos de ARopa&Me

# Clase Etiqueta: podremos señalar diferentes etiquetas en los Items
class Etiqueta(models.Model):
 nombre = models.CharField(max_length=50)
 def __str__(self):
        return self.nombre

# Clase Item: cada artículo que se ponga a la venta será un Item
class Item(models.Model):
        #ID viene por defecto
        TALLAS = (      # Mirar documentación de 'choices' en https://docs.djangoproject.com/en/3.1/topics/db/models/
        ('XS', 'Extra Small'), 
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        )
        nombre = models.CharField(max_length=50)
        coleccion = models.ForeignKey(Coleccion, on_delete=models.CASCADE) # TODO: ahora está como ForeignKey, si queremos hacer una lista tenemos que hacerla nosotros como campo a nuestro gusto
        precio = models.IntegerField()
        descripcion = models.TextField(default="") 
        visitas = models.IntegerField(default=0) # Num de visitas que ha recibido 
        talla = models.CharField(max_length=1, choices=TALLAS) # Talla 
        fecha_insertado = models.DateField() # Fecha en la que fue insertado 
        color = models.CharField(max_length=30) # Color del item                TODO: Se puede implementar mejor?
        imagen = models.ImageField() # Imagen del item
        etiquetas = models.ManyToManyField(Etiqueta)
        ofertas = models.ManyToManyField(Oferta, blank=true) # blank nos pertmite meter o no ofertas a los items
        # TODO: campo de Puntuación ??
        def __str__(self):
                return self.nombre

# Clase Coleccion: grupos de items que salen una temporada/por un evento en concreto
class Coleccion(models.Model):
 nombre = models.CharField(max_length=50)
 fecha_introducido = models.DateField()
 descripcion = models.TextField(default="")
 etiquetas = models.ManyToManyField(Etiqueta)
 ofertas = models.ManyToManyField(Oferta, blank=True) # blank nos pertmite meter o no ofertas a las colecciones
 def __str__(self):
        return self.nombre   

# Clase Comentario: TODO comentarios dentro de los items?
class Comentario(models.Model):
 item = models.ForeignKey(Item, on_delete=models.CASCADE)
 nombre = models.CharField(max_length=50)
 autor = models.CharField(max_length=50)
 fecha = models.DateField()
 texto_comentario = models.TextField(default="")
 def __str__(self):
        return self.nombre

# Clase Oferta: ofertas que se aplican a los diferentes precios
class Oferta(models.Model): # TODO: a esta hay que darle una vuelta porq no sé muy bien cómo lo queremos tener
        DESCUENTOS = (      # Mirar documentación de 'choices' en https://docs.djangoproject.com/en/3.1/topics/db/models/
        ('50%', 'Descuento a la mitad'), 
        ('30%', 'Descuento del 30%'),
        ('20%', 'Descuento del 20%'),
        ('2x1', 'Paga 1 y llévate otro gratis'),
        ('3x2', 'Paga 2 y llévate otro gratis'),
        )
        nombre = nombre = models.CharField(max_length=50)
        descripcion = models.TextField(default="")
        descuento = models.CharField(max_length=1, choices=DESCUENTOS)
        is_activa = models.BooleanField(default=False)
        fecha_fin = models.DateField()

        
#  usuario(admin, invitado, usuario) --> TODO : mirar clase User (permissions / groups)  https://docs.djangoproject.com/en/3.1/topics/auth/ 

# class Usuario(models.User): No sé si va aquí o en django.contrib.auth

# class Carrito(models.Model):
        #lista de items
        #1 por cada usuario
