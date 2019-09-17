from classes import PostcodeTravelInfo


def main():
    print("Welcome to BusBoard.")
    postcode = input("Please enter your postcode: \n")
    number_of_stops = int(input("How many bus stops would you like to see?: \n")) # TODO what if not int
    number_of_buses = input("How many buses would you like to see?: \n") # TODO probably should enforce number here
    PostcodeTravelInfo(postcode, number_of_stops, number_of_buses).display()


if __name__ == "__main__": main()
