import sqlite3

def add_new_pilot():
    print("Add New Pilot")

def view_pilots_menu():
    print("View Pilots")

def update_pilots_menu():
    print("Update Pilot")

def pilot_functions():

    while True:

        print("\n--Pilots Menu--")
        print("1. Add New Pilot")
        print("2. View Pilots")
        print("3. Update Pilots")
        print("4. Return")

        choice = input("Select option: ")

        if choice == "1":
            add_new_pilot()

        elif choice == "2":
            view_pilots_menu()

        elif choice == "3":
            update_pilots_menu()

        elif choice == "4":
            break

        else:
            print("Invalid Option, try again.")