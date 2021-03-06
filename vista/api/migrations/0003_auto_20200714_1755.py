# Generated by Django 2.2.12 on 2020-07-14 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20200714_1528'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='solucion',
            name='gramos',
        ),
        migrations.AddField(
            model_name='solucion',
            name='aplicacion',
            field=models.DecimalField(decimal_places=5, default=0, help_text='Cantidad aplicada para lograr la escala de afeccion', max_digits=15, verbose_name='Mililitros por litro'),
        ),
        migrations.AddField(
            model_name='solucion',
            name='escala',
            field=models.DecimalField(decimal_places=2, default=0, help_text='Ej: Tds = 100 (ppm) , Ph = 1 (grado de acidez)', max_digits=15, verbose_name='Escala de afeccion'),
        ),
    ]
