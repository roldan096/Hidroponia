from django.db import models
from django.utils.timezone import now

# Create your models here.

class Invernadero(models.Model):

    TIPO = (
        ("Tunel", "Tunel"),
        ("Capilla", "Capilla"),
        ("Diente de sierra", "Diente de sierra"),
        ("Generico", "Generico"),
    )
    nombre = models.CharField(max_length=200, verbose_name = 'Nombre', default="-")
    ubicacion = models.CharField(max_length=200, verbose_name = 'Ubicacion', default="-")
    latitud = models.CharField(max_length=200, verbose_name = 'Latitud', default="-")
    longitud = models.CharField(max_length=200, verbose_name = 'Longitud', default="-")
    tipo = models.CharField(max_length=50, choices=TIPO, verbose_name = 'Tipo',default='Generico')
    ancho = models.DecimalField(verbose_name='Ancho', max_digits=15, decimal_places=5, default=0)
    largo = models.DecimalField(verbose_name='Largo', max_digits=15, decimal_places=5, default=0)
    alto = models.DecimalField(verbose_name='Alto', max_digits=15, decimal_places=5, default=0)
    activo = models.BooleanField(verbose_name = 'Activo')
    created = models.DateTimeField(verbose_name = 'Fecha de creacion',default = now)
    updated = models.DateTimeField(auto_now=True, verbose_name = 'Ultima modificacion')

    class Meta:
        verbose_name = 'Invernadero'
        verbose_name_plural = 'Invernadero'
        ordering = ['-created']

    def __str__(self):
        return str(self.nombre)+" "+str(self.ubicacion)



class Nutriente(models.Model):

    TIPO = (
        ("Soluble", "Soluble"),
        ("Ambiental", "Ambiental"),
    )
    UNIDAD = (
        ("Gramos", "Gramos"),
        ("Mililitros", "Mililitros"),
    )
    nombre = models.CharField(max_length=200, verbose_name = 'Nombre', default="-")
    descripcion = models.TextField(max_length=200, verbose_name = 'Descripcion')
    tipo = models.CharField(max_length=50, choices=TIPO, verbose_name = 'Tipo',default='Hidroponico')
    unidad = models.CharField(max_length=50, choices=UNIDAD, verbose_name = 'Unidad',default='Mililitros')
    cantidad = models.DecimalField(verbose_name='Cantidad', max_digits=15, decimal_places=5, default=0)
    expiracion = models.DateField(verbose_name = 'Fecha de expiracion')    
    created = models.DateTimeField(verbose_name = 'Fecha de pago',default = now)
    updated = models.DateTimeField(auto_now=True, verbose_name = 'Ultima modificacion')
    class Meta:
        verbose_name = 'Nutriente'
        verbose_name_plural = 'Nutriente'
        ordering = ['-created']

    def __str__(self):
        return str(self.nombre)+" "+str(self.cantidad)


class Solucion(models.Model):

    TIPO = (
        ("Agua", "Agua"),
        ("Solucion Nutritiva", "Solucion Nutritiva"),
        ("Ph reductor", "Ph reductor"),
        ("Ph elevador", "Ph elevador"),
        ("Ec reductor", "Ec reductor"),
        ("Ec elevador", "Ec elevador"),
    )
   
    nombre = models.CharField(max_length=200, verbose_name = 'Nombre', default="-")
    tipo = models.CharField(max_length=50, choices=TIPO, verbose_name = 'Tipo',default='Agua')
    nutrientes = models.ManyToManyField(Nutriente, verbose_name = 'Nutrientes')
    aplicacion = models.DecimalField(verbose_name='Mililitros por litro', help_text = "Cantidad aplicada para lograr la escala de afeccion", max_digits=15, decimal_places=5, default=0)
    escala = models.DecimalField(verbose_name='Escala de afeccion', help_text = "Ej: Tds = 100 (ppm) , Ph = 1 (grado de acidez)",max_digits=15, decimal_places=2, default=0)
    direccion = models.IntegerField(verbose_name='Direccion', default=0)
    created = models.DateTimeField(verbose_name = 'Fecha de pago',default = now)
    updated = models.DateTimeField(auto_now=True, verbose_name = 'Ultima modificacion')
    class Meta:
        verbose_name = 'Solucion'
        verbose_name_plural = 'Solucion'
        ordering = ['-created']

    def __str__(self):
        return str(self.nombre)+" "+str(self.tipo)


