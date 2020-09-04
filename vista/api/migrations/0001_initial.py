# Generated by Django 2.2.12 on 2020-07-05 10:41

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Horario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(default='-', max_length=200, verbose_name='Nombre')),
                ('intervalo_descanso', models.IntegerField(default=0, help_text='Ej. Cada 30 minutos tendra un tiempo de descando', verbose_name='Intervalo de descanso en minutos')),
                ('tiempo_descanso', models.IntegerField(default=0, help_text='Ej. Cada intervalo de descanso descansara 5 minutos', verbose_name='Tiempo de descanso en minutos')),
                ('horario_inicio', models.TimeField(blank=True, null=True, verbose_name='Horario inicio')),
                ('horario_fin', models.TimeField(blank=True, null=True, verbose_name='Horario fin')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Fecha de pago')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Ultima modificacion')),
            ],
            options={
                'verbose_name': 'Horario',
                'verbose_name_plural': 'Horario',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Invernadero',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(default='-', max_length=200, verbose_name='Nombre')),
                ('ubicacion', models.CharField(default='-', max_length=200, verbose_name='Ubicacion')),
                ('latitud', models.CharField(default='-', max_length=200, verbose_name='Latitud')),
                ('longitud', models.CharField(default='-', max_length=200, verbose_name='Longitud')),
                ('tipo', models.CharField(choices=[('Tunel', 'Tunel'), ('Capilla', 'Capilla'), ('Diente de sierra', 'Diente de sierra'), ('Generico', 'Generico')], default='Generico', max_length=50, verbose_name='Tipo')),
                ('ancho', models.DecimalField(decimal_places=5, default=0, max_digits=15, verbose_name='Ancho')),
                ('largo', models.DecimalField(decimal_places=5, default=0, max_digits=15, verbose_name='Largo')),
                ('alto', models.DecimalField(decimal_places=5, default=0, max_digits=15, verbose_name='Alto')),
                ('activo', models.BooleanField(verbose_name='Activo')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Fecha de creacion')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Ultima modificacion')),
            ],
            options={
                'verbose_name': 'Invernadero',
                'verbose_name_plural': 'Invernadero',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Nutriente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(default='-', max_length=200, verbose_name='Nombre')),
                ('descripcion', models.TextField(max_length=200, verbose_name='Descripcion')),
                ('tipo', models.CharField(choices=[('Soluble', 'Soluble'), ('Ambiental', 'Ambiental')], default='Hidroponico', max_length=50, verbose_name='Tipo')),
                ('unidad', models.CharField(choices=[('Gramos', 'Gramos'), ('Mililitros', 'Mililitros')], default='Mililitros', max_length=50, verbose_name='Unidad')),
                ('cantidad', models.DecimalField(decimal_places=5, default=0, max_digits=15, verbose_name='Cantidad')),
                ('expiracion', models.DateField(verbose_name='Fecha de expiracion')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Fecha de pago')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Ultima modificacion')),
            ],
            options={
                'verbose_name': 'Nutriente',
                'verbose_name_plural': 'Nutriente',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Solucion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(default='-', max_length=200, verbose_name='Nombre')),
                ('tipo', models.CharField(choices=[('Soluble', 'Soluble'), ('Ambiental', 'Ambiental')], default='Soluble', max_length=50, verbose_name='Tipo')),
                ('gramos', models.DecimalField(decimal_places=5, default=0, max_digits=15, verbose_name='Gramos por litro')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Fecha de pago')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Ultima modificacion')),
                ('nutrientes', models.ManyToManyField(to='api.Nutriente', verbose_name='Nutrientes')),
            ],
            options={
                'verbose_name': 'Solucion',
                'verbose_name_plural': 'Solucion',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Tratamiento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(default='-', max_length=200, verbose_name='Nombre')),
                ('tipo', models.CharField(choices=[('Soluble', 'Soluble'), ('Ambiental', 'Ambiental')], default='Soluble', max_length=50, verbose_name='Tipo')),
                ('nivel_completado', models.IntegerField(default=0, verbose_name='Nivel completado')),
                ('activo', models.BooleanField(verbose_name='Activo')),
                ('unidad', models.CharField(choices=[('Gramos', 'Gramos'), ('Litros', 'Litros'), ('Mililitros', 'Mililitros')], default='Litros', max_length=50, verbose_name='Unidad')),
                ('cantidad', models.DecimalField(decimal_places=2, default=0, max_digits=15, verbose_name='Cantidad')),
                ('ajuste_nivel', models.CharField(default=0, help_text='Se toma una accion al alcanzar esta cantidad de litros', max_length=200, verbose_name='Ajustes en nivel')),
                ('duracion', models.IntegerField(default=0, help_text='Dias de duracion', verbose_name='Duracion')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Fecha de pago')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Ultima modificacion')),
                ('horario_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='get_tratamiento', to='api.Horario', verbose_name='Horario')),
                ('solucion_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='get_tratamiento', to='api.Solucion', verbose_name='Solucion')),
            ],
            options={
                'verbose_name': 'Tratamiento',
                'verbose_name_plural': 'Tratamiento',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Zona',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(default='-', max_length=200, verbose_name='Nombre')),
                ('tipo', models.CharField(choices=[('Hidroponico', 'Hidroponico'), ('Semi-Hidroponico', 'Semi-Hidroponico'), ('Terrestre', 'Terrestre')], default='Hidroponico', max_length=50, verbose_name='Tipo')),
                ('ancho', models.DecimalField(decimal_places=5, default=0, max_digits=15, verbose_name='Ancho')),
                ('largo', models.DecimalField(decimal_places=5, default=0, max_digits=15, verbose_name='Largo')),
                ('alto', models.DecimalField(decimal_places=5, default=0, max_digits=15, verbose_name='Alto')),
                ('activo', models.BooleanField(verbose_name='Activo')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Fecha de pago')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Ultima modificacion')),
                ('invernadero_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='get_zona', to='api.Invernadero', verbose_name='Invernadero')),
                ('tratamiento_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='get_zona', to='api.Tratamiento', verbose_name='Tratamiento')),
            ],
            options={
                'verbose_name': 'Zona',
                'verbose_name_plural': 'Zona',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Tanque',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(default='-', max_length=200, verbose_name='Nombre')),
                ('tipo', models.CharField(choices=[('Agua', 'Agua'), ('Agua acondicionada', 'Agua acondicionada'), ('Nutrientes', 'Nutrientes'), ('Solucion nutritiva', 'Solucion nutritiva')], default='Agua', max_length=50, verbose_name='Tipo')),
                ('tipo_llenado', models.CharField(choices=[('Automatico', 'Automatico'), ('Manual', 'Manual'), ('Mixto', 'Mixto')], default='Automatico', max_length=50, verbose_name='Tipo de llenado')),
                ('unidad', models.CharField(max_length=50, verbose_name='Unidad')),
                ('capacidad', models.DecimalField(decimal_places=2, default=0, max_digits=15, max_length=50, verbose_name='Capacidad')),
                ('valor_actual', models.DecimalField(decimal_places=2, default=0, max_digits=15, max_length=50, verbose_name='Valor actual')),
                ('valor_maximo', models.DecimalField(decimal_places=2, default=0, max_digits=15, max_length=50, verbose_name='Valor maximo')),
                ('valor_minimo', models.DecimalField(decimal_places=2, default=0, max_digits=15, max_length=50, verbose_name='Valor minimo')),
                ('activo', models.BooleanField(verbose_name='Activo')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Fecha de creacion')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Ultima lectura')),
                ('zona_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='get_tanque', to='api.Zona', verbose_name='Zona')),
            ],
            options={
                'verbose_name': 'Tanque',
                'verbose_name_plural': 'Tanque',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(default='-', max_length=200, verbose_name='Nombre')),
                ('tipo', models.CharField(choices=[('PH', 'PH'), ('Conductividad electrica', 'Conductividad electrica'), ('TDS', 'TDS'), ('Temperatura', 'Temperatura'), ('Nivel', 'Nivel'), ('Flujo', 'Flujo')], default='PH', max_length=50, verbose_name='Tipo')),
                ('unidad', models.CharField(max_length=50, verbose_name='Unidad')),
                ('valor_actual', models.DecimalField(decimal_places=2, default=0, max_digits=15, max_length=50, verbose_name='Valor actual')),
                ('valor_maximo', models.DecimalField(decimal_places=2, default=0, max_digits=15, max_length=50, verbose_name='Valor maximo')),
                ('valor_minimo', models.DecimalField(decimal_places=2, default=0, max_digits=15, max_length=50, verbose_name='Valor minimo')),
                ('puerto', models.IntegerField(default=0, verbose_name='Puerto')),
                ('vida_util', models.DecimalField(decimal_places=2, default=0, max_digits=15, verbose_name='Años de vida util')),
                ('activo', models.BooleanField(verbose_name='Activo')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Fecha de creacion')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Ultima lectura')),
                ('tanque_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='get_sensor', to='api.Tanque', verbose_name='Tanque')),
            ],
            options={
                'verbose_name': 'Sensor',
                'verbose_name_plural': 'Sensor',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Planta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(default='-', max_length=200, verbose_name='Nombre')),
                ('descripcion', models.TextField(max_length=200, verbose_name='Descripcion')),
                ('tipo', models.CharField(choices=[('Soluble', 'Soluble'), ('Ambiental', 'Ambiental')], default='Hidroponico', max_length=50, verbose_name='Tipo')),
                ('altura_maxima', models.DecimalField(decimal_places=5, default=0, max_digits=15, verbose_name='Altura maxima')),
                ('diametro_maximo', models.DecimalField(decimal_places=5, default=0, max_digits=15, verbose_name='Diametro maximo')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Fecha de pago')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Ultima modificacion')),
                ('zona_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='get_planta', to='api.Zona', verbose_name='Zona')),
            ],
            options={
                'verbose_name': 'Planta',
                'verbose_name_plural': 'Planta',
                'ordering': ['-created'],
            },
        ),
    ]
