import json
import time
from kafka import KafkaProducer
import uuid

KAFKA_ORDER_TOPIC = 'order_details'
ORDER_LIMIT = 15

Producer = KafkaProducer(bootstrap_servers='localhost:29092')

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
    Producer.send(KAFKA_ORDER_TOPIC, json.dumps(data).encode('utf-8'))
    print(f'data_sent_{i + 1}')
    time.sleep(2)