import os
import json
import uuid
from fastapi import APIRouter
from kafka import KafkaProducer
from dotenv import load_dotenv

load_dotenv()

ORDER_TOPIC = os.getenv('ORDER_TOPIC')
ORDER_LIMIT = int(os.getenv('ORDER_LIMIT'))

router = APIRouter()

producer = KafkaProducer(bootstrap_servers='localhost:9092')

@router.post("/generate-orders")
async def generate_orders():
    for i in range(ORDER_LIMIT):
        data = {
            'Order_id': i + 1,
            'User_name': f'User_name_{i}',
            'Transaction': str(uuid.uuid4()),
            'Total_count': 1 * 2,
            'Items': 'burgers, fries'
        }
        producer.send(ORDER_TOPIC, json.dumps(data).encode('utf-8'))
        print(f'Order {i + 1} sent!')
    
    return {"message": "Orders sent successfully!"}
