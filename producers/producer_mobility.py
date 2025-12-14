import os
import time
import random
import json
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='kafka-kraft:9092')
TOPIC = 'telemetry-mobility'

battery = 100.0
charging = False

def get_mobility_data():
    global battery, charging        # le decimos a Python que vamos a usar y modificar las variables gloables
    
    if charging:        # Si está cargando
        battery += random.uniform(0.5, 2.0)
        if battery >= 100:
            battery = 100
            charging = False
    else:           # Sino está cargando 
        battery -= random.uniform(0.1, 0.5)
        if battery <= 10:   # Si se queda con 10% o menos se pone en modo carga
            charging = True
            
    rpm = random.uniform(1000, 5000)            # El valor de las revoluciones del motos es un valor aleatorio en un rango considerable
    traction = random.uniform(0.8, 1.0)         # agarre de las ruedas inicia con un buen porcentaje

    if random.random() < 0.1:           # cada cierto tiempo --> 10% de las veces
        traction = random.uniform(0.1, 0.4)             # la tracción baja drásticamente --> simula terreno complicado cada cierto tiempo

    # line = f"mobility,unit=rover-01 battery={battery:.2f},rpm={int(rpm)},traction={traction:.2f}"    ¿?
    line = f"mobility,unit=rover-01 battery_voltage={battery:.2f},rpm={int(rpm)},traction={traction:.2f}"           # usa el formato Influx Line Protocol: (measurement,tag1=valor1 tagfield1=...,field2=...,field3=... timestamp(opcional))

    return line.encode('utf-8')         # KafkaProducer espera los mensajes como bytes, no como string

while True:
    for _ in range(20):         # envia ráfaga de 20 mensajes con actualizaciones constantes cada 0.1 seg --> 2 seg en enviar la ráfaga completa
        producer.send(TOPIC, get_mobility_data())       # cada productor envia al topic seleccionado los mensajes de forma síncrona (al mismo tiempo)
        time.sleep(0.1)         # añade un pequeño espacio (~0.1 segundos) entre mensajes → no saturas instantáneamente
    
    producer.flush()            # Fuerza a que todos los mensajes pendientes se envíen ya al broker --> Garantiza que nada se quede en el buffer del cliente
    print("Mobility was send.")
    time.sleep(10)          # Espera 10 seg y vuelve a enviar otra ráfaga