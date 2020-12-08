from django.shortcuts import render
from django.shortcuts import get_object_or_404, get_list_or_404
from django.http import HttpResponse
from .models import User, Oferta, Item, Producto, Carrito, Cliente
from .forms import ClientSignUpForm, itemForm
from django.views.generic import CreateView
from django.contrib.auth import login
from django.shortcuts import redirect
from .decorators import staff_required
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db import transaction
from datetime import date

def index(request):
    ofertas = Oferta.objects.all()
    hay_ofertas = False
    for o in ofertas:
        if o.descuento != 1:
            hay_ofertas = True

    context = {"ofertas": hay_ofertas}
    return render(request, 'index.html', context)

def chaquetasH(request):
    items = Item.objects.all()
    nom = "chaqueta"
    lista_items = []
    for i in items:
        if(i.categoria=="Chaqueta" and i.genero =="M"):
            lista_items.append(i)
    
    context = {"lista_items": lista_items, "nombre_categoria": nom}
    return render(request, 'categorias.html', context)

def chaquetasM(request):
    items = Item.objects.all()
    nom = "chaqueta"
    lista_items = []
    for i in items:
        if(i.categoria=="Chaqueta" and i.genero =="F"):
            lista_items.append(i)
        
    context = {"lista_items": lista_items, "nombre_categoria": nom}
    return render(request, 'categorias.html', context)

# Vista detalle a producto, hay que pasar el item y sus productos asociados (las tallas)
def producto(request, item_id):
    if request.user:
        request.user.carrito = Carrito()
        request.user.save()
        carrito = request.user.carrito
    else:
        user = Cliente()
        user.carrito = Carrito()
        user.save()
        carrito = user.carrito
    item = get_object_or_404(Item, pk=item_id)
    lista_productos = Producto.objects.filter(item__nombre = item.nombre)

    context = {"lista_productos": lista_productos, "carrito": carrito, "item":item }
    return render(request, 'producto.html', context)

def carrito(request, producto_id):
    carrito = request.user.carrito
    producto_anyadir = Producto.get_object_or_404(pk=producto_id)
    carrito.productos.add(producto_anyadir)
    carrito.save()
    context = {"carrito": carrito}
    return render(request, 'carrito.html', context)


class ClientSignUpView(CreateView):
    model = User
    form_class = ClientSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'client'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('') 

@login_required
@staff_required
def administrar(request):    
    form = itemForm()    
    return render(request, 'administrar.html', {'form' : form})


@login_required
@staff_required
def anyadido(request):
    if request.method == "POST":
        form = itemForm(request.POST, request.FILES)
        if form.is_valid():
            nombre = form.cleaned_data.get("nombre")
            descripcion = form.cleaned_data.get("descripcion")
            categoria = form.cleaned_data.get("categoria")
            precio = form.cleaned_data.get("precio")
            color = form.cleaned_data.get("color")
            genero= form.cleaned_data.get("genero")
            imagen = form.cleaned_data.get("imagen")
        
            talla_xs1 = form.cleaned_data.get("stock_talla_xs")
            talla_s1 = form.cleaned_data.get("stock_talla_s")
            talla_m1 = form.cleaned_data.get("stock_talla_m")
            talla_l1 = form.cleaned_data.get("stock_talla_l")
            talla_xl1 = form.cleaned_data.get("stock_talla_xl")
            talla_xxl1 = form.cleaned_data.get("stock_talla_xxl")

            oferta = Oferta(1)
            o = oferta.save()
            item = Item.objects.create(nombre = nombre, descripcion = descripcion, 
                    categoria = categoria, precio = precio, oferta = oferta, fecha_insertado = date.today(), 
                    imagen = imagen, color = color, genero = genero)
            item.save()
            print(item)
            producto1 = Producto.objects.create(item = item, talla = "XS", stock = talla_xs1)
            producto2 = Producto.objects.create(item = item, talla = "S", stock = talla_s1)
            producto3 = Producto.objects.create(item = item, talla = "M", stock = talla_m1)
            producto4 = Producto.objects.create(item = item, talla = "L", stock = talla_l1)
            producto5 = Producto.objects.create(item = item, talla = "XL", stock = talla_xl1)
            producto6 = Producto.objects.create(item = item, talla = "XXL", stock = talla_xxl1)
            producto1.save()
            producto2.save()
            producto3.save()
            producto4.save()
            producto5.save()
            producto6.save()
    else:
        form = itemForm()

    return render(request, 'anyadido.html')



# @login_required
# @staff_required
# def anyadido(request):
#     form = itemForm()
#     nombre = request.POST["nombre"]
#     descripcion = request.POST["descripcion"]
#     categoria = request.POST["categoria"]
#     precio = request.POST["precio"]
#     imagen = request.POST["imagen"]
#     color = request.POST["color"]
#     genero= request.POST["genero"]
    
#     talla_xs1 = request.POST["stock_talla_xs"]
#     talla_s1 = request.POST["stock_talla_s"]
#     talla_m1 = request.POST["stock_talla_m"]
#     talla_l1 = request.POST["stock_talla_l"]
#     talla_xl1 = request.POST["stock_talla_xl"]
#     talla_xxl1 = request.POST["stock_talla_xxl"]

#     oferta = Oferta(1)
#     o = oferta.save()
#     item = Item(nombre = nombre, descripcion = descripcion, 
#             categoria = categoria, precio = precio, oferta = oferta, fecha_insertado = date.today(), 
#             imagen = imagen, color = color, genero = genero)

#     item.save()
    
#     producto1 = Producto(item = item, talla = "XS", stock = talla_xs1)
#     producto2 = Producto(item = item, talla = "S", stock = talla_s1)
#     producto3 = Producto(item = item, talla = "M", stock = talla_m1)
#     producto4 = Producto(item = item, talla = "L", stock = talla_l1)
#     producto5 = Producto(item = item, talla = "XL", stock = talla_xl1)
#     producto6 = Producto(item = item, talla = "XXL", stock = talla_xxl1)

#     producto1.save()
#     producto2.save()
#     producto3.save()
#     producto4.save()
#     producto5.save()
#     producto6.save()

#     return render(request, 'anyadido.html')

