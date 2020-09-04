import threading
import sys
import os
import time
import fechaUTC as hora
#import Conexiones.cliente as Servidor
#from pygame import mixer
import subprocess
from threading import Timer,Thread 
import sched
import termios
import serial
import binascii
#from bitstring import BitArray
from datetime import datetime, timedelta
import calendar
#import psycopg2, psycopg2.extras
#from Botones.Botones import Botones,PuertoDeComunicacion, obtenerNombreDelPuerto
#from Pila.Pila import Pila
from struct import *

import traceback
from Logs.GuardarLogs import GuardarLogs
import shutil
from termcolor import colored,cprint




ruta =  os.path.join(os.path.dirname(os.path.abspath(__file__)))
ruta = ruta + "/"
def obtenerUsuario(ruta):
    lista = ruta.split("/")
    return "/"+lista[1]+"/"+lista[2]+"/"	
rutaUsuario = obtenerUsuario(ruta)
print(rutaUsuario)
print(rutaUsuario[6:-1])
usuario = rutaUsuario[6:-1]


raiz =  os.path.join(os.path.dirname(os.path.abspath(__file__)),"..")
sys.path.append(raiz)

from Variables.Variable import Variable
from Variables.Temporizador import Temporizador
from Conexiones.Servidor import Servidor
from Monitor.Comunicacion import Comunicacion

from Monitor.PuertoSerie import PuertoSerie
from Monitor.Hopper import Hopper
from Monitor.Monedero import Monedero
from Monitor.Billetero import Billetero
from Monitor.Controladora import Controladora,ListaDeVariables



raiz =  os.path.join(os.path.dirname(os.path.abspath(__file__)),"../..")
sys.path.append(raiz)





#import Conexiones.cliente as Servidor
#from Conexiones.Conexiones import Conexiones

'''DL17'''
#from encriptacionQR import codificar
#from configParser.viewData import viewData
'''DL17'''


from Interfaz import Interfaz
from Reloj import Reloj
#from Scanner import Scanner


