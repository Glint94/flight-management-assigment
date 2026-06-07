import sqlite3

def add_new_flight():
    print("Add New Flight")

def view_flights_menu():
    print("View Flights")

def update_flight_menu():
    print("Update Flights")

def assign_pilot_to_flight():
    print("Assign Pilot")

def flight_functions():

    while True:

        print("\n--Flights Menu--")
        print("1. Add New Flight")
        print("2. View Flights")
        print("3. Update Flight")
        print("4. Assign Pilot")
        print("5. Return")

        choice = input("Select option: ")

        if choice == "1":
            add_new_flight()

        elif choice == "2":
            view_flights_menu()

        elif choice == "3":
            update_flight_menu()

        elif choice == "4":
            assign_pilot_to_flight()

        elif choice == "5":
            break

        else:
            print("Invalid Option, try again.")