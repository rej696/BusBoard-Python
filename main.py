from classes import BusDepartures
from classes import SingleDeparture
from classes import TransportApi
from classes import PostcodeTravelInfo
import logging
import json
logging.basicConfig(filename="BusBoard.log", filemode="w", level=logging.DEBUG)


def main():
    # print("Welcome to BusBoard.")
    # cont = True
    # while cont:
    #     postcode = input("Please enter your postcode: \n")
    #     transport_api = TransportApi(postcode)
    #     number_of_stops = int(input("How many bus stops would you like to see?: \n")) # TODO what if not int
    #     atcocode_lst = transport_api.identify_bus_stop(number_of_stops)
    #     number_of_buses = input("How many buses would you like to see?: \n") # TODO probably should enforce number here
    #     for atcocode in atcocode_lst:
    #         bus_departures = transport_api.bus_stop_live_departures(atcocode, number_of_buses)
    #         if bus_departures is not None:
    #             cont = False
    #             print(bus_departures)
    # return foo

    info = PostcodeTravelInfo("ba23hu", 1, 2)
    print(info.bus_stops[0].)


if __name__ == "__main__": main()
