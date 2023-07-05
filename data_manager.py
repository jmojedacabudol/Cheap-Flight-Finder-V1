import requests
import os

class DataManager:
    #This class is responsible for talking to the Google Sheet.

    SHEETY_ENDPOINT = os.environ.get("SHEETY_ENDPOINT")

    def __init__(self):
        self.result = requests.get(url=self.SHEETY_ENDPOINT)
        self.data = None


    def get_data(self):
        return self.result.json()["prices"]

    def update_date(self, object_id, iataCode):
        self.data = {
            "price": {
                "iataCode": iataCode,
            }
        }
        new_shetty_id = self.SHEETY_ENDPOINT+f"/{object_id}"
        return requests.put(url=new_shetty_id, json=self.data)




