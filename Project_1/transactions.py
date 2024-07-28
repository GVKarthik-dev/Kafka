import json
from kafka import KafkaProducer
from kafka import KafkaConsumer

KAFKA_ORDER_TOPIC = 'order_details'
KAFKA_CONFIRMED_TOPIC = 'order_confirmed'

Consumer = KafkaConsumer(KAFKA_ORDER_TOPIC,bootstrap_servers='localhost:29092')

Producer = KafkaProducer(bootstrap_servers='localhost:29092')

print('Going to Listen for orders ....')

while True:
    for message in Consumer:
        order = json.loads(message.value.decode())
        print(order)
        
        user_id = order['User_id']
        total = order['Total_count']
        
        data = {
            'Customer_id':user_id,
            'Customer_email':f'{user_id}@kick.com',
            'Total':total
        }
        print('Sucessfull Transection ....')
        Producer.send(
            KAFKA_CONFIRMED_TOPIC,
            json.dumps(data).encode('utf-8')
        )