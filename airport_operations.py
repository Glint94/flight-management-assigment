import sqlite3

def add_new_airport():
    print("Add New Airport")

def view_airports_menu():
    print("View Airports")

def update_airport_menu():
    print("Update Airports")

def airport_functions():

    while True:

        print("\n--Airports Menu--")
        print("1. Add New Airport")
        print("2. View Airports")
        print("3. Update Airport")
        print("4. Return")

        choice = input("Select option: ")

        if choice == "1":
            add_new_airport()

        elif choice == "2":
            view_airports_menu()

        elif choice == "3":
            update_airport_menu()

        elif choice == "4":
            break

        else:
            print("Invalid Option, try again.")