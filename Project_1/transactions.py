import os
import json
from fastapi import APIRouter, BackgroundTasks
from kafka import KafkaProducer, KafkaConsumer
from dotenv import load_dotenv

load_dotenv()

ORDER_TOPIC = os.getenv('ORDER_TOPIC')
CONFIRMED_TOPIC = os.getenv('CONFIRMED_TOPIC')

router = APIRouter()

consumer = KafkaConsumer(ORDER_TOPIC, bootstrap_servers='localhost:9092')
producer = KafkaProducer(bootstrap_servers='localhost:9092')

def process_orders():
    print('Listening for orders...')
    while True:
        for message in consumer:
            order = json.loads(message.value.decode())
            print(order)

            user_id = order['User_name']
            total = order['Total_count']

            data = {
                'Customer_id': user_id,
                'Customer_email': f'{user_id}@kick.com',
                'Total': total
            }
            print('Successful Transaction...')
            producer.send(CONFIRMED_TOPIC, json.dumps(data).encode('utf-8'))

@router.post("/listen-orders")
async def listen_orders(background_tasks: BackgroundTasks):
    background_tasks.add_task(process_orders)
    return {"message": "Started listening to orders in the background"}
