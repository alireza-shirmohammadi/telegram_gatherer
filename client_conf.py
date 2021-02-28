# use full phone number including + and country code
from telethon.sync import TelegramClient
from telethon.errors import SessionPasswordNeededError


def conf(api_id, api_hash):
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
    return client
