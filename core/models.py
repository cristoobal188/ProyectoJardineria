from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here

class TipoProductos(models.Model):
    tipo = models.CharField(max_length=40)
    def __str__(self):
        return self.tipo

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    stock = models.PositiveIntegerField()
    precio = models.PositiveIntegerField()
    tipo = models.ForeignKey(TipoProductos, on_delete=models.CASCADE)
    foto = models.ImageField(null=True, blank=True)
    fechagregado = models.DateField(null=True)
    fechamodificado = models.DateField(null=True)
    
    def __str__(self):
        return self.nombre
    
class ProductoCarrito(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    foto = models.ImageField(null=True, blank=True)
    fecha_compra = models.DateTimeField(default=timezone.now)
    
class Productofavorito(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    foto = models.ImageField(null=True, blank=True)
    fecha_compra = models.DateTimeField(default=timezone.now)

class Suscriptores(models.Model):
    nombrecompleto = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    correo = models.CharField(max_length=100)
    numerotelefono = models.PositiveIntegerField()
    contraseña = models.CharField(max_length=100)
    confirmarcontraseña = models.CharField(max_length=100)

    def __str__(self):
        return self.nombrecompleto