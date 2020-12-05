from django.contrib import admin

from .models import Oferta, Coleccion, Item, Carrito, Producto, Tarjeta, Pedido, Cliente
admin.site.register(Oferta)
admin.site.register(Coleccion)
admin.site.register(Item)
admin.site.register(Carrito)
admin.site.register(Producto)
admin.site.register(Tarjeta)
admin.site.register(Pedido)
admin.site.register(Cliente)