class Horario(models.Model):
    DIA = (
        ("ninguno", "ninugno"),
        ("lunes", "lunes"),
        ("martes", "MARTES"),
        ("miercoles", "miercoles"),
        ("jueves", "jueves"),
        ("viernes", "viernes"),
        ("sabado", "sabado"),
        ("domingo", "domingo")
    )
    nombre = models.CharField(max_length=200, verbose_name = 'Nombre', default="-")
    #fecha_inicio = models.DateField(verbose_name = 'Fecha inicio',blank=True, null=True)
    #fecha_fin = models.DateField(verbose_name = 'Fecha fin',blank=True, null=True)
    intervalo_descanso = models.IntegerField(verbose_name='Intervalo de descanso en minutos',help_text="Ej. Cada 30 minutos tendra un tiempo de descando", default=0)
    tiempo_descanso = models.IntegerField(verbose_name='Tiempo de descanso en minutos',help_text="Ej. Cada intervalo de descanso descansara 5 minutos", default=0)

    horario_inicio = models.TimeField(verbose_name = 'Horario inicio',blank=True, null=True)
    horario_fin = models.TimeField(verbose_name = 'Horario fin',blank=True, null=True)
    #dia_semana = models.CharField(max_length=200, choices=DIA, verbose_name = 'Dia de la semana',blank=True, null=True)
    created = models.DateTimeField(verbose_name = 'Fecha de pago',default = now)
    updated = models.DateTimeField(auto_now=True, verbose_name = 'Ultima modificacion')
    class Meta:
        verbose_name = 'Horario'
        verbose_name_plural = 'Horario'
        ordering = ['-created']

    def __str__(self):
        return str(self.nombre)


class Tratamiento(models.Model):

    TIPO = (
        ("Soluble", "Soluble"),
        ("Ambiental", "Ambiental"),
    )
    UNIDAD = (
        ("Gramos", "Gramos"),
        ("Litros", "Litros"),
        ("Mililitros", "Mililitros"),
    )
    nombre = models.CharField(max_length=200, verbose_name = 'Nombre', default="-")
    tipo = models.CharField(max_length=50, choices=TIPO, verbose_name = 'Tipo',default='Soluble')
    nivel_completado = models.IntegerField(verbose_name='Nivel completado', default=0)
    activo = models.BooleanField(verbose_name = 'Activo')
    unidad = models.CharField(max_length=50, choices=UNIDAD, verbose_name = 'Unidad',default='Litros')
    cantidad = models.DecimalField(verbose_name='Cantidad', max_digits=15, decimal_places=2, default=0)
    ajuste_nivel = models.IntegerField(verbose_name='Ajustes en nivel', help_text="Se toma una accion al alcanzar esta cantidad de litros", default=0)
    duracion = models.IntegerField(verbose_name='Duracion',help_text="Dias de duracion", default=0)
    horario_id = models.ForeignKey(Horario, verbose_name = 'Horario', related_name='get_tratamiento', on_delete = models.CASCADE)
    solucion_id = models.ManyToManyField(Solucion, verbose_name = 'Solucion')

    created = models.DateTimeField(verbose_name = 'Fecha de pago',default = now)
    updated = models.DateTimeField(auto_now=True, verbose_name = 'Ultima modificacion')
    class Meta:
        verbose_name = 'Tratamiento'
        verbose_name_plural = 'Tratamiento'
        ordering = ['-created']

    def __str__(self):
        return str(self.nombre)+" "+str(self.tipo)




class Zona(models.Model):

    TIPO = (
        ("Hidroponico", "Hidroponico"),
        ("Semi-Hidroponico", "Semi-Hidroponico"),
        ("Terrestre", "Terrestre"),
    )
    nombre = models.CharField(max_length=200, verbose_name = 'Nombre', default="-")
    tipo = models.CharField(max_length=50, choices=TIPO, verbose_name = 'Tipo',default='Hidroponico')
    
    ancho = models.DecimalField(verbose_name='Ancho', max_digits=15, decimal_places=5, default=0)
    largo = models.DecimalField(verbose_name='Largo', max_digits=15, decimal_places=5, default=0)
    alto = models.DecimalField(verbose_name='Alto', max_digits=15, decimal_places=5, default=0)
    activo = models.BooleanField(verbose_name = 'Activo')
    tratamiento_id = models.ForeignKey(Tratamiento, verbose_name = 'Tratamiento', related_name='get_zona', on_delete = models.CASCADE)
    invernadero_id = models.ForeignKey(Invernadero, verbose_name = 'Invernadero', related_name='get_zona', on_delete = models.CASCADE)
    created = models.DateTimeField(verbose_name = 'Fecha de pago',default = now)
    updated = models.DateTimeField(auto_now=True, verbose_name = 'Ultima modificacion')
    class Meta:
        verbose_name = 'Zona'
        verbose_name_plural = 'Zona'
        ordering = ['-created']

    def __str__(self):
        return str(self.nombre)+" "+str(self.tipo)

