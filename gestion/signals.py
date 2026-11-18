from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.utils import timezone

from .models import Historial, Usuario


@receiver(post_save, sender=Usuario)
def registrar_guardado_usuario(sender, instance, created, **kwargs):
    Historial.objects.create(
        tabla_afectada='Usuario',
        accion='INSERT' if created else 'UPDATE',
        fecha=timezone.now(),
    )


@receiver(post_delete, sender=Usuario)
def registrar_eliminacion_usuario(sender, instance, **kwargs):
    Historial.objects.create(
        tabla_afectada='Usuario',
        accion='DELETE',
        fecha=timezone.now(),
    )
