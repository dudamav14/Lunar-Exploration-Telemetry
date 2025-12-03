import os
import time
import random
import math
from kafka import KafkaProducer


producer = KafkaProducer(bootstrap_servers='kafka-kraft:9092')
TOPIC = 'telemetry-comms'

orbit_step = 0.0 

def get_hga_data():
    global orbit_step
    
    base_snr = 40 + (10 * math.sin(orbit_step))
    orbit_step += 0.1
    base_latency = 20 + (100 / (abs(base_snr) + 1))
    ber = 0.000001
    
    if random.random() < 0.20:
        snr = base_snr - random.uniform(15, 25) 
        ber = random.uniform(0.01, 0.05)        
        latency = base_latency + random.uniform(200, 800)
    else:
        snr = base_snr + random.uniform(-1, 1)
        latency = base_latency + random.uniform(-5, 5)

    if snr < 0: snr = 0.0
    payload = f"comms,antenna_type=high_gain snr={snr:.2f},ber={ber:.8f},latency={latency:.2f}"
    
    return payload.encode('utf-8')


while True:
       
        for _ in range(20):
            producer.send(TOPIC, get_hga_data())
            time.sleep(0.1)
            
        producer.flush()
        print("HGA was send.")
        time.sleep(10)
        