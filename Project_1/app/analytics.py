import os
import json
from fastapi import APIRouter, BackgroundTasks
from kafka import KafkaConsumer
from dotenv import load_dotenv

load_dotenv()

CONFIRMED_TOPIC = os.getenv('CONFIRMED_TOPIC')

router = APIRouter()

consumer = KafkaConsumer(CONFIRMED_TOPIC, bootstrap_servers='localhost:9092')

TOTAL_NUMBER_ORDERS = 0
TOTAL_REVENUE = 0

def analyze_transactions():
    global TOTAL_NUMBER_ORDERS, TOTAL_REVENUE
    print('Listening for analytics...')
    while True:
        for transaction in consumer:
            customer_details = json.loads(transaction.value.decode())
            total_count = customer_details['Total']

            TOTAL_NUMBER_ORDERS += 1
            TOTAL_REVENUE += float(total_count)

            print(f'Total revenue: {TOTAL_REVENUE}, Total orders: {TOTAL_NUMBER_ORDERS}')

@router.post("/analyze-transactions")
async def analyze_transactions_route(background_tasks: BackgroundTasks):
    background_tasks.add_task(analyze_transactions)
    return {"message": "Started analyzing transactions in the background"}
