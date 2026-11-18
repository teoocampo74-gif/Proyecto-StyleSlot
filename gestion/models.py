from django.contrib.auth.hashers import make_password, identify_hasher
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Usuario(models.Model):
    ROLES = (
        ('Admin', 'Admin'),
        ('Barbero', 'Barbero'),
        ('Cliente', 'Cliente'),
    )
    id = models.AutoField(primary_key=True, db_column='idUsuario')
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    rol = models.CharField(max_length=10, choices=ROLES)
    direccion = models.CharField(max_length=40)

    class Meta:
        db_table = 'usuario'

    def save(self, *args, **kwargs):
        try:
            identify_hasher(self.password)
        except ValueError:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.nombre} {self.apellido} ({self.rol})'


class Barberia(models.Model):
    id = models.AutoField(primary_key=True, db_column='idBarberia')
    nombre = models.CharField(max_length=255)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=50)
    latitud = models.CharField(max_length=200)
    longitud = models.CharField(max_length=234)
    usuario = models.ForeignKey(Usuario, db_column='idUsuario', null=True, blank=True, on_delete=models.PROTECT)

    class Meta:
        db_table = 'barberia'
        verbose_name_plural = 'barberias'

    def __str__(self):
        return self.nombre


class Suscripcion(models.Model):
    ESTADOS = (
        ('Activa', 'Activa'),
        ('Inactiva', 'Inactiva'),
    )
    id = models.AutoField(primary_key=True, db_column='idSuscripcion')
    plan = models.CharField(max_length=150)
    estado = models.CharField(max_length=10, choices=ESTADOS)
    fecha_inicio = models.DateField(db_column='Fechainicio')
    fecha_fin = models.DateField(db_column='FechaFin')
    barberia = models.ForeignKey(Barberia, db_column='idBarberia', null=True, blank=True, on_delete=models.PROTECT)

    class Meta:
        db_table = 'suscripcion'
        verbose_name_plural = 'suscripciones'

    def clean(self):
        if self.fecha_inicio and self.fecha_fin and self.fecha_fin < self.fecha_inicio:
            raise ValidationError('La fecha fin no puede ser anterior a la fecha de inicio.')

    def __str__(self):
        return f'{self.plan} - {self.estado}'


class Personalizacion(models.Model):
    id = models.AutoField(primary_key=True, db_column='idPersonal')
    logo_url = models.CharField(max_length=255, db_column='logoURL')
    color_primario = models.CharField(max_length=40, db_column='colorPrimario')
    color_secundario = models.CharField(max_length=20, db_column='colorSecundario')
    splash_url = models.CharField(max_length=255, db_column='splashURL')
    barberia = models.ForeignKey(Barberia, db_column='idBarberia', null=True, blank=True, on_delete=models.PROTECT)

    class Meta:
        db_table = 'personalizacion'
        verbose_name_plural = 'personalizaciones'

    def __str__(self):
        return f'Personalizacion {self.id}'


class Barbero(models.Model):
    id = models.AutoField(primary_key=True, db_column='idBarbero')
    nombre = models.CharField(max_length=255)
    especialidad = models.CharField(max_length=100)
    comision = models.DecimalField(max_digits=12, decimal_places=5, db_column='comicion')
    barberia = models.ForeignKey(Barberia, db_column='idBarberia', null=True, blank=True, on_delete=models.PROTECT)
    usuario = models.ForeignKey(Usuario, db_column='idUsuario', null=True, blank=True, on_delete=models.PROTECT)

    class Meta:
        db_table = 'barbero'
        verbose_name_plural = 'barberos'

    def __str__(self):
        return f'{self.nombre} - {self.especialidad}'


class Sucursal(models.Model):
    id = models.AutoField(primary_key=True, db_column='idSucursal')
    nombre = models.CharField(max_length=255)
    direccion = models.CharField(max_length=100)
    barberia = models.ForeignKey(Barberia, db_column='idBarberia', null=True, blank=True, on_delete=models.PROTECT)

    class Meta:
        db_table = 'sucursal'
        verbose_name_plural = 'sucursales'

    def __str__(self):
        return self.nombre


