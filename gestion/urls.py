from django.urls import path

from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('barberpro/', views.barberpro, name='barberpro'),
    path('cerrar-sesion/', views.cerrar_sesion, name='cerrar_sesion'),
]

for modelo in views.MODELOS:
    base = views.nombre(modelo)
    vistas = views.crear_vistas(modelo)
    urlpatterns += [
        path(f'{base}/', vistas['list'].as_view(), name=f'{base}_list'),
        path(f'{base}/nuevo/', vistas['create'].as_view(), name=f'{base}_create'),
        path(f'{base}/<int:pk>/editar/', vistas['update'].as_view(), name=f'{base}_update'),
        path(f'{base}/<int:pk>/eliminar/', vistas['delete'].as_view(), name=f'{base}_delete'),
    ]
