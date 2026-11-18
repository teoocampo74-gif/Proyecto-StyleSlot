from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('', views.barberpro, name='inicio'),
    path('panel/', views.inicio, name='panel'),
    path('barberpro/', views.barberpro, name='barberpro'),
    path(
        'login/',
        LoginView.as_view(template_name='gestion/login.html'),
        name='login',
    ),
    path('registro/', views.registrar, name='registro'),
    path('logout/', LogoutView.as_view(), name='logout'),
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
