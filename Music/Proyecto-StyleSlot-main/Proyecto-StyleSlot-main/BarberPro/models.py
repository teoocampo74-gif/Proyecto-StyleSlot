from django.db import models

# Create your models here.


class Barberias(models.Model):
    idbarberia = models.AutoField(db_column='idBarberia', primary_key=True)
    nombre = models.CharField(max_length=255)
    direccion = models.CharField(unique=True, max_length=255)
    telefono = models.CharField(max_length=255, blank=True, null=True)
    latitud = models.DecimalField(max_digits=10, decimal_places=7)
    longitud = models.DecimalField(max_digits=10, decimal_places=7)

    class Meta:
        managed = False
        db_table = 'Barberias'

    def __str__(self):
        return self.nombre


class Usuarios(models.Model):
    idusuario = models.AutoField(db_column='idUsuario', primary_key=True)
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    email = models.CharField(unique=True, max_length=255)
    telefono = models.PositiveIntegerField(unique=True)
    direccion = models.CharField(max_length=255)
    clave = models.CharField(unique=True, max_length=255, blank=True, null=True)
    rol = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'Usuarios'

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.rol})"


class Clientes(models.Model):
    idcliente = models.AutoField(db_column='idCliente', primary_key=True)
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    email = models.CharField(unique=True, max_length=255)
    telefono = models.PositiveIntegerField()
    direccion = models.CharField(max_length=255)
    idusuario = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='idUsuario', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Clientes'

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Barberos(models.Model):
    idbarbero = models.AutoField(db_column='idBarbero', primary_key=True)
    nombre = models.CharField(max_length=255)
    especialidad = models.CharField(max_length=255)
    comision = models.DecimalField(max_digits=10, decimal_places=2)
    idusuario = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='idUsuario', blank=True, null=True)
    idbarberia = models.ForeignKey(Barberias, models.DO_NOTHING, db_column='idBarberia', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Barberos'

    def __str__(self):
        return self.nombre


class Servicios(models.Model):
    idservicio = models.AutoField(db_column='idServicio', primary_key=True)
    duracion = models.TimeField(blank=True, null=True)
    precio = models.PositiveIntegerField()
    nombre = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255)
    idbarberia = models.ForeignKey(Barberias, models.DO_NOTHING, db_column='idBarberia', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Servicios'

    def __str__(self):
        return self.nombre


class Citas(models.Model):
    idcita = models.AutoField(db_column='idCita', primary_key=True)
    fecha = models.DateField(blank=True, null=True)
    hora = models.DateTimeField()
    estado = models.CharField(max_length=20, blank=True, null=True)
    idcliente = models.ForeignKey(Clientes, models.DO_NOTHING, db_column='idCliente', blank=True, null=True)
    idbarbero = models.ForeignKey(Barberos, models.DO_NOTHING, db_column='idBarbero', blank=True, null=True)
    idservicio = models.ForeignKey(Servicios, models.DO_NOTHING, db_column='idServicio', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Citas'


class Compras(models.Model):
    idcompra = models.AutoField(db_column='idCompra', primary_key=True)
    fecha = models.DateField(db_column='Fecha', blank=True, null=True)
    total = models.PositiveIntegerField()
    idcliente = models.ForeignKey(Clientes, models.DO_NOTHING, db_column='idCliente', blank=True, null=True)
    idbarberia = models.ForeignKey(Barberias, models.DO_NOTHING, db_column='idBarberia', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Compras'


class Detalles(models.Model):
    iddetalle = models.AutoField(db_column='idDetalle', primary_key=True)
    subtotal = models.PositiveIntegerField(db_column='subTotal')
    cantidad = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'Detalles'


class Facturas(models.Model):
    idfactura = models.AutoField(db_column='idFactura', primary_key=True)
    estado = models.CharField(max_length=20, blank=True, null=True)
    fecha = models.DateField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    impuesto = models.IntegerField(blank=True, null=True)
    idcita = models.ForeignKey(Citas, models.DO_NOTHING, db_column='idCita', blank=True, null=True)
    idcliente = models.ForeignKey(Clientes, models.DO_NOTHING, db_column='idCliente', blank=True, null=True)
    idbarberia = models.ForeignKey(Barberias, models.DO_NOTHING, db_column='idBarberia', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Facturas'


class Favoritos(models.Model):
    idfavoritos = models.AutoField(db_column='idFavoritos', primary_key=True)
    idbarberia = models.ForeignKey(Barberias, models.DO_NOTHING, db_column='idBarberia', blank=True, null=True)
    idcliente = models.ForeignKey(Clientes, models.DO_NOTHING, db_column='idCliente', blank=True, null=True)

    class Meta:
        managed = False
        db_table='Favoritos'


class Notificaciones(models.Model):
    idnotificacion = models.AutoField(db_column='idNotificacion', primary_key=True)
    tipo = models.CharField(max_length=20, blank=True, null=True)
    mensaje = models.CharField(max_length=255)
    fecha = models.DateField(blank=True, null=True)
    leida = models.IntegerField()
    idusuario = models.ForeignKey(Usuarios, models.DO_NOTHING, db_column='idUsuario', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Notificaciones'


class Pagos(models.Model):
    idpago = models.AutoField(db_column='idPago', primary_key=True)
    monto = models.PositiveIntegerField(blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    metodopago = models.CharField(max_length=20, db_column='metodoPago', blank=True, null=True)
    estado = models.CharField(max_length=20, blank=True, null=True)
    idfactura = models.ForeignKey(Facturas, models.DO_NOTHING, db_column='idFactura', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Pagos'


class Personalizaciones(models.Model):
    idpersonalizacion = models.AutoField(db_column='idPersonalizacion', primary_key=True)
    logourl = models.CharField(max_length=255, db_column='logoUrl')
    colorprimario = models.CharField(max_length=255, db_column='colorPrimario')
    colorsecundario = models.CharField(max_length=255, db_column='colorSecundario')
    splashurl = models.CharField(max_length=255, db_column='splashUrl')
    idbarberia = models.ForeignKey(Barberias, models.DO_NOTHING, db_column='idBarberia', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Personalizaciones'


class Productos(models.Model):
    idproducto = models.AutoField(db_column='idProducto', primary_key=True)
    nombre = models.CharField(unique=True, max_length=255)
    descripcion = models.CharField(max_length=255)
    stock = models.IntegerField()
    precio = models.IntegerField()
    idbarberia = models.ForeignKey(Barberias, models.DO_NOTHING, db_column='idBarberia', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Productos'

    def __str__(self):
        return self.nombre


class Resenas(models.Model):
    idresena = models.AutoField(db_column='idResena', primary_key=True)
    calificacion = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    comentario = models.CharField(max_length=255, blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    idbarberia = models.ForeignKey(Barberias, models.DO_NOTHING, db_column='idBarberia', blank=True, null=True)
    idcliente = models.ForeignKey(Clientes, models.DO_NOTHING, db_column='idCliente', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Resenas'


class Suscripciones(models.Model):
    idsuscripcion = models.AutoField(db_column='idSuscripcion', primary_key=True)
    plan = models.CharField(max_length=20, blank=True, null=True)
    estado = models.CharField(max_length=20, blank=True, null=True)
    fechainicio = models.DateField(db_column='fechaInicio')
    fechafin = models.DateField(db_column='fechaFin')
    idbarberia = models.ForeignKey(Barberias, models.DO_NOTHING, db_column='idBarberia', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Suscripciones'