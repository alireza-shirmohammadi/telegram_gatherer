**How To Run**

i made requirements.txt to list packages and dependencies .

you have to make a venv and install dependencies(requirements.txt):

`pip install requirement.txt`

also you need to run kafka on port 9092 and zookeeper on port 2118.

create a topic on kafka and named it telegram.
then run elasticsearch on port 9200.

finally to run application:

`python main.py`

after running application its asks for your **api_id** and **api_hash**
you can get them from **telegram.org**

then get your phone number and send a verification code to your telegram account

after login its asks for your requested channel address 
and number of data to gather

for example : https://t.me/akharinkhabar , 50


**Development RoadMap**


i use telethon package to connect to telegram :


    phone = None
        username = "@lireza"
        client = TelegramClient(username, api_id, api_hash)
        client.start()
        print("Client Created")

    # Ensure you're authorized
    if not client.is_user_authorized():
        client.send_code_request(phone)
        try:
            client.sign_in(phone, input("Enter the code: "))
        except SessionPasswordNeededError:
            client.sign_in(password=input("Password: "))

and gather data:

    def collect(self, channel, limit):
        filter = InputMessagesFilterEmpty()
        result = client(
            GetHistoryRequest(
                peer=channel,  # On which chat/conversation
                offset_date=None,
                offset_id=0,  # ID of the message to use as offset
                add_offset=0,  # Additional offset
                limit=limit,  # How many results
                max_id=0,  # Maximum message ID
                min_id=0,  # Minimum message ID
                hash=0,
            )
        )

after gathering data we send them to the kafka using producer:

    def kafka_producer(dict):
        producer = Producer(conf)
        producer.produce("telegram", value=dict)
        producer.flush()


again we connect to kafka and consum data and pass it to the elastic:
    
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
                message = msg.value()
                my_json = json.loads(message.decode("utf-8"))
                elastic(my_json["message"], i)
                i += 1


elastic config:

    def elastic(message, i):
        dic = {}
        dic["id"] = i
        dic["message"] = message
        es.index(index="kafka", id=i, body=dic)


i also write a func to search data in elastic:

    def search(q):

        body = {"query": {"prefix": {"message": {"value": q}}}}
        m = es.search(index="kafka", body=body)
        # len of search :
        size = len(m["hits"]["hits"])
    
        i = 0
        for i in range(0, size):
    
            print(m["hits"]["hits"][i]["_source"]["message"])
            i += 1


