from kafka import KafkaConsumer
from typing import List, Dict
import json

def get_unread_messages(username: str) -> List[Dict]:
    # In a real application, you would have Kafka topic per user or some filtering logic.
    consumer = KafkaConsumer('social-media-topic', bootstrap_servers='localhost:9092', group_id=username, auto_offset_reset='earliest')
    unread_messages = []
    
    for message in consumer:
        data = json.loads(message.value.decode('utf-8'))
        if not data.get("read"):
            unread_messages.append(data)
    return unread_messages
