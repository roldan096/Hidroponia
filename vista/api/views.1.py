from django.shortcuts import render
from transaccion.models import Transaccion
from datetime import datetime, timedelta
from django.db.models import Sum, Q, Count
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
# Create your views here.
class CorteApiView(APIView):
    """
    A view that returns the count of active users in JSON.
    """
    renderer_classes = [JSONRenderer]
    def get(self, request, format=None):
        fecha_1 = self.request.GET.get('f1') 
        hora_1 = self.request.GET.get('h1') 
        fecha_2 = self.request.GET.get('f2') 
        hora_2 = self.request.GET.get('h2') 
        fechahora_1 = datetime.strptime(str(fecha_1)+" "+str(hora_1), '%d-%m-%Y %H:%M:%S')
        fechahora_2 = datetime.strptime(str(fecha_2)+" "+str(hora_2), '%d-%m-%Y %H:%M:%S')
        exitosos = 0
        incidencias = 0
        cancelados = 0
        ingreso = 0
        operaciones = 0
        print("datetimes:",fechahora_1,fechahora_2)
        if fechahora_1:
            if fechahora_2:
                transaccion = Transaccion.objects.filter(created__range=[fechahora_1, fechahora_2])
                exitosos = transaccion.filter(codigo = 1).count()
                incidencias = transaccion.filter(codigo__range=(2, 4)).count()
                cancelados = transaccion.filter(codigo = 5).count()
                ingreso=transaccion.aggregate(Sum('monto'))['monto__sum']
                operaciones = transaccion.count()
                print("Transaccion full: ",transaccion)
            else:
                transaccion = Transaccion.objects.filter(
                    Q(created__date=fechahora_1)
                    )
                return transaccion
        else:
            transaccion = Tansaccion.objtects.all()

        print(ingreso)
        print("pagos: ", operaciones)

        content = {
            'operaciones': operaciones,
            'ingreso': ingreso,
            'exitosos':exitosos,
            'incidencias':incidencias,
            'cancelados':cancelados
            }
        return Response(content)