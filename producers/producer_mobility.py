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
    global battery, charging
    
    if charging:
        battery += random.uniform(0.5, 2.0)
        if battery >= 100:
            battery = 100
            charging = False
    else:
        battery -= random.uniform(0.1, 0.5)
        if battery <= 10: 
            charging = True
            
    rpm = random.uniform(1000, 5000)
    traction = random.uniform(0.8, 1.0)

    if random.random() < 0.1: 
        traction = random.uniform(0.1, 0.4)

    line = f"mobility,unit=rover-01 battery={battery:.2f},rpm={int(rpm)},traction={traction:.2f}"
    return line.encode('utf-8')

while True:
    for _ in range(20): 
        producer.send(TOPIC, get_mobility_data())
        time.sleep(0.1) 
    
    producer.flush()
    print("Mobility was send.")
    time.sleep(10) 