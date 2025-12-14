import os
import time
import random
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='kafka-kraft:9092')
TOPIC = 'telemetry-eclss'

def get_eclss_data():

    temp = random.uniform(-170, 120)                # Esto refleja el rango extremo típico del entorno lunar (muy frío en sombra, muy caliente al sol)
    pressure = random.uniform(95, 105)              # Presión interna de la cabina en kPa, un rango cercano a 101.3 kPa (presión atmosférica terrestre)
    
    # ¿La presión nunca cambia? ¿Cual es un valor normal y cual es un valor atípico?

    rand_val = random.random()
    if rand_val < 0.8:
        rad = random.uniform(0.06, 0.3) #Normal
    elif rand_val < 0.95:
        rad = random.uniform(2.1, 2.8)  #Comercial flight         --> siguiente 15% --> alores típicos de radiación que podrías recibir en un vuelo comercial (a gran altura, más radiación que al nivel del mar)
    else:
        rad = random.uniform(5.0, 9.4)  #Chernobyl 

    line = f"eclss,unit=module-alpha temperature={temp:.2f},pressure={pressure:.2f},radiation={rad:.4f}"
    return line.encode('utf-8')

while True:
    for _ in range(20):
        producer.send(TOPIC, get_eclss_data())
        time.sleep(0.1)
    
    producer.flush()
    print("ECLSS was send.")            # Se podría enviar también la linea de datos insertados en la DB (line) a tiempo real y con la opción -u se verían una por una y no todas de golpe al llenarse el buffer
    time.sleep(10)



    # ¿? DEBERÍAMOS PONER ALGUNA VARIACIÓN TANTO EN LAS ALERTA COMO EN EL PRODUCER PARA QUE NO ESTÉ TODO DENTRO DE UN RANGO EN PRESSURE PARA QUE HAYAN CASOS EXTREMOS
    # EN EL DASHBOARD