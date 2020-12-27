from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('administrar/', views.administrar, name = 'administrar'),
    path('anyadido/', views.anyadido, name = 'anyadido'),
    path('producto/<int:item_id>/', views.producto, name = 'producto'),
    path('carrito/', views.carrito, name = 'carrito'),
    path('compra/', views.compra, name = 'compra'),
    path('carrito/?id=<int:producto_id>/', views.carrito_anyadir, name = 'carrito_anyadir'), # esta url es para probar que podemos guardar al carrito bien habría que hacerlo directamente con js desde 'producto.html'
    path('<str:genero>/<str:tipo>/', views.articulos, name = 'articulos'), # El ultimo por que sino coge por defecto el str:genero como cualquier cadena que se meta
]