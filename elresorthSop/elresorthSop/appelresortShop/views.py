from django.shortcuts import render
from django.shortcuts import get_object_or_404, get_list_or_404
from django.http import HttpResponse
from .models import User, Oferta, Item, Producto, Carrito, Cliente, Tarjeta
from .forms import ClientSignUpForm, itemForm
from django.views.generic import CreateView
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from .decorators import staff_required, client_required
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Max
from datetime import date

# Vista principal de EL RESORT SHOP con novedades y ofertas
def index(request):
    # Nos aseguramos de que exista una sesión en la que vamos a guardar datos relacionados con el carrito
    if not request.session.session_key:
        request.session.create()
    print(request.session.session_key) # La clave de sesión

    recientes = Item.objects.annotate(recentAddedItems = Max('fecha_insertado')   ) 
    items_mas_recientes = Item.objects.filter(fecha_insertado__in=[i.recentAddedItems for i in recientes])
    ofertas = Oferta.objects.all()
    hay_ofertas = False
    for o in ofertas:
        if o.descuento != 1:
            hay_ofertas = True

    context = {"ofertas": hay_ofertas, "novedades": items_mas_recientes}
    return render(request, 'index.html', context)

# Vista a artículos de un TIPO y un GÉNERO dados
def articulos(request, genero, tipo):
    items = Item.objects.all()
    lista_items = []

    if genero == 'Hombre':
        genero = 'M'
    elif genero == 'Mujer':
        genero = 'F'

    if tipo == 'Jerseis':
        tipo = 'Jerséis'
    elif tipo == 'Banadores':
        tipo = 'Bañadores y ropa de baño'
   
    for i in items:
        if(i.categoria== tipo and i.genero == genero):
            lista_items.append(i)
    
    context = {"lista_items": lista_items, "nombre_categoria": tipo}
    return render(request, 'articulos.html', context)

# Vista detalle a producto, hay que pasar el item y sus productos asociados (las tallas)
def producto(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    lista_productos = Producto.objects.filter(item__nombre = item.nombre)
    
    context = {"lista_productos": lista_productos, "item":item }
    return render(request, 'producto.html', context)

# Visualiza los productos del carrito de un cliente
@login_required #tenemos que estar logueados (y por ende registrados) 
@client_required #NO podemos ser staff
def carrito(request):
    # Sacamos el carrito del cliente
    cliente_id = request.user.id
    cliente = Cliente.objects.get(pk=cliente_id)
    carrito = cliente.carrito
    lista_productos = Producto.objects.filter(carrito__id=carrito.id)
    lista_items = []
    subtotal = 0
    for p in lista_productos:
        item = Item.objects.get(producto__id = p.id)
        print(item.nombre)
        subtotal = subtotal + item.precio
        print(subtotal)

        # lista_items.append(item)
        if item not in lista_items:
            lista_items.append(item)
        
    context = {"lista_productos": lista_productos, "lista_items":lista_items, "subtotal":subtotal}
    return render(request, 'carrito.html', context)


# Añade un producto dado y visualiza los productos del carrito de un cliente
@login_required #tenemos que estar logueados (y por ende registrados) 
@client_required #NO podemos ser staff
def carrito_anyadir(request, producto_id):

    cliente_id = request.user.id
    cliente = Cliente.objects.get(pk=cliente_id)
    carrito = cliente.carrito
    producto_anyadir = Producto.objects.get(pk=producto_id)
    carrito.productos.add(producto_anyadir)
    carrito.save()
    producto_anyadir.stock = producto_anyadir.stock-1 # Reducimos en 1 el stock de la prenda  ESTO SE DEBE HACER ANTES PARA CHEQUEAR que quedan artículos
    producto_anyadir.save()
    lista_productos = Producto.objects.filter(carrito__id=carrito.id)
    lista_items = []
    subtotal = 0
    for p in lista_productos:
        item = Item.objects.get(producto__id = p.id)
        subtotal = subtotal + item.precio
        print(subtotal)
        # lista_items.append(item)
        if item not in lista_items:
            lista_items.append(item)
        
    context = {"lista_productos": lista_productos, "lista_items":lista_items, "subtotal":subtotal}

    return render(request, 'carrito.html', context)

def compra(request):
    cliente_id = request.user.id
    cliente = Cliente.objects.get(pk=cliente_id)
    carrito = cliente.carrito
    # AQUÍ HABRÍA QUE HACER OPERATORIA PARA COMPRAR

    return render(request, 'compra.html')

# Usar variables de SESIÓN:
#--------------------------
    # # Obtener un dato de la sesión por su clave (ej. 'my_car'), generando un KeyError si la clave no existe
    # my_car = request.session['my_car']

    # # Obtener un dato de la sesión, estableciendo un valor por defecto ('mini') si el dato requerido no existe
    # my_car = request.session.get('my_car', 'mini')

    # # Asignar un dato a la sesión
    # request.session['my_car'] = 'mini'

    # # Eliminar un dato de la sesión
    # del request.session['my_car']



# Vistas y clases de login/sign_up de usuarios
#-------------------------------------

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
        return redirect('index') 

# Permite introducir nuevos items / productos en BD
@login_required
@staff_required # HAY que ser staff
def administrar(request):    
    form = itemForm()    
    return render(request, 'administrar.html', {'form' : form})

# Recoge los datos del form y los guarda en BD
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

