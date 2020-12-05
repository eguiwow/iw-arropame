from django.urls import path
from . import views

urlpatterns = [
 path('', views.index, name='index'),
 path('administrar/', views.administrar, name = 'administrar'),
 path('anyadido/', views.anyadido, name = 'anyadido'),
 path('hombre/chaquetas/', views.chaquetasH, name = 'chaquetasH'),
 path('mujer/chaquetas/', views.chaquetasM, name = 'chaquetasM'),
]