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

# Producer = KafkaProducer(bootstrap_servers='localhost:29092')

print('Going to Email users about their order ....')

email_sent_tillnow = set()

while True:
    for message in Consumer:
        details = json.loads(message.value.decode())
        print(details)
        
        email  = details['Customer_email']
        print(f'sent a mail to {email}')
        email_sent_tillnow.add(email)
        print(f'Till now we have sent {len(email_sent_tillnow)} emails till now')