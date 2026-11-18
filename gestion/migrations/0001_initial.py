import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Barberia',
            fields=[
                ('id', models.AutoField(db_column='idBarberia', primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=255)),
                ('direccion', models.CharField(max_length=255)),
                ('telefono', models.CharField(max_length=50)),
                ('latitud', models.CharField(max_length=200)),
                ('longitud', models.CharField(max_length=234)),
            ],
            options={
                'verbose_name_plural': 'barberias',
                'db_table': 'barberia',
            },
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(db_column='idCliente', primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=255)),
                ('apellido', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('telefono', models.CharField(max_length=255)),
                ('direccion', models.CharField(max_length=245)),
            ],
            options={
                'verbose_name_plural': 'clientes',
                'db_table': 'cliente',
            },
        ),
        migrations.CreateModel(
            name='Historial',
            fields=[
                ('id', models.AutoField(db_column='idHistorial', primary_key=True, serialize=False)),
                ('tabla_afectada', models.CharField(blank=True, db_column='tablaAfectada', max_length=50, null=True)),
                ('accion', models.CharField(blank=True, max_length=50, null=True)),
                ('fecha', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'historial',
                'db_table': 'historial',
                'ordering': ['-fecha'],
            },
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(db_column='idUsuario', primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=255)),
                ('apellido', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=100)),
                ('telefono', models.CharField(max_length=20)),
                ('rol', models.CharField(choices=[('Admin', 'Admin'), ('Barbero', 'Barbero'), ('Cliente', 'Cliente')], max_length=10)),
                ('direccion', models.CharField(max_length=40)),
            ],
            options={
                'db_table': 'usuario',
            },
        ),
        migrations.CreateModel(
            name='Barbero',
            fields=[
                ('id', models.AutoField(db_column='idBarbero', primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=255)),
                ('especialidad', models.CharField(max_length=100)),
                ('comision', models.DecimalField(db_column='comicion', decimal_places=5, max_digits=12)),
                ('barberia', models.ForeignKey(blank=True, db_column='idBarberia', null=True, on_delete=django.db.models.deletion.PROTECT, to='gestion.barberia')),
                ('usuario', models.ForeignKey(blank=True, db_column='idUsuario', null=True, on_delete=django.db.models.deletion.PROTECT, to='gestion.usuario')),
            ],
            options={
                'verbose_name_plural': 'barberos',
                'db_table': 'barbero',
            },
        ),
        migrations.CreateModel(
            name='Cita',
            fields=[
                ('id', models.AutoField(db_column='idCita', primary_key=True, serialize=False)),
                ('fecha', models.DateField()),
                ('hora', models.TimeField()),
                ('estado', models.CharField(choices=[('Pendiente', 'Pendiente'), ('Confirmada', 'Confirmada'), ('Finalizada', 'Finalizada')], default='Pendiente', max_length=10)),
                ('barbero', models.ForeignKey(blank=True, db_column='idBarbero', null=True, on_delete=django.db.models.deletion.PROTECT, to='gestion.barbero')),
                ('cliente', models.ForeignKey(blank=True, db_column='idCliente', null=True, on_delete=django.db.models.deletion.PROTECT, to='gestion.cliente')),
            ],
            options={
                'verbose_name_plural': 'citas',
                'db_table': 'cita',
                'ordering': ['fecha', 'hora'],
            },
        ),
        migrations.CreateModel(
            name='Compra',
            fields=[
                ('id', models.AutoField(db_column='idCompra', primary_key=True, serialize=False)),
                ('fecha', models.DateField()),
                ('total', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('barberia', models.ForeignKey(blank=True, db_column='idBarberia', null=True, on_delete=django.db.models.deletion.PROTECT, to='gestion.barberia')),
                ('cliente', models.ForeignKey(blank=True, db_column='idCliente', null=True, on_delete=django.db.models.deletion.PROTECT, to='gestion.cliente')),
            ],
            options={
                'verbose_name_plural': 'compras',
                'db_table': 'compra',
            },
        ),
        migrations.CreateModel(
            name='Factura',
            fields=[
                ('id', models.AutoField(db_column='idFactura', primary_key=True, serialize=False)),
                ('fecha', models.DateField()),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('impuesto', models.CharField(max_length=255)),
                ('estado', models.CharField(choices=[('Pagada', 'Pagada'), ('Pendiente', 'Pendiente')], max_length=10)),
                ('barberia', models.ForeignKey(blank=True, db_column='idBarberia', null=True, on_delete=django.db.models.deletion.PROTECT, to='gestion.barberia')),
                ('cita', models.ForeignKey(blank=True, db_column='idCita', null=True, on_delete=django.db.models.deletion.PROTECT, to='gestion.cita')),
                ('cliente', models.ForeignKey(blank=True, db_column='idCliente', null=True, on_delete=django.db.models.deletion.PROTECT, to='gestion.cliente')),
            ],
            options={
                'verbose_name_plural': 'facturas',
                'db_table': 'factura',
            },
        ),
        migrations.CreateModel(
            name='Favorito',
            fields=[
                ('id', models.AutoField(db_column='idFavorito', primary_key=True, serialize=False)),
                ('barberia', models.ForeignKey(blank=True, db_column='idBarberia', null=True, on_delete=django.db.models.deletion.PROTECT, to='gestion.barberia')),
                ('cliente', models.ForeignKey(blank=True, db_column='idCliente', null=True, on_delete=django.db.models.deletion.PROTECT, to='gestion.cliente')),
            ],
            options={
                'verbose_name_plural': 'favoritos',
                'db_table': 'favorito',
            },
        ),
        migrations.CreateModel(
            name='Pago',
            fields=[
                ('id', models.AutoField(db_column='idPago', primary_key=True, serialize=False)),
                ('monto', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('fecha', models.DateField()),
                ('metodo_pago', models.CharField(db_column='metodoPago', max_length=255)),
                ('estado', models.CharField(choices=[('Completado', 'Completado'), ('Pendiente', 'Pendiente')], max_length=10)),
                ('factura', models.ForeignKey(blank=True, db_column='idFactura', null=True, on_delete=django.db.models.deletion.PROTECT, to='gestion.factura')),
            ],
            options={
                'verbose_name_plural': 'pagos',
                'db_table': 'pago',
            },
        ),
        migrations.CreateModel(
            name='Personalizacion',
            fields=[
                ('id', models.AutoField(db_column='idPersonal', primary_key=True, serialize=False)),
                ('logo_url', models.CharField(db_column='logoURL', max_length=255)),
                ('color_primario', models.CharField(db_column='colorPrimario', max_length=40)),
                ('color_secundario', models.CharField(db_column='colorSecundario', max_length=20)),
                ('splash_url', models.CharField(db_column='splashURL', max_length=255)),
                ('barberia', models.ForeignKey(blank=True, db_column='idBarberia', null=True, on_delete=django.db.models.deletion.PROTECT, to='gestion.barberia')),
            ],
            options={
                'verbose_name_plural': 'personalizaciones',
                'db_table': 'personalizacion',
            },
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(db_column='idProducto', primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=255)),
                ('descripcion', models.CharField(db_column='descrpción', max_length=255)),
                ('precio', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('stock', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('barberia', models.ForeignKey(blank=True, db_column='idBarberia', null=True, on_delete=django.db.models.deletion.PROTECT, to='gestion.barberia')),
            ],
            options={
                'verbose_name_plural': 'productos',
                'db_table': 'producto',
            },
        ),
        migrations.CreateModel(
            name='DetalleCompra',
            fields=[
                ('id', models.AutoField(db_column='idDetalle', primary_key=True, serialize=False)),
                ('cantidad', models.IntegerField(db_column='catidad', validators=[django.core.validators.MinValueValidator(1)])),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=10)),
                ('compra', models.ForeignKey(blank=True, db_column='idCompra', null=True, on_delete=django.db.models.deletion.PROTECT, to='gestion.compra')),
                ('producto', models.ForeignKey(blank=True, db_column='idProducto', null=True, on_delete=django.db.models.deletion.PROTECT, to='gestion.producto')),
            ],
            options={
                'verbose_name': 'detalle de compra',
                'verbose_name_plural': 'detalles de compra',
                'db_table': 'detallecompra',
            },
        ),
        migrations.CreateModel(
            name='Resena',
            fields=[
                ('id', models.AutoField(db_column='idResena', primary_key=True, serialize=False)),
                ('calificacion', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('comentario', models.TextField()),
                ('fecha', models.DateField()),
                ('barberia', models.ForeignKey(blank=True, db_column='idBarberia', null=True, on_delete=django.db.models.deletion.PROTECT, to='gestion.barberia')),
                ('cliente', models.ForeignKey(blank=True, db_column='idCliente', null=True, on_delete=django.db.models.deletion.PROTECT, to='gestion.cliente')),
            ],
            options={
                'verbose_name': 'reseña',
                'verbose_name_plural': 'reseñas',
                'db_table': 'resena',
            },
        ),
        migrations.CreateModel(
            name='Servicio',
            fields=[
                ('id', models.AutoField(db_column='idServicio', primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=255)),
                ('descripcion', models.CharField(db_column='descrpcion', max_length=100)),
                ('precio', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('duracion', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('barberia', models.ForeignKey(blank=True, db_column='idBarberia', null=True, on_delete=django.db.models.deletion.PROTECT, to='gestion.barberia')),
            ],
            options={
                'verbose_name_plural': 'servicios',
                'db_table': 'servicio',
            },
        ),
        migrations.AddField(
            model_name='cita',
            name='servicio',
            field=models.ForeignKey(blank=True, db_column='idServicio', null=True, on_delete=django.db.models.deletion.PROTECT, to='gestion.servicio'),
        ),
        migrations.CreateModel(
            name='Sucursal',
            fields=[
                ('id', models.AutoField(db_column='idSucursal', primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=255)),
                ('direccion', models.CharField(max_length=100)),
                ('barberia', models.ForeignKey(blank=True, db_column='idBarberia', null=True, on_delete=django.db.models.deletion.PROTECT, to='gestion.barberia')),
            ],
            options={
                'verbose_name_plural': 'sucursales',
                'db_table': 'sucursal',
            },
        ),
        migrations.CreateModel(
            name='Suscripcion',
            fields=[
                ('id', models.AutoField(db_column='idSuscripcion', primary_key=True, serialize=False)),
                ('plan', models.CharField(max_length=150)),
                ('estado', models.CharField(choices=[('Activa', 'Activa'), ('Inactiva', 'Inactiva')], max_length=10)),
                ('fecha_inicio', models.DateField(db_column='Fechainicio')),
                ('fecha_fin', models.DateField(db_column='FechaFin')),
                ('barberia', models.ForeignKey(blank=True, db_column='idBarberia', null=True, on_delete=django.db.models.deletion.PROTECT, to='gestion.barberia')),
            ],
            options={
                'verbose_name_plural': 'suscripciones',
                'db_table': 'suscripcion',
            },
        ),
        migrations.CreateModel(
            name='Notificacion',
            fields=[
                ('id', models.AutoField(db_column='idNotif', primary_key=True, serialize=False)),
                ('tipo', models.CharField(max_length=255)),
                ('mensaje', models.TextField()),
                ('fecha', models.DateField()),
                ('leida', models.CharField(max_length=255)),
                ('usuario', models.ForeignKey(blank=True, db_column='idUsuario', null=True, on_delete=django.db.models.deletion.PROTECT, to='gestion.usuario')),
            ],
            options={
                'verbose_name': 'notificación',
                'verbose_name_plural': 'notificaciones',
                'db_table': 'notificacion',
            },
        ),
        migrations.AddField(
            model_name='cliente',
            name='usuario',
            field=models.ForeignKey(blank=True, db_column='idUsuario', null=True, on_delete=django.db.models.deletion.PROTECT, to='gestion.usuario'),
        ),
        migrations.AddField(
            model_name='barberia',
            name='usuario',
            field=models.ForeignKey(blank=True, db_column='idUsuario', null=True, on_delete=django.db.models.deletion.PROTECT, to='gestion.usuario'),
        ),
    ]
