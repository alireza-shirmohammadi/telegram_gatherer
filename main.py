from producer import kafka_producer
from telethon.tl.types import InputMessagesFilterEmpty
from telethon.tl.functions.messages import GetHistoryRequest
import json
from client_conf import conf
from consumer import consum
from search_channels import search_channel


# Create the client and connect

api_id = input("enter your api_id : ")
api_hash = input("enter your api-hash : ")
client = conf(api_id, api_hash)


class Messages:
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
        i = 0
        a = {}
        for i in range(0, limit):

            a["message"] = result.messages[i].message
            binary = json.dumps(a).encode("utf-8")
            kafka_producer(binary)
            print(result.messages[i].message)
            i += 1

        return None


b = Messages()

b.collect(input("address of channel:"), int(input("number of result:")))

consum()
search_channel()
