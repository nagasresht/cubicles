from kafka import KafkaProducer
import json, time, random
from datetime import datetime

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

users = ["alice", "bob", "charlie"]
locations = ["Delhi", "Mumbai", "Russia", "USA"]

while True:
    event = {
        "timestamp": datetime.utcnow().isoformat(),
        "user": random.choice(users),
        "location": random.choice(locations),
        "logins_last_minute": random.randint(1, 200),
        "data_transfer_mb": random.randint(1, 1000)
    }
    producer.send("security-events", event)
    print("Produced:", event)
    time.sleep(1)
