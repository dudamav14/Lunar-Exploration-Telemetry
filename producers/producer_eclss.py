import os
import time
import random
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='kafka-kraft:9092')
TOPIC = 'telemetry-eclss'

def get_eclss_data():

    temp = random.uniform(-170, 120)
    pressure = random.uniform(95, 105) 
    
    rand_val = random.random()
    if rand_val < 0.8:
        rad = random.uniform(0.06, 0.3) #Normal
    elif rand_val < 0.95:
        rad = random.uniform(2.1, 2.8)  #Comercial flight
    else:
        rad = random.uniform(5.0, 9.4)  #Chernobyl 

    line = f"eclss,unit=module-alpha temperature={temp:.2f},pressure={pressure:.2f},radiation={rad:.4f}"
    return line.encode('utf-8')

while True:
    for _ in range(20):
        producer.send(TOPIC, get_eclss_data())
        time.sleep(0.1)
    
    producer.flush()
    print("ECLSS was send.")
    time.sleep(10)