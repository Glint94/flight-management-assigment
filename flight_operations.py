import sqlite3
from database_setup import connect_to_database
from pilot_operations import show_available_pilots, get_pilot_id

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

def add_new_flight():
    database = None

    try:
        flight_number = input("Flight Number: ")

        show_available_airports()
        origin_code = input("Origin Airport Code: ").upper()
        origin_id = get_airport_id(origin_code)
        if origin_id is None:
            print("Invalid airport code.")
            return

        show_available_airports()
        destination_code = input("Destination Airport Code: ").upper()
        destination_id = get_airport_id(destination_code)
        if destination_id is None:
            print("Invalid airport code.")
            return

        show_available_pilots()
        license_number = input("Pilot License Number: ")
        pilot_id = get_pilot_id(license_number)
        if pilot_id is None:
            print("Invalid Pilot License Number")
            return

        departure_datetime = input("Departure Date/Time (Format YYYY-MM-DD HH:MM:SS): ")

        arrival_datetime = input("Arrival Date/Time (Format YYYY-MM-DD HH:MM:SS): ")

        database = connect_to_database()
        cursor = database.cursor()

        cursor.execute('''
                        INSERT INTO flights (
                            flight_number,
                            origin_id,
                            destination_id,
                            pilot_id,
                            departure_datetime,
                            arrival_datetime,
                            status
                        )
                        VALUES (?, ?, ?, ?, ?, ?, ?) 
                        ''',
                        (
                            flight_number,
                            origin_id,
                            destination_id,
                            pilot_id,
                            departure_datetime,
                            arrival_datetime,
                            "scheduled"
                        )
        )

        database.commit()

        print("Flight added successfully.")

    except sqlite3.IntegrityError as error:
        print(f"Database error: {error}")

    finally:
            if database is not None:
                database.close()

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