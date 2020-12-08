from django.urls import path
from . import views

urlpatterns = [
 path('', views.index, name='index'),
 path('administrar/', views.administrar, name = 'administrar'),
 path('anyadido/', views.anyadido, name = 'anyadido'),
 path('hombre/chaquetas/', views.chaquetasH, name = 'chaquetasH'),
 path('mujer/chaquetas/', views.chaquetasM, name = 'chaquetasM'),
 path('producto/<int:item_id>', views.producto, name = 'producto'),
 path('carrito/<int:producto_id>', views.carrito, name = 'carrito'), # esta url es para probar que podemos guardar al carrito bien habría que hacerlo directamente con js desde 'producto.html'
]