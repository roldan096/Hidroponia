from .models import *
from rest_framework.serializers import ModelSerializer


class InvernaderoSerializer(ModelSerializer):
    class Meta:
        model = Invernadero
        fields = '__all__'

class ZonaSerializer(ModelSerializer):
    class Meta:
        model = Zona
        fields = '__all__'

class TratamientoSerializer(ModelSerializer):
    class Meta:
        model = Tratamiento
        fields = '__all__'

class HorarioSerializer(ModelSerializer):
    class Meta:
        model = Horario
        fields = '__all__'

class SolucionSerializer(ModelSerializer):
    class Meta:
        model = Solucion
        fields = '__all__'

class NutrienteSerializer(ModelSerializer):
    class Meta:
        model = Nutriente
        fields = '__all__'

class PlantaSerializer(ModelSerializer):
    class Meta:
        model = Planta
        fields = '__all__'

class TanqueSerializer(ModelSerializer):
    class Meta:
        model = Tanque
        fields = '__all__'

class SensorSerializer(ModelSerializer):
    class Meta:
        model = Sensor
        fields = '__all__'