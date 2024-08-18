import os
import json
from kafka import KafkaProducer
from kafka import KafkaConsumer
from dotenv import load_dotenv

load_dotenv()

CONFIRMED_TOPIC = os.getenv('CONFIRMED_TOPIC')

Consumer = KafkaConsumer(
    CONFIRMED_TOPIC,
    bootstrap_servers='localhost:9092'
    )

TOTAL_NUMBER_ORDERS = 0
TOTAL_REVENUE = 0

print('Analytics listing ....')


while True:
    for tansection in Consumer:
        customer_details = json.loads(tansection.value.decode())
        
        Total_count = customer_details['Total']
        
        TOTAL_NUMBER_ORDERS += 1
        TOTAL_REVENUE += float(Total_count)
        
        print(f'Total revenue {TOTAL_REVENUE}, Total orders {TOTAL_NUMBER_ORDERS}')