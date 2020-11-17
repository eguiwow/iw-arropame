from django.db import models

# Modelo de datos de ARopa&Me

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
        precio = models.IntegerField()
        descripcion = models.TextField(default="") 
        visitas = models.IntegerField(default=0) # Num de visitas que ha recibido 
        talla = models.CharField(max_length=1, choices=TALLAS) # Talla 
        fecha_insertado = models.DateField() # Fecha en la que fue insertado 
        color = models.CharField(max_length=30) # Color del item                TODO: Se puede implementar mejor?
        imagen = models.ImageField() # Imagen del item
        def __str__(self):
                return self.nombre

# Clase Etiqueta, podremos señalar diferentes etiquetas en los Items
class Etiqueta(models.Model):
 nombre = models.CharField(max_length=50)
 def __str__(self):
        return self.nombre

# Clase Post como Entrada del blog
class Post(models.Model):
 nombre = models.CharField(max_length=50)
 autor = models.CharField(max_length=50)
 fecha = models.DateField()
 texto_entrada = models.TextField(default="")
 visitas = models.IntegerField(default=0)
 etiquetas = models.ManyToManyField(Etiqueta)
 def __str__(self):
        return self.nombre   

class Comentario(models.Model):
 post = models.ForeignKey(Post, on_delete=models.CASCADE)
 nombre = models.CharField(max_length=50)
 autor = models.CharField(max_length=50)
 fecha = models.DateField()
 texto_comentario = models.TextField(default="")
 def __str__(self):
        return self.nombre
