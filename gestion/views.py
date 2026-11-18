from django.contrib import messages
from django.db.models import ProtectedError
from django.forms import Select
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .models import (
    Barberia, Barbero, Cita, Cliente, Compra, DetalleCompra, Factura,
    Favorito, Historial, Notificacion, Pago, Personalizacion, Producto,
    Resena, Servicio, Sucursal, Suscripcion, Usuario,
)

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
    return render(request, 'gestion/inicio.html', {'enlaces': enlaces})


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