import requests
import os

class DataManager:
    #This class is responsible for talking to the Google Sheet.

    FLIGHT_ENDPOINT = os.environ.get("FLIGHT_ENDPOINT")
    USERS_ENDPOINT = os.environ.get("USERS_ENDPOINT")

    def __init__(self):
        self.flights = requests.get(url=self.FLIGHT_ENDPOINT)
        self.users = requests.get(url=self.USERS_ENDPOINT)
        self.data = None


    def get_flight_data(self):
        return self.flights.json()["prices"]

    def update_iataCode(self, object_id, iataCode):
        self.data = {
            "price": {
                "iataCode": iataCode,
            }
        }
        new_shetty_id = self.SHEETY_ENDPOINT+f"/{object_id}"
        return requests.put(url=new_shetty_id, json=self.data)

    def get_users(self):
        return self.users.json()["users"]




