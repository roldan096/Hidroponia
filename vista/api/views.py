from django.shortcuts import render
from django.shortcuts import render
from .models import *
from datetime import datetime, timedelta
from django.db.models import Sum, Q, Count
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
# Create your views here.
class ZonasInvernaderoApiView(APIView):
    """
    A view that returns the count of active users in JSON.
    """
    renderer_classes = [JSONRenderer]
    def get(self, request, format=None):
        idx = self.request.GET.get('invernadero') 
        #if idx:
        transaccion = Zona.objects.filter(id=idx)
        return transaccion