import json
import pika


connection = pika.BlockingConnection(
    pika.ConnectionParameters('rabbitmq', heartbeat=600,
                              blocked_connection_timeout=300))

channel = connection.channel()

channel.queue_declare(queue='db')


def publish(method, body=''):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='db', body=json.dumps(body), properties=properties)
