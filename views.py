import logging
from smtplib import SMTPException

from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import ProtectedError
from django.db import transaction
from django.forms import Select
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import RegistroForm
from .models import (
    Barberia, Barbero, Cita, Cliente, Compra, DetalleCompra, Factura,
    Favorito, Historial, Notificacion, Pago, Personalizacion, Producto,
    Resena, Servicio, Sucursal, Suscripcion, Usuario,
)

logger = logging.getLogger(__name__)

MODELOS = [
    Usuario, Barberia, Suscripcion, Personalizacion, Barbero, Sucursal,
    Servicio, Producto, Cliente, Cita, Compra, DetalleCompra, Factura,
    Pago, Resena, Favorito, Notificacion, Historial,
]


def nombre(modelo):
    return modelo._meta.model_name


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


class ListaBase(ListView):
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


class FormularioBase:
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


class EliminarBase(DeleteView):
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
def barberpro(request):
    return render(request, 'gestion/barberpro.html')


def registrar(request):
    form = RegistroForm(request.POST if request.method == 'POST' else None)
    if request.method == 'POST' and form.is_valid():
        if not (
            settings.EMAIL_HOST_USER
            and settings.EMAIL_HOST_PASSWORD
            and settings.REGISTRATION_NOTIFICATION_EMAIL
            and settings.DEFAULT_FROM_EMAIL
        ):
            form.add_error(
                None,
                'El registro no está disponible hasta configurar el correo de notificaciones.',
            )
        else:
            try:
                with transaction.atomic():
                    user = form.save()
                    sent_count = send_mail(
                        subject='Nuevo registro en StyleSlot',
                        message=(
                            'Se creó una cuenta nueva en StyleSlot.\n\n'
                            f'Nombre: {user.first_name}\n'
                            f'Usuario: {user.username}\n'
                            f'Correo: {user.email}\n'
                            f'Teléfono: {form.cleaned_data["telefono"]}\n\n'
                            'La cuenta está activa. La contraseña no se envía por correo.'
                        ),
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[settings.REGISTRATION_NOTIFICATION_EMAIL],
                        fail_silently=False,
                    )
                    if sent_count != 1:
                        raise SMTPException('No se pudo enviar el aviso de registro.')
            except (OSError, SMTPException):
                logger.exception('No se pudo enviar el aviso de nuevo registro.')
                form.add_error(
                    None,
                    'No se pudo enviar el aviso y el registro no se guardó. '
                    'Inténtalo más tarde o contacta al administrador.',
                )
            else:
                messages.success(request, 'Tu cuenta ya está activa. Inicia sesión para continuar.')
                return redirect('login')

    return render(request, 'gestion/registro.html', {'form': form})