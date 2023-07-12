from django.shortcuts import render,redirect,get_object_or_404
from django.db.models import Sum, F , Q
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import Group
from .models import *
from .forms import *
from .carrito import *
from django.contrib.auth.decorators import login_required, permission_required,user_passes_test
import requests


# Create your views here.
def index(request):
    return render(request, 'core/index.html')
@login_required
def indexapi(request):
        respuesta = requests.get('http://127.0.0.1:8000/api/productos/')
        respuesta2 = requests.get('https://mindicador.cl/api/')

        productos = respuesta.json()
        monedas = respuesta2.json()

        data = {'listado':productos,
                'monedas':monedas,}
        return render(request,'core/indexapi.html',data)
@login_required
def cart(request):
    respuesta = requests.get('https://mindicador.cl/api/dolar').json()
    valor_usd = respuesta['serie'][0]['valor']

    items_carrito = ProductoCarrito.objects.filter(usuario=request.user)
    cantidad_total = items_carrito.aggregate(total_cantidad=Sum('cantidad'))
    cantidad_seleccionada = request.GET.get('cantidad')
    
    
    precio_total = items_carrito.annotate(precio_total=F('producto__precio') * F('cantidad')).aggregate(total_precio=Sum('precio_total'))
    if precio_total['total_precio'] is not None and valor_usd != 0:
        precio_total = round(precio_total['total_precio'] / valor_usd,2)
    else:
        precio_total = 0
    
    return render(request, 'core/cart.html', {
        'items_carrito': items_carrito,
        'cantidad_total': cantidad_total['total_cantidad'],
        'precio_total': precio_total,
        'cantidad_seleccionada': cantidad_seleccionada,
    })

@login_required
def productosfavoritos(request):

    items_carrito = Productofavorito.objects.filter(usuario=request.user)
    cantidad_total = items_carrito.aggregate(total_cantidad=Sum('cantidad'))
    cantidad_seleccionada = request.GET.get('cantidad')
    
    
    return render(request, 'core/productosfavoritos.html', {
        'items_carrito': items_carrito,
        'cantidad_total': cantidad_total['total_cantidad'],
        'cantidad_seleccionada': cantidad_seleccionada,
    })
    
@login_required
def agregarafavoritos(request, id):
    producto = Producto.objects.get(id=id)
    
    # Verificar si el stock es cero
    
    item_carrito, created = Productofavorito.objects.get_or_create(
            producto=producto,
            usuario=request.user,
            defaults={'cantidad': 1}
        )
    if not created:
            item_carrito.cantidad += 1
            item_carrito.save()
        
        # Restar la cantidad del producto al stock disponible
    Producto.objects.filter(id=id).update(stock=F('stock') - 1)
        
    total_precio = Productofavorito.objects.filter(usuario=request.user).aggregate(Sum('producto__precio'))
    request.session['total_precio'] = total_precio.get('producto__precio__sum', 0)
    
    return redirect('productosfavoritos')

@login_required
def agregaralcarrito(request, id):
    producto = Producto.objects.get(id=id)
    
    # Verificar si el stock es cero
    if producto.stock == 0:
        messages.error(request, 'Hay un producto agotado en tu carrito.')
    else:
        item_carrito, created = ProductoCarrito.objects.get_or_create(
            producto=producto,
            usuario=request.user,
            defaults={'cantidad': 1}
        )
        if not created:
            item_carrito.cantidad += 1
            item_carrito.save()
        
        # Restar la cantidad del producto al stock disponible
        Producto.objects.filter(id=id).update(stock=F('stock') - 1)
        
    total_precio = ProductoCarrito.objects.filter(usuario=request.user).aggregate(Sum('producto__precio'))
    request.session['total_precio'] = total_precio.get('producto__precio__sum', 0)
    
    return redirect('cart')

@login_required
def devolvercarrito(request):
    items_carrito = ProductoCarrito.objects.filter(usuario=request.user)
    
    # Devolver la cantidad de productos al stock disponible
    for item in items_carrito:
        Producto.objects.filter(id=item.producto.id).update(stock=F('stock') + item.cantidad)
    
    # Eliminar todos los productos del carrito
    items_carrito.delete()
    
    return redirect('cart')

