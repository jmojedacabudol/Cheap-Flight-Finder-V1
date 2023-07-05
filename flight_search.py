import requests
from flight_data import FlightData
import os


class FlightSearch:
    # This class is responsible for talking to the Flight Search API.
    API_KEY = os.environ.get("TEQUILA_API_KEY")
    FLIGHT_SEARCH_ENDPOINT = os.environ.get("TEQUILA_ENDPOINT")

    HEADER = {
        "apikey": API_KEY
    }

    def __init__(self):
        self.data = None

    def find_iata(self, city_name):
        data = {
            "term": city_name,
            "location_types": "city"
        }

        result = requests.get(url=self.FLIGHT_SEARCH_ENDPOINT + "locations/query", params=data,
                              headers=self.HEADER).json()
        return result["locations"][0]['code']

    def find_flight(self, origin_city_code, destination_city_code, from_time, to_time, max_stopover=0):
        query = {
            "fly_from": origin_city_code,
            "fly_to": destination_city_code,
            "date_from": from_time,
            "date_to": to_time,
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "one_for_city": 1,
            "flight_type": "round",
            "max_stopovers": max_stopover,
            "curr": "GBP"
        }

        response = requests.get(url=self.FLIGHT_SEARCH_ENDPOINT + "v2/search", params=query, headers=self.HEADER)
        try:
            data = response.json()["data"][0]
        except IndexError:

            query['max_stopovers'] = 1
            response = requests.get(url=self.FLIGHT_SEARCH_ENDPOINT + "v2/search", params=query, headers=self.HEADER)
            try:
                data = response.json()["data"][0]

                flight_data = FlightData(price=data['price'],
                                     origin_city=data['route'][0]['cityFrom'],
                                     origin_airport=data['route'][0]['flyFrom'],
                                     destination_city=data['route'][1]['cityTo'],
                                     destination_airport=data['route'][1]['flyTo'],
                                     out_date=data['route'][0]['local_departure'].split("T")[0],
                                     return_date=data['route'][2]['local_departure'].split("T")[0],
                                     stop_over=1,
                                     via_city=data["route"][0]["cityTo"]
                                         )
                return flight_data
            except IndexError:
                return None
        else:
            # print(f"{data['cityTo']} £{data['price']}")
            flight_data = FlightData(price=data['price'],
                                     origin_city=data['route'][0]['cityFrom'],
                                     origin_airport=data['route'][0]['flyFrom'],
                                     destination_city=data['route'][0]['cityTo'],
                                     destination_airport=data['route'][0]['flyTo'],
                                     out_date=data['route'][0]['local_departure'].split("T")[0],
                                     return_date=data['route'][1]['local_departure'].split("T")[0])
            return flight_data
