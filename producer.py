from confluent_kafka import Producer
import socket

conf = {
    "bootstrap.servers": "0.0.0.0:9092,0.0.0.0:9092",
    "client.id": socket.gethostname(),
}

def kafka_producer(dict):
    producer = Producer(conf)
    producer.produce('telegram', value=dict)
    producer.flush()


