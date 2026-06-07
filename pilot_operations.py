import sqlite3
from database_setup import connect_to_database

def show_available_pilots():
    database = connect_to_database()
    cursor = database.cursor()

    cursor.execute('''
                    SELECT license_number, name
                    FROM pilots
                    ORDER BY license_number
    ''')

    print("\nAvailable Pilots")

    for pilots in cursor.fetchall():

        print(
            f"{pilots[0]} - {pilots[1]}"
        )   

def get_pilot_id(license_number):
        database = connect_to_database()
        cursor = database.cursor()

        cursor.execute('''SELECT pilot_id FROM pilots WHERE license_number = ?''', (license_number,))
        pilot = cursor.fetchone()
        database.close()

        if pilot is None:
           return None
        else:
            return pilot[0]

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
            print("Invalid option, try again.")