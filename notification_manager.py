from twilio.rest import Client
import os
import smtplib
class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.
    ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
    AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
    FROM_NUM = os.environ.get("TWILIO_FROM_NUM")
    RECIPIENT_NUM = os.environ.get("TWILIO_RECIPIENT_NUM")
    MY_EMAIL = os.environ.get("MY_EMAIL")
    MY_PASSWORD = os.environ.get("MY_PASSWORD")

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

    def send_emails(self,message,recipient_email):
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user= self.MY_EMAIL, password=self.MY_PASSWORD)
            connection.sendmail(from_addr=self.MY_EMAIL,
                                to_addrs=recipient_email,
                                msg=message)