class Servicio(models.Model):
    id = models.AutoField(primary_key=True, db_column='idServicio')
    nombre = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=100, db_column='descrpcion')
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    duracion = models.IntegerField(validators=[MinValueValidator(1)])
    barberia = models.ForeignKey(Barberia, db_column='idBarberia', null=True, blank=True, on_delete=models.PROTECT)

    class Meta:
        db_table = 'servicio'
        verbose_name_plural = 'servicios'

    def __str__(self):
        return f'{self.nombre} ({self.duracion} min)'


class Producto(models.Model):
    id = models.AutoField(primary_key=True, db_column='idProducto')
    nombre = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255, db_column='descrpción')
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.IntegerField(validators=[MinValueValidator(0)])
    barberia = models.ForeignKey(Barberia, db_column='idBarberia', null=True, blank=True, on_delete=models.PROTECT)

    class Meta:
        db_table = 'producto'
        verbose_name_plural = 'productos'

    def __str__(self):
        return self.nombre


class Cliente(models.Model):
    id = models.AutoField(primary_key=True, db_column='idCliente')
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    telefono = models.CharField(max_length=255)
    direccion = models.CharField(max_length=245)
    usuario = models.ForeignKey(Usuario, db_column='idUsuario', null=True, blank=True, on_delete=models.PROTECT)

    class Meta:
        db_table = 'cliente'
        verbose_name_plural = 'clientes'

    def __str__(self):
        return f'{self.nombre} {self.apellido}'


class Cita(models.Model):
    ESTADOS = (
        ('Pendiente', 'Pendiente'),
        ('Confirmada', 'Confirmada'),
        ('Finalizada', 'Finalizada'),
    )
    id = models.AutoField(primary_key=True, db_column='idCita')
    fecha = models.DateField()
    hora = models.TimeField()
    estado = models.CharField(max_length=10, choices=ESTADOS, default='Pendiente')
    cliente = models.ForeignKey(Cliente, db_column='idCliente', null=True, blank=True, on_delete=models.PROTECT)
    barbero = models.ForeignKey(Barbero, db_column='idBarbero', null=True, blank=True, on_delete=models.PROTECT)
    servicio = models.ForeignKey(Servicio, db_column='idServicio', null=True, blank=True, on_delete=models.PROTECT)

    class Meta:
        db_table = 'cita'
        verbose_name_plural = 'citas'
        ordering = ['fecha', 'hora']

    def clean(self):
        if self.barbero_id and self.fecha and self.hora:
            choque = Cita.objects.filter(barbero_id=self.barbero_id, fecha=self.fecha, hora=self.hora).exclude(pk=self.pk)
            if choque.exists():
                raise ValidationError('El barbero ya tiene una cita en esa fecha y hora.')

    def __str__(self):
        return f'Cita {self.id} - {self.fecha} {self.hora}'


class Compra(models.Model):
    id = models.AutoField(primary_key=True, db_column='idCompra')
    fecha = models.DateField()
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cliente = models.ForeignKey(Cliente, db_column='idCliente', null=True, blank=True, on_delete=models.PROTECT)
    barberia = models.ForeignKey(Barberia, db_column='idBarberia', null=True, blank=True, on_delete=models.PROTECT)

    class Meta:
        db_table = 'compra'
        verbose_name_plural = 'compras'

    def __str__(self):
        return f'Compra {self.id} - {self.fecha}'


class DetalleCompra(models.Model):
    id = models.AutoField(primary_key=True, db_column='idDetalle')
    cantidad = models.IntegerField(db_column='catidad', validators=[MinValueValidator(1)])
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    compra = models.ForeignKey(Compra, db_column='idCompra', null=True, blank=True, on_delete=models.PROTECT)
    producto = models.ForeignKey(Producto, db_column='idProducto', null=True, blank=True, on_delete=models.PROTECT)

    class Meta:
        db_table = 'detallecompra'
        verbose_name = 'detalle de compra'
        verbose_name_plural = 'detalles de compra'

    def __str__(self):
        return f'Detalle {self.id}'


