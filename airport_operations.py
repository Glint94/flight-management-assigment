import sqlite3
import tabulate
from database_setup import connect_to_database


def get_airport_id(airport_code):
        database = connect_to_database()
        cursor = database.cursor()

        cursor.execute('''SELECT airport_id FROM airports WHERE airport_code = ?''', (airport_code,))
        airport = cursor.fetchone()
        database.close()

        if airport is None:
           return None
        else:
            return airport[0]
        
def show_available_airports():

    database = connect_to_database()
    cursor = database.cursor()

    cursor.execute('''
                    SELECT airport_code, airport_name
                    FROM airports
                    ORDER BY airport_code
    ''')

    print("\nAvailable Airports")

    for airport in cursor.fetchall():

        print(
            f"{airport[0]} - {airport[1]}"
        )   

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
            print("Invalid option, try again.")