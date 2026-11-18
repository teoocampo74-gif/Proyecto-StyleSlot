from django.db import migrations


def crear_datos_iniciales(apps, schema_editor):
    Barberia = apps.get_model('gestion', 'Barberia')
    Barbero = apps.get_model('gestion', 'Barbero')
    Servicio = apps.get_model('gestion', 'Servicio')

    barberia, _ = Barberia.objects.get_or_create(
        nombre='StyleSlot Barbería',
        defaults={
            'direccion': 'Medellín, Colombia',
            'telefono': '3000000000',
            'latitud': '6.2442',
            'longitud': '-75.5812',
        },
    )

    for nombre, especialidad, comision in (
        ('Miguel Rodríguez', 'Corte clásico', 4),
        ('Carlos Martínez', 'Barba y afeitado', 3.5),
        ('David Torres', 'Diseño moderno', 3),
    ):
        Barbero.objects.get_or_create(
            nombre=nombre,
            defaults={
                'especialidad': especialidad,
                'comision': comision,
                'barberia': barberia,
            },
        )

    for nombre, precio, duracion in (
        ('Corte clásico', 25000, 30),
        ('Recorte de barba', 18000, 20),
        ('Corte y barba', 40000, 45),
    ):
        Servicio.objects.get_or_create(
            nombre=nombre,
            defaults={
                'descripcion': nombre,
                'precio': precio,
                'duracion': duracion,
                'barberia': barberia,
            },
        )


def eliminar_datos_iniciales(apps, schema_editor):
    Barberia = apps.get_model('gestion', 'Barberia')
    Barbero = apps.get_model('gestion', 'Barbero')
    Servicio = apps.get_model('gestion', 'Servicio')

    barberias = Barberia.objects.filter(nombre='StyleSlot Barbería')
    Barbero.objects.filter(barberia__in=barberias).delete()
    Servicio.objects.filter(barberia__in=barberias).delete()
    barberias.delete()


class Migration(migrations.Migration):
    dependencies = [
        ('gestion', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(crear_datos_iniciales, eliminar_datos_iniciales),
    ]
