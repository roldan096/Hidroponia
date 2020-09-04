from django.shortcuts import render,get_object_or_404
from django.views.generic.base import TemplateView,RedirectView

import requests,json,os

# Create your views here.
cancelacion = 0
class UiPageView(TemplateView):
    template_name = "ui/ui.html"

class UiCancelacionView(TemplateView):
    template_name = "ui/ui.html"	
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['number'] = 3
        print("##########################")
        datos = {
        "cancelar_pago": 1,
        "operacion_recarga": 0,
        }
        url = 'http://127.0.0.1:8000/hook/'
        encabezado = {'Content-Type': 'application/json'}
        response = requests.post(
                url, data=json.dumps(datos),
                headers=encabezado
                )
        print("##########################",response.json())
        return context
class UiRecargaView(TemplateView):
    template_name = "ui/ui.html"	
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['number'] = 3
        print("##########################")
        datos = {
        "cancelar_pago": 0,
        "operacion_recarga": 1,
        }
        url = 'http://127.0.0.1:8000/hook/'
        encabezado = {'Content-Type': 'application/json'}
        response = requests.post(
                url, data=json.dumps(datos),
                headers=encabezado
                )
        print("##########################",response)
        #print("##########################",response.json())
        return context

