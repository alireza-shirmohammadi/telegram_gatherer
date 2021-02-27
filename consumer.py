from confluent_kafka import Consumer, KafkaError, KafkaException
import sys
import json
from connect_elastic import elastic


conf = {
    "bootstrap.servers": "0.0.0.0:9092,0.0.0.0:9092",
    "group.id": "foo",
    "auto.offset.reset": "smallest",
    "enable.auto.commit": True,
}

consumer = Consumer(conf)

def consum():
    i = 0
    try:
        consumer.subscribe(["telegram"])
        while True:

            msg = consumer.poll(timeout=1.0)

            if msg is None:
                break
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    sys.stderr.write(
                        "%% %s [%d] reached end at offset %d\n"
                        % (msg.topic(), msg.partition(), msg.offset())
                    )
                elif msg.error():
                    raise KafkaException(msg.error())

            else:
                message = (msg.value())
                my_json = json.loads(message.decode('utf-8'))
                elastic(my_json['message'],i)
                i+=1




    finally:
         print('end',i)
         consumer.close()

    #     # Close down consumer to commit final offsets.