class Tanque(models.Model):

    TIPO = (
        ("Agua", "Agua"),
        ("Agua acondicionada", "Agua acondicionada"),
        ("Nutrientes", "Nutrientes"),
        ("Solucion nutritiva", "Solucion nutritiva"),
    )
    TIPO_LLENADO = (
        ("Automatico", "Automatico"),
        ("Manual", "Manual"),
        ("Mixto", "Mixto"),
    )
    nombre = models.CharField(max_length=200, verbose_name = 'Nombre', default="-")
    tipo = models.CharField(max_length=50, choices=TIPO, verbose_name = 'Tipo',default='Agua')
    tipo_llenado = models.CharField(max_length=50, choices=TIPO_LLENADO, verbose_name = 'Tipo de llenado',default='Automatico')
    unidad = models.CharField(max_length=50, verbose_name = 'Unidad')
    capacidad = models.DecimalField(max_length=50, verbose_name = 'Capacidad', max_digits=15, decimal_places=2, default=0)
    valor_actual = models.DecimalField(max_length=50, verbose_name = 'Valor actual', max_digits=15, decimal_places=2, default=0)
    valor_maximo = models.DecimalField(max_length=50, verbose_name = 'Valor maximo', max_digits=15, decimal_places=2, default=0)
    valor_minimo = models.DecimalField(max_length=50, verbose_name = 'Valor minimo', max_digits=15, decimal_places=2, default=0)
    activo = models.BooleanField(verbose_name = 'Activo')
    zona_id = models.ForeignKey(Zona, verbose_name = 'Zona', related_name='get_tanque', on_delete = models.CASCADE)
    created = models.DateTimeField(verbose_name = 'Fecha de creacion',default = now)
    updated = models.DateTimeField(auto_now=True, verbose_name = 'Ultima lectura')
    class Meta:
        verbose_name = 'Tanque'
        verbose_name_plural = 'Tanque'
        ordering = ['-created']

    def __str__(self):
        return str(self.nombre)+" "+str(self.tipo_llenado)


class Sensor(models.Model):

    TIPO = (
        ("PH", "PH"),
        ("Conductividad electrica", "Conductividad electrica"),
        ("TDS", "TDS"),
        ("Temperatura", "Temperatura"),
        ("Nivel", "Nivel"),
        ("Flujo", "Flujo"),
    )
    nombre = models.CharField(max_length=200, verbose_name = 'Nombre', default="-")
    tipo = models.CharField(max_length=50, choices=TIPO, verbose_name = 'Tipo',default='PH')
    unidad = models.CharField(max_length=50, verbose_name = 'Unidad')
    valor_actual = models.DecimalField(max_length=50, verbose_name = 'Valor actual',max_digits=15, decimal_places=2, default=0)
    valor_maximo = models.DecimalField(max_length=50, verbose_name = 'Valor maximo',max_digits=15, decimal_places=2, default=0)
    valor_minimo = models.DecimalField(max_length=50, verbose_name = 'Valor minimo',max_digits=15, decimal_places=2, default=0)
    puerto = models.IntegerField(verbose_name='Puerto', default=0)
    vida_util = models.DecimalField(verbose_name='Años de vida util', max_digits=15, decimal_places=2, default=0)
    activo = models.BooleanField(verbose_name = 'Activo')
    tanque_id = models.ForeignKey(Tanque, verbose_name = 'Tanque', related_name='get_sensor', on_delete = models.CASCADE)
    created = models.DateTimeField(verbose_name = 'Fecha de creacion',default = now)
    updated = models.DateTimeField(auto_now=True, verbose_name = 'Ultima lectura')
    class Meta:
        verbose_name = 'Sensor'
        verbose_name_plural = 'Sensor'
        ordering = ['-created']

    def __str__(self):
        return str(self.nombre)+" "+str(self.tipo)




class Planta(models.Model):
    TIPO = (
        ("Soluble", "Soluble"),
        ("Ambiental", "Ambiental"),
    )
    nombre = models.CharField(max_length=200, verbose_name = 'Nombre', default="-")
    descripcion = models.TextField(max_length=200, verbose_name = 'Descripcion')
    tipo = models.CharField(max_length=50, choices=TIPO, verbose_name = 'Tipo',default='Hidroponico')
    altura_maxima = models.DecimalField(verbose_name='Altura maxima', max_digits=15, decimal_places=5, default=0)
    diametro_maximo = models.DecimalField(verbose_name='Diametro maximo', max_digits=15, decimal_places=5, default=0) 
    zona_id = models.ForeignKey(Zona, verbose_name = 'Zona', related_name='get_planta', on_delete = models.CASCADE)
    created = models.DateTimeField(verbose_name = 'Fecha de pago',default = now)
    updated = models.DateTimeField(auto_now=True, verbose_name = 'Ultima modificacion')
    class Meta:
        verbose_name = 'Planta'
        verbose_name_plural = 'Planta'
        ordering = ['-created']

    def __str__(self):
        return str(self.nombre)+" "+str(self.zona_id)



