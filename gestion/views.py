from datetime import date, datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import ProtectedError
from django.forms import Select
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .models import (
    Barberia, Barbero, Cita, Cliente, Compra, DetalleCompra, Factura,
    Favorito, Historial, Notificacion, Pago, Personalizacion, Producto,
    Resena, Servicio, Suscripcion, Usuario, Sucursal,
)

MODELOS = [
    Usuario, Barberia, Suscripcion, Personalizacion, Barbero, Sucursal,
    Servicio, Producto, Cliente, Cita, Compra, DetalleCompra, Factura,
    Pago, Resena, Favorito, Notificacion, Historial,
]


def nombre(modelo):
    return modelo._meta.model_name


@login_required(login_url='login_publico')
def inicio(request):
    enlaces = [
        (m._meta.verbose_name_plural.capitalize(), f'{nombre(m)}_list')
        for m in MODELOS
    ]
    return render(request, 'gestion/inicio.html', {
        'enlaces': enlaces,
        'citas_total': Cita.objects.count(),
        'clientes_total': Cliente.objects.count(),
        'barberos_total': Barbero.objects.count(),
        'productos_total': Producto.objects.count(),
    })


class ListaBase(LoginRequiredMixin, ListView):
    login_url = 'login_publico'
    template_name = 'gestion/listar.html'
    paginate_by = 15

    def get_queryset(self):
        consulta = super().get_queryset()
        if consulta.ordered:
            return consulta
        return consulta.order_by('pk')

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        modelo = self.model
        campos = modelo._meta.fields
        filas = []
        for objeto in contexto['object_list']:
            celdas = []
            for campo in campos:
                if campo.choices:
                    valor = getattr(objeto, f'get_{campo.name}_display')()
                else:
                    valor = getattr(objeto, campo.name)
                celdas.append('' if valor is None else valor)
            filas.append({'pk': objeto.pk, 'celdas': celdas})
        contexto.update({
            'titulo': modelo._meta.verbose_name_plural.capitalize(),
            'columnas': [c.verbose_name.capitalize() for c in campos],
            'filas': filas,
            'prefijo': nombre(modelo),
            'solo_lectura': modelo is Historial,
        })
        return contexto


class FormularioBase(LoginRequiredMixin):
    login_url = 'login_publico'
    template_name = 'gestion/formulario.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy(f'{nombre(self.model)}_list')

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['titulo'] = self.model._meta.verbose_name.capitalize()
        contexto['prefijo'] = nombre(self.model)
        return contexto

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for campo in form.fields.values():
            clase = 'form-select' if isinstance(campo.widget, Select) else 'form-control'
            campo.widget.attrs['class'] = clase
        return form

    def form_valid(self, form):
        messages.success(self.request, 'Registro guardado correctamente.')
        return super().form_valid(form)


class EliminarBase(LoginRequiredMixin, DeleteView):
    login_url = 'login_publico'
    template_name = 'gestion/eliminar.html'

    def get_success_url(self):
        return reverse_lazy(f'{nombre(self.model)}_list')

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['prefijo'] = nombre(self.model)
        return contexto

    def post(self, request, *args, **kwargs):
        try:
            respuesta = super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, 'No se puede eliminar: el registro está relacionado con otros datos.')
            return redirect(self.get_success_url())
        messages.success(request, 'Registro eliminado correctamente.')
        return respuesta


def crear_vistas(modelo):
    return {
        'list': type(f'{modelo.__name__}Lista', (ListaBase,), {'model': modelo}),
        'create': type(f'{modelo.__name__}Crear', (FormularioBase, CreateView), {'model': modelo}),
        'update': type(f'{modelo.__name__}Editar', (FormularioBase, UpdateView), {'model': modelo}),
        'delete': type(f'{modelo.__name__}Eliminar', (EliminarBase,), {'model': modelo}),
    }


def cerrar_sesion(request):
    logout(request)
    return redirect('/barberpro/login/')


def login_publico(request):
    if request.user.is_authenticated:
        return redirect('inicio')

    if request.method == 'POST':
        identificador = request.POST.get('usuario', '').strip()
        password = request.POST.get('password', '')

        usuario = authenticate(request, username=identificador, password=password)
        if usuario is None:
            usuario_auth = get_user_model().objects.filter(email__iexact=identificador).first()
            if usuario_auth:
                usuario = authenticate(request, username=usuario_auth.username, password=password)

        if usuario is not None:
            login(request, usuario)
            destino = request.POST.get('next') or request.GET.get('next')
            if destino and destino.startswith('/') and not destino.startswith('//'):
                return redirect(destino)
            return redirect('inicio')

        return render(request, 'gestion/login.html', {
            'error_login': 'Usuario o contraseña incorrectos.',
        }, status=401)

    return render(request, 'gestion/login.html')


