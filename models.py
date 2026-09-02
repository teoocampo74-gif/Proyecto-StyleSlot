from django.db import models

# Create your models here.
from django.core.exceptions import ValidationError



class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    mail = models.EmailField(max_length=254)
    telefono = models.CharField(max_length=15, null=True, blank=True)
    fecha_registro = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Profesional(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=100)  # ej: Barbero, Colorista, Estilista
    correo = models.EmailField(max_length=100, unique=True)
    tel = models.CharField(max_length=15, null=True, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.especialidad}"


class Servicio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    duracion_minutos = models.PositiveIntegerField(default=30)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    profesionales = models.ManyToManyField(Profesional, related_name="servicios")

    ESTADOS = (
        ("Inactivo", "INACTIVO"),
        ("Activo", "ACTIVO"),
    )
    estado = models.CharField(max_length=10, choices=ESTADOS, default="Activo")

    def __str__(self):
        return f"{self.nombre} - {self.estado}"


class Turno(models.Model):

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="turnos")
    profesional = models.ForeignKey(Profesional, on_delete=models.CASCADE, related_name="turnos")
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name="turnos")
    fecha = models.DateField()
    hora_inicio = models.TimeField()

    ESTADOS_TURNO = (
        ("Pendiente", "PENDIENTE"),
        ("Confirmado", "CONFIRMADO"),
        ("Cancelado", "CANCELADO"),
        ("Completado", "COMPLETADO"),
    )
    estado = models.CharField(max_length=10, choices=ESTADOS_TURNO, default="Pendiente")
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Un profesional no puede tener dos turnos activos a la misma hora
        unique_together = ("profesional", "fecha", "hora_inicio")
        ordering = ["fecha", "hora_inicio"]

    def clean(self):
        if self.profesional_id and self.servicio_id:
            if not self.servicio.profesionales.filter(pk=self.profesional_id).exists():
                raise ValidationError(
                    "Ese profesional no presta el servicio seleccionado."
                )

    def __str__(self):
        return f"{self.cliente} con {self.profesional} - {self.fecha} {self.hora_inicio} ({self.estado})"
