import os
import json
import time
import uuid
from kafka import KafkaProducer
from dotenv import load_dotenv

load_dotenv()

ORDER_TOPIC = os.getenv('ORDER_TOPIC')
ORDER_LIMIT = int(os.getenv('ORDER_LIMIT'))

Producer = KafkaProducer(bootstrap_servers='localhost:9092')

print('Going to generate orders ....')

for i in range(ORDER_LIMIT):
    data = {
        'Order_id': i + 1,
        'User_name': f'User_name_{i}',
        'Transaction': str(uuid.uuid4()),
        'Total_count': 1 * 2,
        'Items': 'burgers, fries'
    }
    # Use Producer.send instead of producer.send
    Producer.send(ORDER_TOPIC, json.dumps(data).encode('utf-8'))
    print(f'data_sent_{i + 1}')
    # time.sleep(2)