import sqlite3
from flight_operations import flight_functions
from airport_operations import airport_functions
from pilot_operations import pilot_functions
from database_setup import create_tables, populate_database_sample_data

create_tables()
populate_database_sample_data()

#Prints the main menu
def print_main_menu():
    print("\n--Flight Management System--\n")
    print("Main Menu")
    print("1. Flights")
    print("2. Airports")
    print("3. Pilots")
    print("4. Exit")
    print("\nInput option number and press enter to select.")

#Option selection for the main menu.
def main_menu_options():
    while True:
        print_main_menu()
        choice = input("Select option: ")
            
        if choice == "1":
            flight_functions()

        elif choice == "2":
            airport_functions()

        elif choice == "3":
            pilot_functions()

        elif choice == "4":
            break

        else:
            print("Invalid option, please try again.")
            print_main_menu()

#Starts the program by entering the main menu.
main_menu_options()