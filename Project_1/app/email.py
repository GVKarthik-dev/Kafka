import os
import json
from fastapi import APIRouter, BackgroundTasks
from kafka import KafkaConsumer
from dotenv import load_dotenv

load_dotenv()

CONFIRMED_TOPIC = os.getenv('CONFIRMED_TOPIC')

router = APIRouter()

consumer = KafkaConsumer(CONFIRMED_TOPIC, bootstrap_servers='localhost:9092')

email_sent_tillnow = set()

def send_emails():
    print('Listening for email sending...')
    while True:
        for message in consumer:
            details = json.loads(message.value.decode())
            email = details['Customer_email']
            print(f'Sent a mail to {email}')
            email_sent_tillnow.add(email)
            print(f'Total emails sent: {len(email_sent_tillnow)}')

@router.post("/send-emails")
async def send_emails_route(background_tasks: BackgroundTasks):
    background_tasks.add_task(send_emails)
    return {"message": "Started sending emails in the background"}
