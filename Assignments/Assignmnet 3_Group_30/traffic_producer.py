from kafka import KafkaProducer
import json
import random
import time

# Confugiring kafka server , note my localhost is at port 9092 and 
# our topic for assignment is traffic data instead of music_events
bootstrap_servers = 'localhost:9092'
topic = 'traffic_data'

producer = KafkaProducer(bootstrap_servers=bootstrap_servers, value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# Five sensors -> requirement
sensors = ["Sensor_0", "Sensor_1", "Sensor_2", "Sensor_3", "Sensor_4"]

try:
    while True:
        # Generate random data
        data = {
            "sensor_id": random.choice(sensors),
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "vehicle_count": random.randint(0, 100),
            "average_speed": round(random.uniform(0, 120), 1),
            "congestion_level": random.choice(["LOW", "MEDIUM", "HIGH"])
        }
        
        # senfing data to kafka
        producer.send(topic, value=data)
        print(f"Sent: {data}")
        time.sleep(1)  # Send every second -> Again requirement

except KeyboardInterrupt:
    producer.flush()
    producer.close()