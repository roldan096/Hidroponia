# Generated by Django 2.2.12 on 2020-07-14 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='solucion',
            name='direccion',
            field=models.IntegerField(default=0, verbose_name='Direccion'),
        ),
        migrations.AlterField(
            model_name='solucion',
            name='gramos',
            field=models.DecimalField(decimal_places=5, default=0, max_digits=15, verbose_name='Mililitros por litro'),
        ),
        migrations.AlterField(
            model_name='solucion',
            name='tipo',
            field=models.CharField(choices=[('Agua', 'Agua'), ('Ph reductor', 'Ph reductor'), ('Ph elevador', 'Ph elevador'), ('Ec reductor', 'Ec reductor'), ('Ec elevador', 'Ec elevador')], default='Agua', max_length=50, verbose_name='Tipo'),
        ),
        migrations.AlterField(
            model_name='tratamiento',
            name='ajuste_nivel',
            field=models.IntegerField(default=0, help_text='Se toma una accion al alcanzar esta cantidad de litros', verbose_name='Ajustes en nivel'),
        ),
    ]
