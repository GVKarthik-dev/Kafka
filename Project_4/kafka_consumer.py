from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'supply_chain',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='supply-chain-group',
    value_serializer=lambda x: json.loads(x.decode('utf-8'))
)

for message in consumer:
    print(f"Received message: {message.value}")
    # Implement logic to mark messages as unread for the users
