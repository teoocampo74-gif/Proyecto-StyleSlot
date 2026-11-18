from django.contrib import admin

from .models import (
    Barberia, Barbero, Cita, Cliente, Compra, DetalleCompra, Factura,
    Favorito, Historial, Notificacion, Pago, Personalizacion, Producto,
    Resena, Servicio, Sucursal, Suscripcion, Usuario,
)


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'apellido', 'email', 'telefono', 'rol']
    list_filter = ['rol']
    search_fields = ['nombre', 'apellido', 'email']


@admin.register(Barberia)
class BarberiaAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'direccion', 'telefono', 'usuario']
    search_fields = ['nombre']


@admin.register(Suscripcion)
class SuscripcionAdmin(admin.ModelAdmin):
    list_display = ['id', 'plan', 'estado', 'fecha_inicio', 'fecha_fin', 'barberia']
    list_filter = ['estado']


@admin.register(Personalizacion)
class PersonalizacionAdmin(admin.ModelAdmin):
    list_display = ['id', 'barberia', 'color_primario', 'color_secundario']


@admin.register(Barbero)
class BarberoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'especialidad', 'comision', 'barberia']
    list_filter = ['barberia']
    search_fields = ['nombre', 'especialidad']


@admin.register(Sucursal)
class SucursalAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'direccion', 'barberia']


@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'precio', 'duracion', 'barberia']
    list_filter = ['barberia']
    search_fields = ['nombre']


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'precio', 'stock', 'barberia']
    list_filter = ['barberia']
    search_fields = ['nombre']


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'apellido', 'email', 'telefono']
    search_fields = ['nombre', 'apellido', 'email']


@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ['id', 'fecha', 'hora', 'estado', 'cliente', 'barbero', 'servicio']
    list_filter = ['estado', 'fecha', 'barbero']
    list_editable = ['estado']


@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ['id', 'fecha', 'total', 'cliente', 'barberia']
    list_filter = ['fecha']


@admin.register(DetalleCompra)
class DetalleCompraAdmin(admin.ModelAdmin):
    list_display = ['id', 'compra', 'producto', 'cantidad', 'subtotal']


@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ['id', 'fecha', 'total', 'impuesto', 'estado', 'cita', 'cliente']
    list_filter = ['estado']


@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ['id', 'monto', 'fecha', 'metodo_pago', 'estado', 'factura']
    list_filter = ['estado', 'metodo_pago']


@admin.register(Resena)
class ResenaAdmin(admin.ModelAdmin):
    list_display = ['id', 'calificacion', 'fecha', 'cliente', 'barberia']
    list_filter = ['calificacion']


@admin.register(Favorito)
class FavoritoAdmin(admin.ModelAdmin):
    list_display = ['id', 'cliente', 'barberia']


@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    list_display = ['id', 'tipo', 'fecha', 'leida', 'usuario']
    list_filter = ['tipo']


@admin.register(Historial)
class HistorialAdmin(admin.ModelAdmin):
    list_display = ['id', 'tabla_afectada', 'accion', 'fecha']
    list_filter = ['tabla_afectada', 'accion']
