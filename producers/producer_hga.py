import os
import time
import random
import math
from kafka import KafkaProducer


producer = KafkaProducer(bootstrap_servers='kafka-kraft:9092')
TOPIC = 'telemetry-comms'

orbit_step = 0.0            # “posición” en la órbita  

# La idea es que cada vez que generes datos, orbit_step va aumentando un poco.
# Eso hace que math.sin(orbit_step) cambie de forma suave (curva sinusoidal).
# Así simulas que ciertas métricas (como el SNR) cambian gradualmente a medida que el satélite/orbiter cambia de posición respecto a la Tierra o al rover.

# SNR = Signal-to-Noise Ratio = Relación Señal-Ruido
    # Si estás en una habitación silenciosa → oyes muy bien a la otra persona → SNR alto.
    # Si estás en una discoteca llena de ruido → casi no oyes nada → SNR bajo.

def get_hga_data():
    global orbit_step
    
    base_snr = 40 + (10 * math.sin(orbit_step))         # SNR --> (sin: Devuelve valores entre -1 y 1) oscila entre 30 y 50 dB
    orbit_step += 0.1           # Hace que cada llamada a la función avance un poco la “posición orbital”
    base_latency = 20 + (100 / (abs(base_snr) + 1))         # o es una fórmula física real, pero crea una relación lógica:  “Peor señal ⟶ normalmente más latencia”
    ber = 0.000001          # Valor por defecto de BER (Bit Error Rate) muy pequeño → muy pocas bits erróneas
    
    # En resumen:
    # Con buena señal, tienes:
    #     SNR alto,
    #     latencia moderada,
    #     BER casi 0.

    if random.random() < 0.20:      # Caso “mala comunicación” -->  Hay un 20% de probabilidad (1 de cada 5, aprox) de entrar en el bloque de degradación 
        snr = base_snr - random.uniform(15, 25) 
        ber = random.uniform(0.01, 0.05)        
        latency = base_latency + random.uniform(200, 800)

        # Se simulan “ventanas” donde el enlace se pone fatal: mucha latencia, alta tasa de error y SNR bajo

    else:       # Caso “normal”
        snr = base_snr + random.uniform(-1, 1)              # Le añades un pequeño ruido aleatorio, ±1 dB → variación realista, pero sin “catástrofe”
        latency = base_latency + random.uniform(-5, 5)

    # Esto representa:
        # El enlace normalmente funciona relativamente bien, con variaciones pequeñas.
        # Y solo a veces se desploma la calidad de la señal.

    if snr < 0: snr = 0.0       # SNR negativo no tiene mucho sentido en este contexto
    payload = f"comms,antenna_type=high_gain snr={snr:.2f},ber={ber:.8f},latency={latency:.2f}"
    
    return payload.encode('utf-8')


while True:
       
        for _ in range(20):
            producer.send(TOPIC, get_hga_data())
            time.sleep(0.1)
            
        producer.flush()
        print("HGA was send.")
        time.sleep(10)
        