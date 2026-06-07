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
    database = None

    try:
        airport_code = input("Airport Code: ").upper()

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

    except sqlite3.IntegrityError:
        print("Airport code already exists.")

    finally:
        if database is not None:
            database.close()

def view_all_airports():
    database = connect_to_database()
    cursor = database.cursor()

    cursor.execute('''SELECT * FROM airports ORDER BY airport_code''')

    airports = cursor.fetchall()

    headers = ["Airport Code", "Airport Name", "City", "Country"]

    print(tabulate.tabulate(airports, headers = headers, tablefmt="grid"))

    database.close()


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
            view_all_airports()

        elif choice == "3":
            update_airport_menu()

        elif choice == "4":
            break

        else:
            print("Invalid option, try again.")