class Vehicle:
    def __init__(self, brand, model, km_done, service_date):
        self.brand = brand
        self.model = model
        self.km_done = km_done
        self.service_date = service_date  # string in a format "DD.MM.YYYY"

    def add_km(self, new_km):
        self.km_done += new_km  # this is the same as km_done = km_done + new_km. It adds new_km number to the existing km_done

    def update_service_date(self, new_date):
        self.service_date = new_date


def list_all_vehicles(vehicles):
    if vehicles == []:  # alternative: if not vehicles
        print "There is not any vehicle yet entered in the program. Please select option b to add the first vehicle."
    else:
        for index, vehicle in enumerate(vehicles):
            print "%s) %s %s with %s km driven so far. Last service date: %s." % (index+1, vehicle.brand, vehicle.model,
                                                                                 vehicle.km_done, vehicle.service_date)


def add_new_vehicle(vehicles):
    brand = raw_input("Please enter the brand of the vehicle: ")
    model = raw_input("Please enter the model of the vehicle: ")
    km_done_str = raw_input("Please enter the amount of kilometers that vehicle has done so far (just a number): ")
    service_date = raw_input("Please enter the last service date (DD.MM.YYYY): ")

    try:
        km_done_str = km_done_str.replace(",", ".")
        km_done = float(km_done_str)

        new_vehicle = Vehicle(brand=brand, model=model, km_done=km_done, service_date=service_date)

        vehicles.append(new_vehicle)

        print "You have successfully added a new vehicle %s %s!" % (brand, model)
    except ValueError:
        print "Please enter just a number for the kilometers done so far."


def choose_vehicle(vehicles):
    print "Please choose the number of the vehicle that you would like to edit."
    print ""
    list_all_vehicles(vehicles)
    print ""
    selection = raw_input("What vehicle number wold you like to choose? ")
    return vehicles[int(selection) - 1]  # -1 because we add +1 to index in list_all_vehicles function


def add_new_kilometers(vehicles):
    sel_vehicle = choose_vehicle(vehicles)

    print "Vehicle selected: %s %s with %s km." % (sel_vehicle.brand, sel_vehicle.model, sel_vehicle.km_done)
    print ""
    new_km_str = raw_input("How many kilometers would you like to add to the existing ones? (enter only a number) ")
    print ""

    try:
        new_km_str = new_km_str.replace(",", ".")
        new_km = float(new_km_str)

        sel_vehicle.add_km(new_km)
        print "New number of kilometers for %s %s is now: %s." % (sel_vehicle.brand, sel_vehicle.model, sel_vehicle.km_done)
    except ValueError:
        print "Please enter just a number for the kilometers you'd like to add."


def change_service_date(vehicles):
    sel_vehicle = choose_vehicle(vehicles)

    print "Vehicle selected: %s %s with service date: %s." % (sel_vehicle.brand, sel_vehicle.model, sel_vehicle.service_date)
    print ""
    new_service_date = raw_input("What is the new general service date for this vehicle? (DD.MM.YYYY) ")
    print ""
    sel_vehicle.update_service_date(new_date=new_service_date)
    print "Service date updated!"


def main():
    print "Welcome to the Vehicle Manager program."

    vehicles = []

    while True:
        print ""  # empty line
        print "Please pick one of the following options:"
        print "a) See a list of all the company vehicles."
        print "b) Add new vehicle."
        print "c) Edit the kilometers done for the chosen vehicle."
        print "d) Edit the last service date for the chosen vehicle."
        print "e) Quit the program."
        print ""

        choice = raw_input("Which option would you like to choose? (a, b, c, d) ")
        print ""

        if choice.lower() == "a":
            list_all_vehicles(vehicles)
        elif choice.lower() == "b":
            add_new_vehicle(vehicles)
        elif choice.lower() == "c":
            add_new_kilometers(vehicles)
        elif choice.lower() == "d":
            change_service_date(vehicles)
        elif choice.lower() == "e":
            print "Thank you for using the Vehicle Manager. Have a nice day!"
            break
        else:
            print "I'm sorry, but I didn't understand your choice. Please type in just a letter, either a, b, c or d."

if __name__ == "__main__":
    main()
