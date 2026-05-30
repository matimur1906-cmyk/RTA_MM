from kafka import KafkaConsumer, KafkaProducer
from datetime import datetime
import json
import requests

consumer = KafkaConsumer(
    'transactions',
    bootstrap_servers='broker:9092',
    auto_offset_reset='earliest',
    group_id='ml-scoring-v2',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

alert_producer = KafkaProducer(
    bootstrap_servers='broker:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

API_URL = "http://localhost:8001/score"

for msg in consumer:
    tx = msg.value

    try:
        # --- 1. Feature engineering ---
        amount = tx.get("amount", 0)
        is_electronics = tx.get("is_electronics", 0)

        # timestamp → hour (opcjonalnie, do debug/logów)
        timestamp = tx.get("timestamp")
        if timestamp:
            hour = datetime.fromisoformat(timestamp).hour
        else:
            hour = None

        # uproszczenie zgodnie z zadaniem
        tx_per_minute = 5

        features = {
            "amount": amount,
            "is_electronics": is_electronics,
            "tx_per_minute": tx_per_minute
        }

        # --- 2. Call API ---
        response = requests.post(API_URL, json=features)

        result = response.json()

        # --- 3. Jeśli fraud → alert ---
        if result.get("is_fraud"):
            alert = {
                "timestamp": datetime.utcnow().isoformat(),
                "transaction": tx,
                "fraud_probability": result.get("fraud_probability")
            }

            alert_producer.send('alerts', alert)

            print("ALERT:", alert)

        else:
            print("OK:", result)
    except Exception as e:
        print("ERROR:", e)