class Tanque:
    """
    Clase utulizada para administrar el Tanque
    """
    #-------------------- Identificadores de dispositivos      
    MONEDERO_MDB = 1
    BILLETERO_MDB = 2
    HOPPER_01_CCTALK = 3
    HOPPER_02_CCTALK = 4
    HOPPER_03_CCTALK = 5
    VALIDADOR_CCTALK = 6
    BILLETERO_ACEPTADOR_ID003 = 7
    BILLETERO_RECICLADOR_ID003 = 8
    def __init__(self,variables,zona_id,tanque_id):
        self.zona_id = zona_id
        self.tanque_id = tanque_id
        
        self.tipo_controladora = ""
        self.encriptacion = ""
        self.nombre_sucursal = ""
        self.localidad_sucursal = ""
        self.server_ip_address = ""
        self.ip_address = ""
        self.id = ""
        self.id_sucursal = ""
        self.politicas = ""
        self.puerto = ""
        self.reloj = ""
        self.logs = ""


        #-------------------- Leer configuracion        
        self.vizualizar = ""
        #-------------------- Modo operacion 
        self.listaDeVariables = variables
        self.tarjeta_controladora = ""
        #-------------------- Diccionatrios
        self.informacion = "" 
        self.variables = "" 

        
        
        #-------------------- Secuencia operacion
        self.secuencia_operacion = 0
        self.duracion = 0
        self.nivel_completado = 0
        self.horario_inicio = 0
        self.horario_fin = 0
        self.minutos_faltantes = 0
        self.minutos_tratamiento = 0
        self.contador_segundos = 0
        self.hora_inicio_operacion = 0
        self.estado_operacion = 1

        #-------------------- Secuencia lectura boleto
        

        #-------------------- Modelos
        self.invernadero = ""
        self.zona = ""
        self.tratamiento = []
        self.horario = ""
        self.nutriente = ""
        self.planta = ""
        self.tanque = []
        self.sensor = []
        self.solucion = []


        #-------------------- Interfaces
        self.vista = ""
        self.api = ""

        self.inicializar()

        self.TON_01 = Temporizador("TON_01",2.5)
        
        print("Iniciando Cajero.")
        tarea1 = threading.Thread(target=self.run)
        tarea1.start()

    def __str__(self):
        return "Tanque {}: ".format(self.tanque_id)
    def run (self):
        self.funcionando = True
        listaDeVariables_tmp = 0
        self.hora_inicio_operacion = datetime.strptime(time.strftime("%H:%M:%S"), '%H:%M:%S')
        self.hora_inicio_operacion = time.time()

        while (self.funcionando):
            time.sleep(.8)
            self.TON_01.entrada = not self.TON_01.salida
            self.TON_01.actualizar()
            print(" #-------------------- Secuencia de operacion: ",self.secuencia_operacion)
            #print(" #-------------------- conexion a internet: ",self.servidor.estado_internet)
            #print(" #-------------------- conexion a servidor: ",self.servidor.estado_servidor)
            if self.secuencia_operacion == 0:
                #-------------------- Validar tratamiento
                self.variables.update(cancelar_pago=0)
                self.variables.update(operacion_recarga=0)
                self.variables.update(estado_operacion=self.estado_operacion)

                invernadero_id = 4
                tratamiento_valido = self.validar_operacion()
                #self.dispensar_cambio2(583)
                if tratamiento_valido == 1:
                    self.secuencia_operacion = 1
                else:
                    self.secuencia_operacion = 0

            if self.secuencia_operacion == 1:
                #-------------------- Validar sensores
                validacion = self.validar_sensores()
                if validacion == 1:
                    self.secuencia_operacion = 2
                else:
                    self.secuencia_operacion = 0

            if self.secuencia_operacion == 2:
                #-------------------- Aplicar tratamiento
                validacion = self.validar_sensores()
                if validacion == 1:
                    self.secuencia_operacion = 3
                else:
                    self.secuencia_operacion = 0
            if self.secuencia_operacion == 3:
                #-------------------- Operacion nivel bajo
                monto_completado = self.actualiza_cobro(listaDeVariables_tmp)
                self.variables.update(interfaz=2)
                if monto_completado == 1:
                    self.secuencia_operacion = 4
                else:
                    self.secuencia_operacion = 3

            if self.secuencia_operacion == 4:
                #-------------------- Operacion llenado
                operacion_validada = self.validar_operacion()
                if operacion_validada == 1:
                    self.secuencia_operacion = 8
                else:
                    self.secuencia_operacion = 5
                
            if self.secuencia_operacion == 5:
                #-------------------- Operacion vaciado
                combrobante_error = self.secuencia_error()
                if combrobante_error == 1:
                    self.secuencia_operacion = 7
                else:
                    print("No se pudo expedir el comprobante de error")

            if self.secuencia_operacion == 6:
                #-------------------- Operacion ajuste nivel 
                self.variables.update(interfaz=1)
                self.variables.update(cancelar_pago=2)
                secuencia_exitosa = self.secuencia_ajuste_nivel()
                if secuencia_exitosa == 1:
                    self.secuencia_operacion = 0
                else:
                    self.secuencia_operacion = 7
                    print("Ocurrio un error [6]")


            if self.secuencia_operacion == 7:
                #-------------------- Error en la operacion
                self.cajero_suspendido()

            if self.secuencia_operacion == 8:
                #-------------------- Finalizar operacion y reiniciar valores
                operacion_finalizada = self.finalizar_operacion()
                self.secuencia_operacion = 0
            
            if self.secuencia_operacion == 9:
                #-------------------- Operacion recarga
                self.variables.update(operacion_recarga=2)
                self.variables.update(interfaz=2)
                operacion_finalizada = self.recargar()

            fecha = time.strftime("%Y-%m-%d %H:%M:%S")
            
            


            """
            self.variables.update(monto_ingresar=self.monto_ingresar)
            self.variables.update(monto_ingresado=self.monto_ingresado)
            self.variables.update(monto_a_dispensar=self.monto_a_dispensar)
            self.variables.update(folio=self.folio)
            self.variables.update(hora_entrada=self.hora_entrada)
            print("te",self.tiempo_estacionado)
            self.variables.update(tiempo_estacionado=self.tiempo_estacionado)
            self.variables.update(descuento=self.descuento)
            self.variables.update(fecha=fecha)
            """
            self.variables.update(ph=self.listaDeVariables.X[1].obtenerValor())
            self.variables.update(ec=self.listaDeVariables.X[2].obtenerValor())
            self.variables.update(temperatura=self.listaDeVariables.X[3].obtenerValor())
            self.variables.update(nivel=self.listaDeVariables.X[4].obtenerValor())


            self.variables.update(nivel_completado=round((self.nivel_completado*100)/self.minutos_tratamiento,1))
            self.variables.update(minutos_tratamiento=self.minutos_tratamiento)
            self.variables.update(fecha=fecha)

            self.leer_sensores()
            #sensores.update(monto=i)
            #response = cajero.enviar(informacion)
            respuesta = self.enviar(self.variables)

            self.validar_respuesta(respuesta)
            #print(respuesta)



    def inicializar(self):
        
        #shutil.copy(ruta+"configParser/configuracion.ini", ruta+"configParser/configuracion_respaldo.ini")
        #shutil.copy(ruta+"configParser/sensores.ini", ruta+"configParser/sensores_respaldo.ini")

        #-------------------- Establecer vista 
        self.vista = Interfaz('http://127.0.0.1:8000/hook/')
        self.vista.establecer_lista_de_variables(self.listaDeVariables)
        body = ""
        metodo = "POST"
        self.vista.establecer_metodo(metodo)
        self.vista.establecer_encabezado({'Content-Type': 'application/json'})
        #-------------------- Establecer API 
        self.api = Interfaz('http://127.0.0.1:8000/api/')
        self.api.establecer_lista_de_variables(self.listaDeVariables)
        body = ""
        metodo = "GET"
        self.api.establecer_metodo(metodo)
        self.api.establecer_encabezado({'Content-Type': 'application/json'})

        self.tipo_controladora = 0
        #-------------------- Leer configuracion        
        #self.vizualizar = viewData('configuracion.ini')
        self.leer_configuracion(self.zona_id)

        #-------------------- Modo operacion 
        #####self.tarjeta_controladora = self.establecer_tarjeta_controladora(self.listaDeVariables)

        #-------------------- configurar dispositivos 
        self.configurar_dispositivos()

        #-------------------- configurar servidores 
        self.configurar_servidores()
        self.configurar_reloj()
        
        self.logs = GuardarLogs("log")

        time.sleep(5)

        
        
        self.variables = dict (
        interfaz = 6,
        operacion_recarga = 0,
        nivel = 0,
        ph = 0,
        ec = 0,
        temperatura = 0,
        estado_operacion = 0,
        z_01 = 0, # Alerta Nivel
        z_02 = 0, # Alerta PH
        z_03 = 0, # Alerta EC
        z_04 = 0, # Alerta Temperatura
        z_05 = 0, # Alerta Solucion 1
        z_06 = 0, # Alerta Solucion 2
        z_07 = 0, # Alerta Solucion 3
        z_08 = 0, # Alerta Solucion 4
        z_09 = 0, # Alerta Solucion 5
        z_10 = 0, # Alerta Placa de control
        z_11 = 0, # Alerta Flujo de agua
        z_12 = 0, # Alerta Bomba de extraccion
        )


    def obtenerEquipo(self,equipo): 
        return self.equipo 
    def obtenerControladora(self,controladora): 
        return self.controladora 
    def obtenerTarifas(self,tarifa): 
        return self.tarifa 
    def obtenerSensores(self,sensor): 
        return self.sensor 
    def obtenerDispositivos(self,dispositivo): 
        return self.dispositivo 
    def obtenerVista(self,vista): 
        return self.vista 

    def establecerPuerto (self, puerto):
        self.puerto = puerto
    def establecerEquipo(self,equipo): 
        self.equipo = equipo
    def establecerControladora(self,controladora): 
        self.controladora = controladora
    def establecerTarifas(self,tarifa): 
        self.tarifa = tarifa
    def establecerSensores(self,sensor): 
        self.sensor = sensor
    def establecerDispositivos(self,dispositivo): 
        self.dispositivo = dispositivo
    def establecerVista(self,vista): 
        self.vista = vista

    


    def establecer_tarjeta_controladora(self,tipo): 
        if self.controladora[0]['modo_operacion'] == "Expedidor":
            if self.controladora[0]['tipo'] == "Controladora Arduino":        
                controladora = Controladora(self.listaDeVariables, 
                    tarjeta = Controladora.TARJETA_DE_INTERFAZ_ARDUINO,
                    tipoDeControladora = Controladora.CONTROLADORA_PARA_EXPEDIDORA_VALIDADORA)
            elif self.controladora[0]['tipo'] == "Controladora Raspberry":
                controladora = Controladora(self.listaDeVariables, 
                    tarjeta = Controladora.TARJETA_DE_INTERFAZ_BLANCA,
                    tipoDeControladora = Controladora.CONTROLADORA_PARA_EXPEDIDORA_VALIDADORA)
            elif self.controladora[0]['tipo'] == "Controladora Raspberry Negra":
                controladora = Controladora(self.listaDeVariables, 
                    tarjeta = Controladora.TARJETA_DE_INTERFAZ_NEGRA,
                    tipoDeControladora = Controladora.CONTROLADORA_PARA_EXPEDIDORA_VALIDADORA)
            elif self.controladora[0]['tipo'] == "Controladora Pulso":
                controladora = Controladora(self.listaDeVariables, 
                    tarjeta = Controladora.TARJETA_DE_PULSO,
                    tipoDeControladora = Controladora.CONTROLADORA_PARA_EXPEDIDORA_VALIDADORA)

        return 0

    def obtener_tanque(self,zona_id):
        #-------------------- Obtener tanques por zona seleccionada    
        body = ""
        metodo = "GET"
        self.api.establecer_url('http://127.0.0.1:8000/api/tanque/?zona={}'.format(self.zona['id']))
        self.api.establecer_metodo('GET')
        self.api.establecer_encabezado({'Content-Type': 'application/json'})
        respuestas = self.api.enviar(Interfaz.PROCESO,body)
        for i,respuesta in enumerate(respuestas):
            if respuesta['activo'] == True:
                if respuesta['id'] == self.tanque_id:
                    self.tanque = respuesta
                    #self.tanque.append(respuesta)
        return self.tanque
    
    def obtener_sensor(self,tanque_id):
         #-------------------- Leer sensores por tanque seleccionado 
        body = ""
        metodo = "GET"
        self.api.establecer_url('http://127.0.0.1:8000/api/sensor/?tanque={}'.format(tanque_id))
        self.api.establecer_metodo('GET')
        self.api.establecer_encabezado({'Content-Type': 'application/json'})
        respuestas = self.api.enviar(Interfaz.PROCESO,body)
        for i,respuesta in enumerate(respuestas):
            if respuesta['activo'] == True:
                self.sensor.append(respuesta)
        return self.sensor

    def obtener_solucion(self,soluciones):
         #-------------------- Leer sensores por tanque seleccionado 
        for i,solucion in enumerate(soluciones):
            body = ""
            metodo = "GET"
            self.api.establecer_url('http://127.0.0.1:8000/api/solucion/{}'.format(solucion))
            self.api.establecer_metodo('GET')
            self.api.establecer_encabezado({'Content-Type': 'application/json'})
            respuesta = self.api.enviar(Interfaz.PROCESO,body)
            self.solucion.append(respuesta)
        return self.solucion
    
    def obtener_horario(self,horario):
        body = ""
        metodo = "GET"
        self.api.establecer_url('http://127.0.0.1:8000/api/horario/{}/'.format(horario))
        self.api.establecer_metodo('GET')
        self.api.establecer_encabezado({'Content-Type': 'application/json'})
        self.horario = self.api.enviar(Interfaz.PROCESO,body)


    def leer_configuracion(self,zona_id):
        #interfaz_api = Interfaz('http://127.0.0.1:8000/api/')
        ### ------------------------------- Leer configuracion de equipo
        body = ""
        metodo = "GET"
        self.api.establecer_url('http://127.0.0.1:8000/api/')
        self.api.establecer_metodo('GET')
        self.api.establecer_encabezado({'Content-Type': 'application/json'})
        modelos = self.api.enviar(Interfaz.PROCESO,body)
        #datos = self.api.response[0]
        #print(response)

       

        #-------------------- Leer tratamiento por zona seleccionada    
        body = ""
        metodo = "GET"
        self.api.establecer_url('http://127.0.0.1:8000/api/zona/{}/'.format(zona_id))
        self.api.establecer_metodo('GET')
        self.api.establecer_encabezado({'Content-Type': 'application/json'})
        respuesta = self.api.enviar(Interfaz.PROCESO,body)
        self.zona = respuesta

        #-------------------- Leer tratamiento por zona seleccionada    
        body = ""
        metodo = "GET"
        self.api.establecer_url('http://127.0.0.1:8000/api/tratamiento/{}/'.format(self.zona['tratamiento_id']))
        self.api.establecer_metodo('GET')
        self.api.establecer_encabezado({'Content-Type': 'application/json'})
        respuesta = self.api.enviar(Interfaz.PROCESO,body)
        self.tratamiento = respuesta
            
        
        self.obtener_horario(self.tratamiento['horario_id'])
        self.obtener_tanque(self.zona['id'])
        sensores = self.obtener_sensor(self.tanque['id'])
        soluciones = self.obtener_solucion(self.tratamiento['solucion_id'])

        self.duracion = int(self.tratamiento['duracion'])
        self.nivel_completado = int(self.tratamiento['nivel_completado'])
        self.horario_inicio =  datetime.strptime(self.horario['horario_inicio'], '%H:%M:%S')
        self.horario_fin =  datetime.strptime(self.horario['horario_fin'], '%H:%M:%S')
        self.minutos_tratamiento = ((self.horario_fin - self.horario_inicio).seconds)/60
        self.minutos_faltantes = self.minutos_tratamiento * self.duracion
        self.minutos_tratamiento = self.minutos_tratamiento * self.duracion

        """
        #-------------------- Leer sensores por tanque seleccionado 
        body = ""
        metodo = "GET"
        self.api.establecer_url('http://127.0.0.1:8000/api/sensor/?tanque={}'.format(self.tanque[0]['id']))
        self.api.establecer_metodo('GET')
        self.api.establecer_encabezado({'Content-Type': 'application/json'})
        respuestas = self.api.enviar(Interfaz.PROCESO,body)
        self.sensor = respuestas


        

        if isinstance(modelos, (dict)):
            print("### -------------------------------Configuracion de equipo ")
            for i,modelo in enumerate(modelos):
                if modelo != 'transaccion' and modelo != 'servicio':
                    self.api.establecer_url('http://127.0.0.1:8000/api/{}/'.format(modelo))
                    campos = self.api.enviar(Interfaz.PROCESO,body)
                    if modelo == "invernadero":
                        self.invernaderos = campos
                    if modelo == "zona":
                        self.zona = campos
                    if modelo == "tratamiento":
                        self.tratamiento = campos
                    if modelo == "horario":
                        self.horario = campos
                    
                    if modelo == "solucion":
                        self.solucion = campos

                    if modelo == "nutriente":
                        self.nutriente = campos

                    if modelo == "tanque":
                        self.tanque = campos

                    if modelo == "sensor":
                        self.sensor = campos

                    if isinstance(campos, (list)):
                        for i,campo in enumerate(campos):
                            print("### -------------------------------Configuracion de {} {}".format(modelo,i+1))
                            for valor in campo:
                                print(valor + " : " + str(campo[valor]))



        for i,tratamiento in enumerate(self.tratamiento):
            if tratamiento['activo'] == True:
                #if tratamiento[]
                self.tratamiento = self.leer_tratamiento(tratamiento['tratamiento_id'])
        
        for i,zona in enumerate(self.zona):
            if zona['activo'] == True:
                self.zona = zona

        for i,tratamiento in enumerate(self.tratamiento):
            if tratamiento['activo'] == True:
                if tratamiento['id'] == self.zona['tratamiento_id']:
                    self.tratamiento = tratamiento
                    self.duracion = int(self.tratamiento['duracion'])
                    self.nivel_completado = int(self.tratamiento['nivel_completado'])
                    self.horario_inicio =  datetime.strptime(self.horario[0]['horario_inicio'], '%H:%M:%S')
                    self.horario_fin =  datetime.strptime(self.horario[0]['horario_fin'], '%H:%M:%S')
                    self.minutos_tratamiento = ((self.horario_fin - self.horario_inicio).seconds)/60
                    self.minutos_faltantes = self.minutos_tratamiento * self.duracion
                    self.minutos_tratamiento = self.minutos_tratamiento * self.duracion

        for i,tanque in enumerate(self.tanque):
            if tanque['activo'] == True:
                if tanque['zona_id'] == self.zona['id']:
                    self.tanque = tanque

        
        for i,sensor in enumerate(self.sensor):
            if sensor['activo'] == True:
                if sensor['tanque_id'] == self.tanque['id']:
                    self.sensor
                self.tratamiento = self.leer_tratamiento(sensor['tratamiento_id'])
        
        return 0
    """
    
    def enviar(self,datos):
        self.vista.enviar(Interfaz.PROCESO,datos)
        #print(self.vista.response)
        return self.vista.response
    def operacion_cobro(self):
        pass
    
        
    
    def configurar_reloj(self):
        self.reloj =  Reloj(self.horario['intervalo_descanso'],self.horario['tiempo_descanso'])
        return 1
    def configurar_servidores(self):
        #self.servidor =  Servidor()
        return 1
    def configurar_dispositivos(self):
        return 1
    
    def leer_sensores(self):
        contador = 0
        #print(self.puerto.puertoAbierto)
        for i,sensor in enumerate(self.sensor):
            if sensor['tipo'] == "NIVEL":
                pass
                #print("Direccion de envio: {} ".format(sensor['puerto']))
            if sensor['tipo'] == "PH":
                pass
                #print("Direccion de envio: {} ".format(sensor['puerto']))
            if sensor['tipo'] == "Conductividad electrica":
                pass
                #print("Direccion de envio: {} ".format(sensor['puerto']))
        if self.puerto.puertoAbierto:
            #while contador <= 1:
            #print ("{}: Deshabilitando".format(self))
            a = "&{},{},{}*".format(1,'sensores',1)
            #a = "&{},{},{}*".format(5,'extraer',2000)
            #a = "&{},{},{}*".format(9,'dosificar',9)
            #print(a.encode())
            self.puerto.write(a.encode())
            time.sleep(.025)
            #time.sleep(1)
            try:
                #Try para la decodificacion
                validacion = 0
                r = self.puerto.read(50).decode('utf-8')
                #r = b'0'
                print ("{}: {}".format("Datos", r))
                if r:
                    #print(r[0])
                    if validacion == 0:
                        if r[0] == '&':
                            validacion = 1
                    if validacion == 1:
                        #print("#############",r[len(r)-3:len(r)-2])
                        if r[len(r)-3:len(r)-2] == '*':
                            validacion = 2
                            r = r[1:len(r)-3]
                            #print(r)
                        else:
                            print("Datos invalidos")
                    if validacion == 2:
                        sensor = r.split(",")
                        #print(sensor)
                        if sensor[0]:
                            self.listaDeVariables.X[1].establecerValor(float(sensor[0])) # Sensor PH
                        else:
                            self.listaDeVariables.X[1].establecerValor(str(-1)) # Sensor PH

                        if sensor[1]:
                            self.listaDeVariables.X[2].establecerValor(float(sensor[1])) # Sensor Ec
                        else:
                            self.listaDeVariables.X[2].establecerValor(str(-1)) # Sensor Ec
                        
                        if sensor[2]:
                            self.listaDeVariables.X[3].establecerValor(float(sensor[2])) # Sensor Ec
                        else:
                            self.listaDeVariables.X[3].establecerValor(str(-1)) # Sensor Temperatura
                        if sensor[3]:
                            self.listaDeVariables.X[4].establecerValor(float(sensor[3])) # Sensor Nivel
                        else:
                            self.listaDeVariables.X[4].establecerValor(str(-1)) # Sensor Nivel

            except:
                print("No se puede decodificar")

            #contador += 1


    def validar_sensores(self):
        nivel = self.variables.get('nivel')
        ph = self.variables.get('ph')
        ec = self.variables.get('ec')
        temperatura = self.variables.get('temperatura')
        self.puerto
        # NOTA: Que el nivel maximo de agua contemple la reduccion de EC (Agua) y elevacion de PH (Agua)
        for i,sensor in enumerate(self.sensor):
            if sensor['tipo'] == "NIVEL":
                if nivel:
                    if nivel <= float(sensor['valor_minimo']):
                        print(colored("nivel bajo detectado",'yellow'),nivel)
                        self.variables.update(z_01=1)
                    if nivel >= float(sensor['valor_maximo']):
                        print(colored("nivel alto detectado",'yellow'),nivel)
                        self.variables.update(z_01=1)
                    else:
                        self.variables.update(z_01=2)

                else:
                    print(colored("Sensor de nivel fuera de posicion o desconectado",'yellow'),nivel)
                    self.variables.update(z_01=-1)

            if sensor['tipo'] == "PH":
                #ph = 8
                if ph:
                    ph_base = (float(sensor['valor_maximo']) + float(sensor['valor_minimo']))/2
                    if ph <= float(sensor['valor_minimo']):
                        print(colored("Ph bajo detectado. ",'yellow'),ph)
                        self.variables.update(z_02=1)
                    if ph >= float(sensor['valor_maximo']):
                        print(colored("Ph alto detectado",'yellow'),ph)
                        self.ajustar_tratamiento(ph,ph_base,"Ph reductor")
                        self.variables.update(z_02=1)
                    else:
                        self.variables.update(z_02=2)
                else:
                    print(colored("Sensor de ph fuera de posicion o desconectado",'yellow'),ph)
                    self.variables.update(z_02=-1)

            if sensor['tipo'] == "Conductividad electrica":
                if ec:
                    ec_base = (float(sensor['valor_maximo']) + float(sensor['valor_minimo']))/2
                    if float(ec) <= float(sensor['valor_minimo']):
                        print(colored("EC bajo detectado",'yellow'),ec)
                        self.ajustar_tratamiento(ec,ec_base,"Ec elevador")
                        self.variables.update(z_03=1)
                    if float(ec) >= float(sensor['valor_maximo']):
                        print(colored("EC alto detectado",'yellow'),ec)
                        self.variables.update(z_03=1)
                    else:
                        self.variables.update(z_03=2)

                else:
                    print(colored("Sensor de EC fuera de posicion o desconectado",'yellow'),ec)
                    self.variables.update(z_03=-1)

                
            if sensor['tipo'] == "TEMPERATURA":
                if temperatura:
                    if temperatura <= float(sensor['valor_minimo']):
                        print(colored("temperatura bajo detectado",'yellow'),temperatura)
                        self.variables.update(z_04=1)
                    if temperatura >= float(sensor['valor_maximo']):
                        print(colored("temperatura alto detectado",'yellow'),temperatura)
                        self.variables.update(z_04=1)
                    else:
                        self.variables.update(z_04=2)

                else:
                    print(colored("Sensor de temperatura fuera de posicion o desconectado",'yellow'),temperatura)
                    self.variables.update(z_04=-1)


        if nivel <= self.tratamiento['ajuste_nivel']:
            #LOG2
            #self.secuencia_operacion = 5
            print(colored("Ajuste al nivel detectado",'yellow'),nivel)  
        try:
            self.logs.print(self.variables)  
        except:
            print("No se pudieron guardar los logs")      
        return 0


    def ajustar_tratamiento(self,valor_actual,valor_base,tipo):
       for i,solucion in enumerate(self.solucion):
            if solucion['tipo'] == tipo:
                direccion = solucion['direccion'] #Ej: ph = 1 grado , tds = 100 ppm
                aplicacion = float(solucion['aplicacion']) #Ej: ph = 1 grado , tds = 100 ppm
                escala = float(solucion['escala']) #Ej: ph = 1 grado , tds = 100 ppm
                litros_actuales = float(self.tanque['valor_actual']) #Cantidad de litros actuales en el tanque
                #factor = (litros_actuales * aplicacion)/1000
                factor = litros_actuales * aplicacion
                if "reductor" in solucion['tipo']:
                    valor_a_ajustar = valor_actual - valor_base
                else:
                    valor_a_ajustar = valor_base - valor_actual  
                cantidad_a_ajustar = (valor_a_ajustar * factor)/escala
                print(colored("direccion: {} aplicacion: {} escala: {} litros_actuales: {} factor: {} valor_a_ajustar: {} cantidad_a_ajustar: {}".format(direccion,aplicacion, escala, litros_actuales, factor, valor_a_ajustar, cantidad_a_ajustar),'blue'))
                self.aplicar_solucion(cantidad_a_ajustar,direccion,tipo)



            


    def aplicar_solucion(self,cantidad_a_ajustar,direccion,tipo):
        aplicaciones = cantidad_a_ajustar 
        a = ""
        if tipo == "Ph reductor":
            a = "{},{},{}*".format(direccion,'dosificar',aplicaciones)
        if tipo == "Ec elevador":
            """
                Considerando 12v a la entrada se calcula que se aplicarian 440 Litros x Hora 
                Equivalente a:
                7.3333333333 Litros x Minuto.
                Equivalente a:
                122.222222222 mililitros x 1000 milisegundos (segundo)
            """
            factor_bomba = 122.22
            aplicaciones = (aplicaciones * 1000)/12
            print("Mililitros a aplicar: ",aplicaciones)
            a = "&{},{},{}*".format(direccion,'extraer',aplicaciones)
        if tipo == "Solucion nutritiva":
            a = "&{},{},{}*".format(direccion,"establecer",cantidad_a_ajustar)
        print(a.encode())
        self.puerto.write(a.encode())
        """time.sleep(.025)
        try:
            #Try para la decodificacion
            validacion = 0
            r = self.puerto.read(25).decode('utf-8')
            #r = b'0'
            print ("{}: {}".format("Datos", r))
            if r:
                print(r[0])
        except:
            print("No se pudo decodificar")
        """

    def validar_respuesta(self,respuesta):
        #print("Respuesta: ",respuesta['status'])
        #print("Respuesta: ",type(respuesta),respuesta)
        """ 
        if respuesta['cancelar_pago'] == 1:
            self.secuencia_operacion = 6
            
        if respuesta['operacion_recarga'] == 1:
            self.secuencia_operacion = 9
        """
        #if respuesta['descuento'] > 0:
        #    self.descuento = respuesta['descuento']
        return 1


            
    


    

   
    def validar_operacion(self):
        #Anotacion: No funciona el horario nocturno debido a que hay que considerar que el horario_fin corresponde al dia de mañana

        #self.boleto = "M,60,1,26'03'2020,10Ñ30Ñ12"

        #for i,zona in enumerate(self.zona):
        if self.zona['activo'] == True:
            if self.zona['id'] == self.zona_id:
                if self.tratamiento:
                    hora_actual =  datetime.strptime(time.strftime("%H:%M:%S"), '%H:%M:%S')
                    # print("porcentaje completado: ",colored(self.nivel_completado,'red'))
                    # print("porcentaje tratamiento: ",colored(self.minutos_tratamiento,'red'))
                    # print("horario inicio: ",colored(self.horario_inicio.time(),'red'))
                    # print("horario fin: ",colored(self.horario_fin.time(),'red'))
                    # print("hora actual: ",colored(hora_actual,'red'))
                    # print("hora actual: ",colored(self.horario['intervalo_descanso'],'red'))
                    # print("hora actual: ",colored(self.horario['tiempo_descanso'],'red'))
                    #print("hora actual: {} {} ".format(hora_actual,self.hora_inicio_operacion),colored("....",'red'))
                    #self.contador_segundos = int(elapsed_time)

                    if self.nivel_completado < self.minutos_tratamiento:
                        print("Minutos completados",colored(self.nivel_completado,'green'))
                        #if hora_actual > self.horario_inicio.time() and hora_actual < self.horario_fin.time():
                        if self.horario_inicio <= hora_actual <= self.horario_fin :
                            

                            #self.contador_segundos = self.contador_segundos + 1
                            #self.contador_segundos = int(time.time () - self.hora_inicio_operacion)
                            self.contador_segundos = self.reloj.obtener_segundos()
                            self.estado_operacion = self.reloj.obtener_estado()
                            direccion = 0
                            for i,solucion in enumerate(self.solucion):
                                if "Nutritiva" in solucion['tipo']:
                                    direccion = solucion['direccion'] #Ej: ph = 1 grado , tds = 100 ppm
                            if self.estado_operacion:   
                                print(colored("[Operando]: ",'green'),self.contador_segundos)
                                self.aplicar_solucion(1,direccion,"Solucion nutritiva")
                            else:
                                print(colored("[Descanso]: ",'red'),self.contador_segundos)
                                self.aplicar_solucion(0,direccion,"Solucion nutritiva")
                            operacion_validada = False

                            '''
                            if self.contador_segundos % 60 == 0 and self.estado_operacion:
                                print(colored("Horario valido: ",'green'),self.contador_segundos)
                                self.nivel_completado = self.nivel_completado + 1
                                self.actualizar_nivel()
                                #LOG1
                                print(colored("Actualizando valores",'magenta'),self.nivel_completado)
                                operacion_validada = True
                            '''
                            '''
                            if self.contador_segundos % 60 == 0 and self.estado_operacion and self.contador_segundos:
                                print(colored("Horario valido: ",'green'),self.contador_segundos)
                                self.nivel_completado = self.nivel_completado + 1
                                self.actualizar_nivel()
                                #LOG1
                                print(colored("Actualizando valores",'magenta'),self.nivel_completado)
                                operacion_validada = True

                            if self.contador_segundos == (self.horario['intervalo_descanso']*60) and self.estado_operacion:
                                print(colored("Deteniendo: ",'red'),self.horario['intervalo_descanso']*60)
                                self.contador_segundos = 0
                                self.hora_inicio_operacion = time.time()
                                self.estado_operacion = 0
                            
                            if not self.estado_operacion:
                                tiempo_total = self.horario['tiempo_descanso']*60
                                print(colored("Tiempo de descanso: ",'red'),self.contador_segundos,tiempo_total)
                                #if self.contador_segundos % tiempo_total == 0:
                                if self.contador_segundos == tiempo_total:
                                    self.contador_segundos = 0
                                    self.hora_inicio_operacion = time.time()
                                    self.estado_operacion = 1
                            '''
                            if self.contador_segundos % 59 == 0 and self.estado_operacion and self.contador_segundos:
                                print(colored("Horario valido: ",'green'),self.contador_segundos)
                                self.nivel_completado = self.nivel_completado + 1
                                self.actualizar_nivel()
                                #LOG1
                                print(colored("Actualizando valores",'magenta'),self.nivel_completado)
                                operacion_validada = True
                                
                            
                                

                            if operacion_validada:
                                return 1
                            else:
                                return 0
                        else:
                            print(colored("Horario de operacion terminado: ",'red'),hora_actual)
                            return 0
                    else:
                        print("Tratamiento terminado: ",colored(self.nivel_completado,'red'))
                        return 0
                else:
                    print(colored("No se encontro un tratamiento: ",'red'))
            else:
                print(colored("No se encontro la zona: ",'red'))


        else:
            print(colored("No se encontro ningun invernadero: ",'red'))

    def leer_tratamiento(self,tratamiendo_id):
        for i,tratamiento in enumerate(self.tratamiento):
             if tratamiento['activo'] == True:
                if tratamiento['id'] == tratamiendo_id:
                    print("Tratamiento seleccionado: ",tratamiendo_id)
                    return tratamiento
        return 0
        
    def actualizar_nivel(self):
        
        metodo = "GET"
        self.api.establecer_url('http://127.0.0.1:8000/api/tratamiento/{}/'.format(self.tratamiento['id']))
        self.api.establecer_metodo(metodo)
        self.api.establecer_encabezado({'Content-Type': 'application/json'})
        body = self.api.enviar(Interfaz.PROCESO,"")
        body.update(nivel_completado=self.nivel_completado)

        metodo = "PUT"
        self.api.establecer_url('http://127.0.0.1:8000/api/tratamiento/{}/'.format(self.tratamiento['id']))
        self.api.establecer_metodo(metodo)
        self.api.establecer_encabezado({'Content-Type': 'application/json'})
        response = self.api.enviar(Interfaz.PROCESO,body)
        print("Respuesta: ",response)


    def reiniciar_variables(self):
        #-------------------- Secuencia cobro
        self.secuencia_operacion = 0
        self.monto_ingresar = 0
        self.monto_ingresado = 0
        self.monto_a_dispensar = 0
        self.descuento = 0
        self.cancelar_pago = 0
        self.tarifa_seleccionada = 0

        
    def ejecutar_programa(self):
        pass
    def secuencia_error(self):
        return 1
    def secuencia_ajuste_nivel(self):
        return 1
    def finalizar_operacion(self):
        self.reiniciar_variables()
        return 1
    
    def restar_hora(self,horab,fechab):
        horab = horab.split(':',2)
        fechab = fechab.split('-')
        fechaBoleto = datetime.strptime(str(fechab[0]) + str(fechab[1]) + str(fechab[2]), '%Y%m%d').date()
        horaBoleto = datetime.strptime(str(horab[0]) +':'+str(horab[1]) +':'+ str(horab[2]), '%H:%M:%S').time()
        fechaActual=datetime.now().date()
        horaActual=datetime.now().time()
        horayFechaBoleto = datetime.now().combine(fechaBoleto, horaBoleto)
        horayFechaActual = datetime.now().combine(fechaActual, horaActual)
        restaFechas = horayFechaActual - horayFechaBoleto
        aux_dif=(str(restaFechas).split('.',1))[0]
        dias = int(restaFechas.days)
        segundos = restaFechas.seconds 
        return dias,segundos,aux_dif

    
