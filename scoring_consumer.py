from kafka import KafkaConsumer, KafkaProducer
import json

consumer = KafkaConsumer(
    'transactions',
    bootstrap_servers='broker:9092',
    auto_offset_reset='earliest',
    group_id='scoring-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

alert_producer = KafkaProducer(
    bootstrap_servers='broker:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

for message in consumer:
    tx = message.value
    score = 0

    # R1
    if tx['amount'] > 3000:
        score += 3

    # R2
    if tx['category'] == 'elektronika' and tx['amount'] > 1500:
        score += 2

    # R3
    if tx['hour'] < 6:
        score += 2

    tx['score'] = score

    if score >= 3:
        alert_producer.send('alerts', value=tx)
        print(f"ALERT: {tx['tx_id']} | amount={tx['amount']} | category={tx['category']} | hour={tx['hour']} | score={score}")

alert_producer.flush()
alert_producer.close()
