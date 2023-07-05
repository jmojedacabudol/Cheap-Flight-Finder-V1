from twilio.rest import Client
import os

class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.
    ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
    AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
    FROM_NUM = os.environ.get("TWILIO_FROM_NUM")
    RECIPIENT_NUM = os.environ.get("TWILIO_RECIPIENT_NUM")

    def __init__(self):
        self.client = Client(self.ACCOUNT_SID,self.AUTH_TOKEN)

    def create_notif(self, message):
        message = self.client.messages \
            .create(
            body=message,
            from_=self.FROM_NUM,
            to= self.RECIPIENT_NUM
        )
        return message.sid