class EjecutarPrograma():
    def __init__(self, listaDeVariables):

        self.listaDeVariables = listaDeVariables

        self.TON_01 = Temporizador("TON_01",0.5)
        self.TON_02 = Temporizador("TON_02",0.5)
        self.TON_03 = Temporizador("TON_03",2)
        self.TON_04 = Temporizador("TON_04",15)

        self.aux = 0
        self.aux_2 = 0

        tarea1 = threading.Thread(target=self.run)
        tarea1.start()

    def run (self):
        self.funcionando = True

        while (self.funcionando):
            self.TON_02.entrada = not self.TON_02.salida
            self.TON_02.actualizar()

            if self.TON_02.salida:
                """
                print ("\n", end='')
                self.listaDeVariables.imprimirX(8)
                print ("", end="\t")
                self.listaDeVariables.imprimirY(8)
                print ("", end="\t")
                self.listaDeVariables.imprimirZ()
                print ("", end=" ")
                """

                self.TON_01.entrada = self.aux
                self.TON_01.actualizar()

                
                



def main():
    variables = ListaDeVariables()
    #variables = 0
    
   

    puerto = PuertoSerie("Puerto Serie")
    print ("Imprimiendo Arduino", PuertoSerie.ARDUINO_UNO)
    puerto.modificarConfiguracion(dispositivo = PuertoSerie.ARDUINO_UNO)
    puerto.modificarConfiguracion(baudrate = "9600")
    #puerto.start()
    try:
        puerto.abrirPuerto()
        print ("Puerto Abridooooooo")
        
    except:
        puerto = 0
        print ("No se abrio el puerto")


    tanque = Tanque(variables,1,1)
    tanque.establecerPuerto(puerto)

    


if __name__ == "__main__":
    main()
