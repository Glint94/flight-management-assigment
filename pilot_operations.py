import sqlite3
import tabulate
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

    for pilot in cursor.fetchall():
        print(f"{pilot[0]} - {pilot[1]}")

    database.close()

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
    database = None

    try:
        name = input("Pilot Name: ")

        license_number = input("License Number: ").upper()

        database = connect_to_database()
        cursor = database.cursor()

        cursor.execute('''INSERT INTO pilots (name, license_number) VALUES (?, ?)''', (name, license_number))

        database.commit()

        print("Pilot added successfully.")

    except sqlite3.IntegrityError as error:
        print(f"Database error: {error}")

    finally:
        if database is not None:
            database.close()

def view_all_pilots():
    database = connect_to_database()
    cursor = database.cursor()

    cursor.execute('''SELECT license_number, name FROM pilots ORDER BY license_number''')

    pilots = cursor.fetchall()

    headers = ["License Number", "Pilot Name"]

    print(tabulate.tabulate(pilots, headers = headers, tablefmt = "grid"))

    database.close()

def update_pilot_name():
    database = None

    try:
        show_available_pilots()

        license_number = input("Pilot License Number: ").upper()
        pilot_id = get_pilot_id(license_number)

        if pilot_id is None:
            print("Invalid Pilot License Number")
            return
        
        new_name = input("New Pilot Name: ")

        database = connect_to_database()
        cursor = database.cursor()

        cursor.execute('''UPDATE pilots SET name = ? WHERE pilot_id = ?''', (new_name, pilot_id))

        database.commit()

        print("Pilot Name Updated.")

    finally:
        if database is not None:
            database.close()

def update_pilot_license_number():
    database = None

    try:
        show_available_pilots()

        license_number = input("Current Pilot License Number: ").upper()
        pilot_id = get_pilot_id(license_number)

        if pilot_id is None:
            print("Invalid Pilot License Number")
            return
        
        new_license_number = input("New Pilot License Number: ").upper()

        database = connect_to_database()
        cursor = database.cursor()

        cursor.execute('''UPDATE pilots SET license_number = ? WHERE pilot_id = ?''', (new_license_number, pilot_id))

        database.commit()

        print("Pilot License Number Updated.")

    except sqlite3.IntegrityError as error:
        print(f"Database error: {error}")

    finally:
        if database is not None:
            database.close()

def update_pilots_menu():
    
    while True:

        print("\n--Update Pilot Menu--")
        print("1. Update Pilot Name")
        print("2. Update License Number")
        print("3. Return")

        choice = input("Select option: ")

        if choice == "1":
            update_pilot_name()

        elif choice == "2":
            update_pilot_license_number()

        elif choice == "3":
            break

        else:
            print("Invalid option, try again.")

def view_pilot_schedule():
    
    show_available_pilots()

    license_number = input("Pilots License Number: ").upper()
    pilot_id = get_pilot_id(license_number)

    if pilot_id is None:
        print("Invalid Pilot License Number.")
        return
    
    database = connect_to_database()
    cursor = database.cursor()

    cursor.execute('''
                    SELECT
                        pilots.name,
                        flights.flight_number,
                        origin.airport_code,
                        destination.airport_code,
                        flights.departure_datetime,
                        flights.arrival_datetime,
                        flights.status
                    FROM flights JOIN pilots ON flights.pilot_id = pilots.pilot_id
                    JOIN airports origin ON flights.origin_id = origin.airport_id
                    JOIN airports destination ON flights.destination_id = destination.airport_id
                    WHERE pilots.pilot_id = ?
                    ORDER BY flights.departure_datetime''', 
                    (pilot_id,)
    )

    schedule = cursor.fetchall()

    if schedule:
        headers = ["Pilot", "Flight Number", "Origin", "Destination", "Departure", "Arrival", "Status"]

        print(tabulate.tabulate(schedule, headers = headers, tablefmt = "grid"))

    else:
        print("No flights assigned to this pilot.")

    database.close()

def pilot_functions():

    while True:

        print("\n--Pilots Menu--")
        print("1. Add New Pilot")
        print("2. View Pilots")
        print("3. View Pilot Schedule")
        print("4. Update Pilots")
        print("5. Return")

        choice = input("Select option: ")

        if choice == "1":
            add_new_pilot()

        elif choice == "2":
            view_all_pilots()

        elif choice == "3":
            view_pilot_schedule()

        elif choice == "4":
            update_pilots_menu()

        elif choice == "5":
            break

        else:
            print("Invalid option, try again.")