class Factura(models.Model):
    ESTADOS = (
        ('Pagada', 'Pagada'),
        ('Pendiente', 'Pendiente'),
    )
    id = models.AutoField(primary_key=True, db_column='idFactura')
    fecha = models.DateField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    impuesto = models.CharField(max_length=255)
    estado = models.CharField(max_length=10, choices=ESTADOS)
    cita = models.ForeignKey(Cita, db_column='idCita', null=True, blank=True, on_delete=models.PROTECT)
    cliente = models.ForeignKey(Cliente, db_column='idCliente', null=True, blank=True, on_delete=models.PROTECT)
    barberia = models.ForeignKey(Barberia, db_column='idBarberia', null=True, blank=True, on_delete=models.PROTECT)

    class Meta:
        db_table = 'factura'
        verbose_name_plural = 'facturas'

    def __str__(self):
        return f'Factura {self.id} - {self.estado}'


class Pago(models.Model):
    ESTADOS = (
        ('Completado', 'Completado'),
        ('Pendiente', 'Pendiente'),
    )
    id = models.AutoField(primary_key=True, db_column='idPago')
    monto = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    fecha = models.DateField()
    metodo_pago = models.CharField(max_length=255, db_column='metodoPago')
    estado = models.CharField(max_length=10, choices=ESTADOS)
    factura = models.ForeignKey(Factura, db_column='idFactura', null=True, blank=True, on_delete=models.PROTECT)

    class Meta:
        db_table = 'pago'
        verbose_name_plural = 'pagos'

    def __str__(self):
        return f'Pago {self.id} - {self.estado}'


class Resena(models.Model):
    id = models.AutoField(primary_key=True, db_column='idResena')
    calificacion = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comentario = models.TextField()
    fecha = models.DateField()
    cliente = models.ForeignKey(Cliente, db_column='idCliente', null=True, blank=True, on_delete=models.PROTECT)
    barberia = models.ForeignKey(Barberia, db_column='idBarberia', null=True, blank=True, on_delete=models.PROTECT)

    class Meta:
        db_table = 'resena'
        verbose_name = 'reseña'
        verbose_name_plural = 'reseñas'

    def __str__(self):
        return f'Reseña {self.id} - {self.calificacion}/5'


class Favorito(models.Model):
    id = models.AutoField(primary_key=True, db_column='idFavorito')
    cliente = models.ForeignKey(Cliente, db_column='idCliente', null=True, blank=True, on_delete=models.PROTECT)
    barberia = models.ForeignKey(Barberia, db_column='idBarberia', null=True, blank=True, on_delete=models.PROTECT)

    class Meta:
        db_table = 'favorito'
        verbose_name_plural = 'favoritos'

    def __str__(self):
        return f'Favorito {self.id}'


class Notificacion(models.Model):
    id = models.AutoField(primary_key=True, db_column='idNotif')
    tipo = models.CharField(max_length=255)
    mensaje = models.TextField()
    fecha = models.DateField()
    leida = models.CharField(max_length=255)
    usuario = models.ForeignKey(Usuario, db_column='idUsuario', null=True, blank=True, on_delete=models.PROTECT)

    class Meta:
        db_table = 'notificacion'
        verbose_name = 'notificación'
        verbose_name_plural = 'notificaciones'

    def __str__(self):
        return f'{self.tipo} - {self.fecha}'


class Historial(models.Model):
    id = models.AutoField(primary_key=True, db_column='idHistorial')
    tabla_afectada = models.CharField(max_length=50, null=True, blank=True, db_column='tablaAfectada')
    accion = models.CharField(max_length=50, null=True, blank=True)
    fecha = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'historial'
        verbose_name_plural = 'historial'
        ordering = ['-fecha']

    def __str__(self):
        return f'{self.tabla_afectada} - {self.accion}'
