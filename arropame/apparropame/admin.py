from django.contrib import admin

from .models import Etiqueta, Oferta, Coleccion, Item, Comentario
admin.site.register(Etiqueta)
admin.site.register(Oferta)
admin.site.register(Coleccion)
admin.site.register(Item)
admin.site.register(Comentario)
