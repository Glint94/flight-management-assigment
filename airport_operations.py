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

    cursor.execute('''SELECT airport_code, airport_name FROM airports ORDER BY airport_code''')

    print("\n--Available Airports--")

    for airport in cursor.fetchall():
        print(f"{airport[0]} - {airport[1]}")   

    database.close()

def add_new_airport():
    database = None

    try:
        airport_code = input("Airport Code: ").upper()

        if len(airport_code) != 3:
            print("Airport Code must be exactly 3 characters long.")
            return

        airport_name = input("Airport Name: ")

        city = input("City: ")

        country = input("Country: ")

        database = connect_to_database()
        cursor = database.cursor()

        cursor.execute('''
                    INSERT INTO airports (
                        airport_code,
                        airport_name,
                        city,
                        country
                       ) 
                       VALUES (?, ?, ?, ?)''',
                       (
                           airport_code,
                           airport_name,
                           city,
                           country
                       )
        )

        database.commit()

        print("Airport added successfully.")

    except sqlite3.IntegrityError as error:
        print(f"Database error: {error}")

    finally:
        if database is not None:
            database.close()

def view_all_airports():
    database = connect_to_database()
    cursor = database.cursor()

    cursor.execute('''SELECT airport_code, airport_name, city, country FROM airports ORDER BY airport_code''')

    airports = cursor.fetchall()

    headers = ["Airport Code", "Airport Name", "City", "Country"]

    print(tabulate.tabulate(airports, headers = headers, tablefmt="grid"))

    database.close()

def update_airport_name():
    database = None

    try:
        show_available_airports()

        airport_code = input("Airport Code: ").upper()
        airport_id = get_airport_id(airport_code)

        if airport_id is None:
            print("Invalid Airport Code")
            return

        airport_name = input("New Airport Name: ")

        database = connect_to_database()
        cursor = database.cursor()

        cursor.execute('''UPDATE airports SET airport_name = ? WHERE airport_id = ?''', (airport_name, airport_id))

        database.commit()

        print("Airport Name updated.")

    finally:
        if database is not None:
            database.close()

def update_city():
    database = None

    try:
        show_available_airports()

        airport_code = input("Airport Code: ").upper()
        airport_id = get_airport_id(airport_code)

        if airport_id is None:
            print("Invalid Airport Code")
            return

        city = input("New Airport City: ")

        database = connect_to_database()
        cursor = database.cursor()

        cursor.execute('''UPDATE airports SET city = ? WHERE airport_id = ?''', (city, airport_id))

        database.commit()

        print("City updated.")

    finally:
        if database is not None:
            database.close()

def update_country():
    database = None

    try:
        show_available_airports()

        airport_code = input("Airport Code: ").upper()
        airport_id = get_airport_id(airport_code)

        if airport_id is None:
            print("Invalid Airport Code")
            return

        country = input("New Airport Country: ")

        database = connect_to_database()
        cursor = database.cursor()

        cursor.execute('''UPDATE airports SET country = ? WHERE airport_id = ?''', (country, airport_id))

        database.commit()

        print("Country updated.")

    finally:
        if database is not None:
            database.close()

def update_airport_menu():
    
    while True:

        print("\n--Update Airport Menu--")
        print("1. Update Airport Name")
        print("2. Update City")
        print("3. Update Country")
        print("4. Return")

        choice = input("Select option: ")
        if choice == "1":
            update_airport_name()

        elif choice == "2":
            update_city()

        elif choice == "3":
            update_country()

        elif choice == "4":
            break

        else:
            print("Invalid option, try again.")

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
            view_all_airports()

        elif choice == "3":
            update_airport_menu()

        elif choice == "4":
            break

        else:
            print("Invalid option, try again.")