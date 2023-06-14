from django.urls import path,include
from .views import *

urlpatterns = [
    path('', index, name="index"),
    path('indexapi/', indexapi, name="indexapi"),
    path('cart.html', cart, name="cart"),
    path('productosfavoritos', productosfavoritos, name="productosfavoritos"),
    path('agregarafavoritos/<id>/', agregarafavoritos, name="agregarafavoritos"),
    path('agregaralcarrito/<id>/', agregaralcarrito, name="agregaralcarrito"),
    path('eliminarcarrito/<id>/', eliminarcarrito, name="eliminarcarrito"),
    path('devolvercarrito/', devolvercarrito, name="devolvercarrito"),
    path('eliminar/<id>/', eliminar_producto, name="Del"),
    path('restar/<id>/', restar_producto, name="Sub"),
    path('limpiar/', limpiar_carrito, name="CLS"),
    path('agregar/<id>/', agregaralcarrito, name="Add"),
    path('api-auth/', include('rest_framework.urls')),
    path('suscripcion.html', suscripcion, name="suscripcion"),
    path('base.html', base, name="base"),
    path('perfil.html', perfil, name='perfil'),
    path('shop.html', shop, name="shop"),
    path('crudproductos.html', crudproductos, name="crudproductos"),
    path('agregarproducto/', agregarproducto, name="agregarproducto"),
    path('eliminarproducto/<id>/', eliminarproducto, name="eliminarproducto"),
    path('modificarproducto/<id>/', modificarproducto, name="modificarproducto"),
    path('crudsuscriptores.html', crudsuscriptores, name="crudsuscriptores"),
    path('agregarsuscriptor/', agregarsuscriptor, name="agregarsuscriptor"),
    path('modificarsuscriptor/<id>/', modificarsuscriptor, name="modificarsuscriptor"),
    path('eliminarsuscriptor/<id>/', eliminarsuscriptor, name="eliminarsuscriptor"),
    path('seguimiento.html', seguimiento, name='seguimiento'),
    path('historial.html', historial, name='historial'),
    
]