@login_required
def restar_producto(request, id):
    item_carrito = ProductoCarrito.objects.get(producto__id=id, usuario=request.user)
    
    if item_carrito.cantidad > 1:
        item_carrito.cantidad -= 1
        Producto.objects.filter(id=item_carrito.producto.id).update(stock=F('stock') + 1)
        item_carrito.save()
    else:
        # Devolver la cantidad del producto al stock disponible
        Producto.objects.filter(id=item_carrito.producto.id).update(stock=F('stock') + 1)
        item_carrito.delete()

    return redirect("cart")

@login_required
def eliminar_producto(request, id):
    producto = Producto.objects.get(id=id)
    ProductoCarrito.objects.filter(producto=producto, usuario=request.user).delete()
    return redirect("cart")

@login_required
def limpiar_carrito(request):
    ProductoCarrito.objects.filter(usuario=request.user).delete()
    request.session['total_precio'] = 0
    return redirect("cart")

@login_required
def eliminarcarrito(request, id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=id)
    carrito.restar(producto)
    return redirect("cart")

def suscripcion(request):
    return render(request, 'core/suscripcion.html')

@login_required
def shop(request):
    productoAll = Producto.objects.all()
    datos = {
        'listaEmpleados': productoAll
    }
    return render(request, 'core/shop.html', datos)

@login_required
def crudproductos(request):
    productosALL = Producto.objects.all()
    datos = {
        'listaProductos' : productosALL
    }
    if not request.user.is_superuser:
    
        return redirect('index')
    else:
        return render(request,'core/crudproductos.html',datos)

@login_required
def agregarproducto(request):
    datos= {
        'form' : ProductoForm()
    }
    if request.method == 'POST':
        formulario = ProductoForm(request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            datos['mensaje'] = "Producto Guardado Correctamente"
            
    return render(request,'core/agregarproductos.html',datos)

@login_required
def modificarproducto(request, id):
    productos = Producto.objects.get(id=id)
    datos= {
        'form' : ProductoForm(instance=productos)
    }
    
    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST,instance=productos, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            datos['mensaje'] = "Producto Modificado Correctamente"
            datos['form'] = formulario
    return render(request,'core/modificarproductos.html', datos)

@login_required
def eliminarproducto(request, id):
    producto = Producto.objects.get(id=id); # OBTENEMOS UN PRODUCTO
    producto.delete()

    return redirect(to="crudproductos")


def base(request):
    return render(request, 'core/base.html')
@login_required
def historial(request):
    return render(request, 'core/historial.html')
@login_required
def seguimiento(request):
    return render(request, 'core/seguimiento.html')
def seguimientoadmin(request):
    return render(request, 'core/seguimientoadmin.html')
@login_required
def perfil(request):
    return render(request, 'core/perfil.html')

@login_required
def crudsuscriptores(request):
    suscriptoresALL = Suscriptores.objects.all()
    datos = {
        'listasuscriptores' : suscriptoresALL
    }
    if not request.user.is_superuser:
    
        return redirect('index')
    else:
        return render(request,'core/crudsuscriptores.html',datos)

@login_required
def agregarsuscriptor(request):
    datos= {
        'form' : SuscriptorForm()
    }
    if request.method == 'POST':
        formulario = SuscriptorForm(request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            datos['mensaje'] = "Suscriptor Guardado Correctamente"
            
    return render(request,'core/agregarsuscriptor.html',datos)

@login_required
def modificarsuscriptor(request, id):
    Suscriptor = Suscriptores.objects.get(id=id)
    datos= {
        'form' : SuscriptorForm(instance=Suscriptor)
    }
    
    if request.method == 'POST':
        formulario = SuscriptorForm(data=request.POST,instance=Suscriptor, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            datos['mensaje'] = "Suscriptor Modificado Correctamente"
            datos['form'] = formulario
    return render(request,'core/modificarsuscriptor.html', datos)

@login_required
def eliminarsuscriptor(request, id):
    Suscriptor = Suscriptores.objects.get(id=id); # OBTENEMOS UN PRODUCTO
    Suscriptor.delete()

    return redirect(to='crudsuscriptores')