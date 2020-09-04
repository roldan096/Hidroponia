from rest_framework import viewsets
from . import serializers
from .models import *
from datetime import datetime, timedelta
from django.db.models import Sum, Q, Count
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView

from rest_framework.decorators import action


class InvernaderoViewset(viewsets.ModelViewSet):
    queryset = Invernadero.objects.all()
    serializer_class = serializers.InvernaderoSerializer

class ZonaViewset(viewsets.ModelViewSet):
    queryset = Zona.objects.all()
    serializer_class = serializers.ZonaSerializer
    def get_queryset(self):
        i = self.request.GET.get('invernadero', None)
        if i :
            zonas_invernadero = Zona.objects.filter(invernadero_id=i)
            print(i)
            return zonas_invernadero
        else:
            queryset = Zona.objects.all()
            return queryset
    
        

class TratamientoViewset(viewsets.ModelViewSet):
    queryset = Tratamiento.objects.all()
    serializer_class = serializers.TratamientoSerializer
    

class HorarioViewset(viewsets.ModelViewSet):
    queryset = Horario.objects.all()
    serializer_class = serializers.HorarioSerializer

class SolucionViewset(viewsets.ModelViewSet):
    queryset = Solucion.objects.all()
    serializer_class = serializers.SolucionSerializer

class NutrienteViewset(viewsets.ModelViewSet):
    queryset = Nutriente.objects.all()
    serializer_class = serializers.NutrienteSerializer

class PlantaViewset(viewsets.ModelViewSet):
    queryset = Planta.objects.all()
    serializer_class = serializers.PlantaSerializer


class TanqueViewset(viewsets.ModelViewSet):
    queryset = Tanque.objects.all()
    serializer_class = serializers.TanqueSerializer
    def get_queryset(self):
        i = self.request.GET.get('zona', None)
        if i :
            tanque_zona = Tanque.objects.filter(zona_id=i)
            print(i)
            return tanque_zona
        else:
            queryset = Tanque.objects.all()
            return queryset


class SensorViewset(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = serializers.SensorSerializer
    def get_queryset(self):
        i = self.request.GET.get('tanque', None)
        if i :
            sensor_tanque = Sensor.objects.filter(tanque_id=i)
            print(i)
            return sensor_tanque
        else:
            queryset = Sensor.objects.all()
            return queryset

