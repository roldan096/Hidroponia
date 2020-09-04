
import sys
import socket
import argparse
import datetime, time
from datetime import datetime, timedelta

import os
import threading
import subprocess
from termcolor import colored
import json
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import rcParams 

ruta =  os.path.join(os.path.dirname(os.path.abspath(__file__)))
ruta = ruta + "/"
def obtenerUsuario(ruta):
    lista = ruta.split("/")
    return "/"+lista[1]+"/"+lista[2]+"/"	
rutaUsuario = obtenerUsuario(ruta)
#print(rutaUsuario)
usuario = rutaUsuario[6:-1]


raiz =  os.path.join(os.path.dirname(os.path.abspath(__file__)),"..")
sys.path.append(raiz)

'''Operacion 2.- Pago de Boleto'''

			# mensaje = (idBoleto, idexpedidora, fecha boleto)
			#mensaje = str(2) + "," + str(1) + "," + '2017-07-11'
			#configSocket("pago boleto", mensaje)


class Grafico:
    CONECTADO = 1
    DESCONECTADO = 0
    def __init__(self,fecha,archivo):
        self.estado = self.DESCONECTADO
        self.funcionando = True
        self.hora_inicio_operacion = time.time()

        datos = self.obtener_datos(fecha,archivo)
        self.inicializar(datos)


    def inicializar (self,datos):
        x_01 = []
        y_01 = []
        x_02 = []
        y_02 = []
        x_03 = []
        y_03 = []
        print("###",datos)
        for dato in datos:
            
            fecha = dato['fecha']
            ph = dato['ph']
            ec = int(dato['ec'])/100
            temperatura = dato['temperatura']



            x_01.append(fecha)
            y_01.append(ph)
            x_02.append(fecha)
            y_02.append(ec)
            x_03.append(fecha)
            y_03.append(temperatura)


            """
            if dato['z_01'] == -1:
                plt.annotate("sc",xy=(fecha,ph),xytext=(fecha,ph)) 
            if dato['z_01'] == 1:
                plt.annotate("alerta",xy=(fecha,ph),xytext=(fecha,ph)) 
            """
                
            if dato['z_02'] == -1:
                plt.annotate("sc",xy=(fecha,ph),xytext=(fecha,ph)) 
            if dato['z_02'] == 1:
                plt.annotate("alerta",xy=(fecha,ph),xytext=(fecha,ph)) 

            if dato['z_03'] == -1:
                plt.annotate("sc",xy=(fecha,ec),xytext=(fecha,ec)) 
            if dato['z_03'] == 1:
                plt.annotate("alerta",xy=(fecha,ec),xytext=(fecha,ec)) 
            
            if dato['z_04'] == -1:
                plt.annotate("sc",xy=(fecha,temperatura),xytext=(fecha,temperatura)) 
            if dato['z_04'] == 1:
                plt.annotate("alerta",xy=(fecha,temperatura),xytext=(fecha,temperatura)) 
            
            

                   
                

            


        
        #plt.ylim(0,14)
        rcParams["figure.figsize"]=15,7
        plt.style.use("ggplot")
        
        plt.plot(x_01,y_01,label="Ph",color="red",marker='o')
        plt.plot(x_02,y_02,label="Conductividad Electrica / 100",color="#00cc00",marker='o')
        plt.plot(x_03,y_03,label="Temperatura",color="#0099ff",marker='o')
        
        #plt.yticks([0,2,4,5,6,7,8,9,10,12,14,16,18,20,22,24,26])
        plt.xticks(rotation='vertical')
        plt.grid(True,color="k",linestyle=":")
        plt.legend(loc=2)
        plt.title("Monitor")
        plt.xlabel("Tiempo")
        plt.ylabel("Valor")
        plt.show()

    def obtener_estado(self):
        return self.estado

    def obtener_datos(self,fecha,archivo):
        r = []
        try:
            archivo = open(ruta+archivo, "r")
            lineas=archivo.readlines()
        except:
            print(f"No se pudo leer del archivo: {archivo} ")
            exit(0)
        
        for linea in lineas:
            if('folio' != ''):
                datos = linea.split(";")
                self.horario_inicio =  datetime.strptime(datos[0], '%Y-%m-%d %H:%M:%S')

                if fecha.date() == self.horario_inicio.date():
                    datos_pre = datos[1].replace("'",'"')
                    datos_json = json.loads(datos_pre)
                    print(datos_json)
                    r.append(datos_json)
        return r
                


    

   

if __name__ == "__main__":
    
    if len(sys.argv) < 3:
        print(f"Ejecucion: python {sys.argv[0]} [fecha AAAA-MM-DD] [archivo.txt]")
        exit(0)
    else:
        fecha = datetime.strptime(sys.argv[1], '%Y-%m-%d')
        archivo = sys.argv[2]
        grafico = Grafico(fecha,archivo)

        try:
            fecha = datetime.strptime(sys.argv[1], '%Y-%m-%d')
            #grafico = Grafico(fecha)
        except:
            print("Fecha invalida")
            print(f"Ejecucion: python {sys.argv[0]} [fecha: AAAA-MM-DD]")
            exit(0)