def barberpro(request):
    barberos = Barbero.objects.select_related('usuario').all()
    servicios = Servicio.objects.all()

    if request.method == 'POST' and request.POST.get('accion') == 'login':
        identificador = request.POST.get('usuario', '').strip()
        password = request.POST.get('password', '')

        usuario = authenticate(request, username=identificador, password=password)
        if usuario is None:
            usuario_auth = get_user_model().objects.filter(email__iexact=identificador).first()
            if usuario_auth:
                usuario = authenticate(request, username=usuario_auth.username, password=password)

        if usuario is not None:
            login(request, usuario)
            return render(request, 'gestion/barberpro.html', {
                'barberos': barberos,
                'servicios': servicios,
                'min_fecha': date.today().isoformat(),
                'login_exitoso': True,
                'sesion_activa': True,
            })

        return render(request, 'gestion/barberpro.html', {
            'barberos': barberos,
            'servicios': servicios,
            'min_fecha': date.today().isoformat(),
            'error_login': 'Usuario o contraseña incorrectos.',
        }, status=401)

    if request.method == 'POST':
        nombre_completo = request.POST.get('nombre', '').strip()
        email = request.POST.get('email', '').strip()
        telefono = request.POST.get('telefono', '').strip()
        barbero_id = request.POST.get('barbero')
        servicio_id = request.POST.get('servicio')
        fecha_texto = request.POST.get('fecha')
        hora_texto = request.POST.get('hora')

        try:
            fecha_cita = date.fromisoformat(fecha_texto)
            hora_cita = datetime.strptime(hora_texto, '%H:%M').time()
            barbero = Barbero.objects.get(pk=barbero_id)
            servicio = Servicio.objects.get(pk=servicio_id)
        except (TypeError, ValueError, Barbero.DoesNotExist, Servicio.DoesNotExist):
            return render(request, 'gestion/barberpro.html', {
                'barberos': barberos,
                'servicios': servicios,
                'error_reserva': 'Revisa los datos de la reserva.',
                'min_fecha': date.today().isoformat(),
            }, status=400)

        if fecha_cita < date.today():
            return render(request, 'gestion/barberpro.html', {
                'barberos': barberos,
                'servicios': servicios,
                'error_reserva': 'La fecha no puede estar en el pasado.',
                'min_fecha': date.today().isoformat(),
            }, status=400)

        if not nombre_completo or not email:
            return render(request, 'gestion/barberpro.html', {
                'barberos': barberos,
                'servicios': servicios,
                'error_reserva': 'El nombre y el correo son obligatorios.',
                'min_fecha': date.today().isoformat(),
            }, status=400)

        choque = Cita.objects.filter(
            barbero=barbero,
            fecha=fecha_cita,
            hora=hora_cita,
        ).exclude(estado='Finalizada').exists()
        if choque:
            return render(request, 'gestion/barberpro.html', {
                'barberos': barberos,
                'servicios': servicios,
                'error_reserva': 'Ese horario ya está ocupado. Selecciona otro.',
                'min_fecha': date.today().isoformat(),
            }, status=409)

        partes = nombre_completo.split(maxsplit=1)
        nombre_cliente = partes[0]
        apellido_cliente = partes[1] if len(partes) > 1 else ''
        cliente, creado = Cliente.objects.get_or_create(
            email=email,
            defaults={
                'nombre': nombre_cliente,
                'apellido': apellido_cliente,
                'telefono': telefono,
                'direccion': '',
            },
        )

        Cita.objects.create(
            fecha=fecha_cita,
            hora=hora_cita,
            estado='Pendiente',
            cliente=cliente,
            barbero=barbero,
            servicio=servicio,
        )

        return render(request, 'gestion/barberpro.html', {
            'barberos': barberos,
            'servicios': servicios,
            'exito_reserva': 'Tu cita quedó registrada como pendiente.',
            'min_fecha': date.today().isoformat(),
        })

    return render(request, 'gestion/barberpro.html', {
        'barberos': barberos,
        'servicios': servicios,
        'min_fecha': date.today().isoformat(),
        'sesion_activa': request.user.is_authenticated,
    })