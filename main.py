# This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
import requests

from data_manager import DataManager
from flight_search import FlightSearch
from datetime import datetime, timedelta
from notification_manager import NotificationManager
from pprint import pprint

dm = DataManager()
fs = FlightSearch()
flight_data = dm.get_data()
nm = NotificationManager()

ORIGIN_CITY_IATA = "LON"

for data in flight_data:
    if not data['iataCode']:
        iataCode = fs.find_iata(data['city'])
        object_id = data['id']
        dm.update_date(object_id, iataCode)

date_for_tomorrow = (datetime.now() + timedelta(days=1)).strftime("%d/%m/%Y")
date_6_months = (datetime.now() + timedelta(days=6 * 30)).strftime("%d/%m/%Y")

for data in flight_data:
    flight = fs.find_flight(
        ORIGIN_CITY_IATA,
        data['iataCode'],
        date_for_tomorrow,
        date_6_months)


    if flight is None:
      continue

    if flight.price < data['lowestPrice']:
        message = f"Low price alert! Only £{flight.price} to fly from {flight.origin_city}-{flight.origin_airport}" \
                         f" to {flight.destination_city}-{flight.destination_airport} from {flight.out_date} to {flight.return_date}"
        if flight.stop_over > 0:
            message += f"\nFlight has {flight.stop_over} stop over, via {flight.via_city}."

        print(message)

