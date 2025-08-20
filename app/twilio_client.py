import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER", "")
APP_ENV = os.getenv("APP_ENV", "dev")

if APP_ENV != "test":
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
else:
    class MockMessages:
        def create(self, to, from_, body):
            print(f"Mock Twilio: Sending message to {to} from {from_} with body: {body}")
            return type("Message", (object,), {"sid": "SMxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"})()
    class MockClient:
        def __init__(self, account_sid, auth_token):
            self.messages = MockMessages()
    client = MockClient(ACCOUNT_SID, AUTH_TOKEN)

def send_message(to_phone_number: str, message_body: str):
    try:
        message = client.messages.create(
            to=to_phone_number,
            from_=TWILIO_PHONE_NUMBER,
            body=message_body
        )
        print(f"Message sent to {to_phone_number}: {message.sid}")
        return message.sid
    except Exception as e:
        print(f"Error sending message to {to_phone_number}: {e}")
        return None
