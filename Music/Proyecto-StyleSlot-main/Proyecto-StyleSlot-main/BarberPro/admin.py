from django.contrib import admin
from .models import *

admin.site.site_header = 'BarberPro Admin'
admin.site.site_title = 'BarberPro Admin'
admin.site.index_title = 'Panel de administración'
admin.site.register(Barberias)
admin.site.register(Usuarios)
admin.site.register(Clientes)
admin.site.register(Barberos)
admin.site.register(Servicios)
admin.site.register(Citas)
admin.site.register(Compras)
admin.site.register(Facturas)
admin.site.register(Favoritos)
admin.site.register(Notificaciones)
admin.site.register(Pagos)
admin.site.register(Personalizaciones)
admin.site.register(Productos)
admin.site.register(Resenas)
admin.site.register(Suscripciones)