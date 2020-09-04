
import sys
import socket
import argparse
import datetime, time
import os
import threading
import subprocess
from termcolor import colored

tam_buffer = 150
host = '192.168.1.129'
port = 2324

hosts = ('8.8.8.8', 'kernel.org', 'yahoo.com',host)

'''Operacion 2.- Pago de Boleto'''

			# mensaje = (idBoleto, idexpedidora, fecha boleto)
			#mensaje = str(2) + "," + str(1) + "," + '2017-07-11'
			#configSocket("pago boleto", mensaje)


class Reloj:
    CONECTADO = 1
    DESCONECTADO = 0
    def __init__(self,tiempo_operacion,tiempo_descanso):
        self.estado = self.DESCONECTADO
        self.funcionando = True
        self.hora_inicio_operacion = time.time()
        self.contador_segundos = int(time.time () - self.hora_inicio_operacion)
        self.tiempo_operacion = tiempo_operacion
        self.tiempo_descanso = tiempo_descanso
        reloj = threading.Thread(target=self.run)
        reloj.start()

    def run (self):
        print("#-------------------- Iniciando Servidor")
        self.funcionando = True
        self.estado = self.CONECTADO
        while (self.funcionando):
            time.sleep(.05)
            #print(colored("Time: ",'green'),self.contador_segundos)

            self.contador_segundos = int(time.time () - self.hora_inicio_operacion)
            if self.contador_segundos >= (self.tiempo_operacion*60) and self.estado:
                print(colored("Deteniendo: ",'red'),self.tiempo_descanso*60)
                self.contador_segundos = 0
                self.hora_inicio_operacion = time.time()
                self.estado = 0
            
            if not self.estado:
                tiempo_total = self.tiempo_descanso*60
                #print(colored("Tiempo de descanso: ",'red'),self.contador_segundos,tiempo_total)
                #if self.contador_segundos % tiempo_total == 0:
                if self.contador_segundos >= tiempo_total:
                    self.contador_segundos = 0
                    self.hora_inicio_operacion = time.time()
                    self.estado = 1

    def obtener_estado(self):
        return self.estado

    def obtener_segundos(self):
        return self.contador_segundos
    

   