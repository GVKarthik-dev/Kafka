import os
import json
from kafka import KafkaProducer
from kafka import KafkaConsumer
from dotenv import load_dotenv

load_dotenv()

ORDER_TOPIC = os.getenv('ORDER_TOPIC')
CONFIRMED_TOPIC = os.getenv('CONFIRMED_TOPIC')

Consumer = KafkaConsumer(ORDER_TOPIC,bootstrap_servers='localhost:9092')

Producer = KafkaProducer(bootstrap_servers='localhost:9092')

print('Going to Listen for orders ....')

while True:
    for message in Consumer:
        order = json.loads(message.value.decode())
        print(order)
        
        user_id = order['User_name']
        total = order['Total_count']
        
        data = {
            'Customer_id':user_id,
            'Customer_email':f'{user_id}@kick.com',
            'Total':total
        }
        print('Sucessfull Transection ....')
        Producer.send(
            CONFIRMED_TOPIC,
            json.dumps(data).encode('utf-8')
        )