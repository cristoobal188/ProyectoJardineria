from django.contrib import admin
from .models import *
# Register your models here.

class ProductosAdmin(admin.ModelAdmin):
    list_display = ['nombre','precio','tipo','fechagregado','fechamodificado']
    search_fields = ['nombre']
    list_per_page = 5

class SuscripcionAdmin(admin.ModelAdmin):
    list_display = ['nombrecompleto','apellidos','correo','numerotelefono']
    search_fields = ['nombrecompleto']
    list_per_page = 5

admin.site.register(TipoProductos)
admin.site.register(Producto, ProductosAdmin)
admin.site.register(Suscriptores, SuscripcionAdmin)
admin.site.register(ProductoCarrito)


