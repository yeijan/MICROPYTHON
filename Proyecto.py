#___Importacion de librerias requeridas
from machine import Pin, ADC
import network
import time
import ujson
import ufirebase as firebase


#___Url BD FireBase
firebase.setURL("https://bdsensor-18efe-default-rtdb.firebaseio.com/")

#___Coneccion Wifi
print("Conectando a la red")
sta_if=network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('Y2K','Ye850915*')
while not sta_if.isconnected():
    print("*", end ="")
    time.sleep(0.50)
print("Conectado", end="")

#___Creacion Objetos Led
ledRojo = Pin(19, Pin.OUT)
ledAzul =Pin(18, Pin.OUT)

#___Creacion Objeto Rele
Rele=Pin(33,Pin.OUT)

#Creacion y Calibra Sensor
sensor=ADC(Pin(32))
sensor.atten(ADC.ATTN_11DB)
sensor.width(ADC.WIDTH_10BIT)

#___Definicion de variable con valores
ppmA=100 #Partes Por Millon Aceptable
ppmN=78  #Parte Por Millon Aceptado, Calculo para un espacio con area de un metro cuadrado

#___Logica de programación
while True:
#___Lectura datos sensor
    datosensor=sensor.read()
#___Calculo de partes por millos, 1200 valor mortal para el ser humano, 4095, valor calibrado del sensor
    ppm= datosensor * 1200/4095
#___Evalua si las partes por millon son menores a las partes Normales
    #si es asi, apaga led rojo, apaga rele, enciende led azul
    if ppm < ppmN:
        ledRojo.off()
        Rele.value(0)
        ledAzul.on()
#___ En caso contrario, enciende led rojo, apaga led azul, enciende rele
    else :
        ledRojo.on()
        Rele.value(1)
        ledAzul.off()
#___Se imprimen las partes por millon obtenidas
    print(f"Partes por millon de CO2 {ppm}")
#___Se almacena en formato Json, los valores de partes por millon obtenidos
    message={"co2":ppm}
#___Se envia a la base de datos en firebase
    firebase.put("SENSORAMBSOLDADURA",message,bg=0)
#___Mensaje de confirmacion de dato enviado
    print("Dato Enviado")
#___Temporisador par retardar un segundo el proceso.
    time.sleep(1)
    
 
    
