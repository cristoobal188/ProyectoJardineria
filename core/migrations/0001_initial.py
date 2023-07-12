# Generated by Django 4.2.2 on 2023-06-26 01:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('stock', models.PositiveIntegerField()),
                ('precio', models.PositiveIntegerField()),
                ('foto', models.ImageField(blank=True, null=True, upload_to='')),
                ('fechagregado', models.DateField(null=True)),
                ('fechamodificado', models.DateField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Suscriptores',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombrecompleto', models.CharField(max_length=100)),
                ('apellidos', models.CharField(max_length=100)),
                ('correo', models.CharField(max_length=100)),
                ('numerotelefono', models.PositiveIntegerField()),
                ('contraseña', models.CharField(max_length=100)),
                ('confirmarcontraseña', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='TipoProductos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Productofavorito',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField()),
                ('foto', models.ImageField(blank=True, null=True, upload_to='')),
                ('fecha_compra', models.DateTimeField(default=django.utils.timezone.now)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.producto')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProductoCarrito',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField()),
                ('foto', models.ImageField(blank=True, null=True, upload_to='')),
                ('fecha_compra', models.DateTimeField(default=django.utils.timezone.now)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.producto')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='producto',
            name='tipo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.tipoproductos'),
        ),
    ]
