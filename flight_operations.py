import sqlite3
import tabulate
from database_setup import connect_to_database
from pilot_operations import show_available_pilots, get_pilot_id
from airport_operations import show_available_airports, get_airport_id

# Function to fetch a flight_id using a flight number, more user friendly than asking for flight_id as input.
def get_flight_id(flight_number):
        database = connect_to_database()
        cursor = database.cursor()

        # SQL statement gets the flight_id of the first flight with a matching flight number. TODO: Improve functionality to
        # deal with cases where there are multiple flights with the same flight number.
        cursor.execute('''SELECT flight_id FROM flights WHERE flight_number = ?''', (flight_number,))
        flight = cursor.fetchone()
        database.close()

        #Return None if there are no flights with a matching flight number, otherwise return the flight.
        if flight is None:
           return None
        else:
            return flight[0]

def add_new_flight():
    #Initialise variable to avoid error in finally section later
    database = None

    try:
        # Take new flight number as input
        flight_number = input("Flight Number: ")

        # Display list of available airports then take airport code as input and perform validation.Convert airport
        # code to airport_id for use in SQL later.
        show_available_airports()
        origin_code = input("Origin Airport Code: ").upper()
        origin_id = get_airport_id(origin_code)
        if origin_id is None:
            print("Invalid airport code.")
            return

        # Take airport code as input and perform validation. Convert airport
        # code to airport_id for use in SQL later.
        destination_code = input("Destination Airport Code: ").upper()
        destination_id = get_airport_id(destination_code)
        if destination_id is None:
            print("Invalid airport code.")
            return

        # Display list of all pilots, take pilot license number as input and perform validation. Convert to pilot_id
        # for use in SQL later.
        show_available_pilots()
        license_number = input("Pilot License Number: ").upper()
        pilot_id = get_pilot_id(license_number)
        if pilot_id is None:
            print("Invalid Pilot License Number")
            return

        # Take departure time as a text input in format compatible for use as datetime. TODO: Add format validation.
        departure_datetime = input("Departure Date/Time (Format YYYY-MM-DD HH:MM:SS): ")

        # Take arrival time as a text input in format compatible for use as datetime. TODO: Add format validation. 
        # Database already prevents arrival being before departure but should enforce this in Python code too.
        arrival_datetime = input("Arrival Date/Time (Format YYYY-MM-DD HH:MM:SS): ")

        database = connect_to_database()
        cursor = database.cursor()

        # Run SQL statement to insert new entry into the flights table if all input is valid.
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

        # Commit changes to database.
        database.commit()

        print("Flight added successfully.")

    # Throw an error if relational integrity would be affected e.g. foreign key constraint would fail etc.
    except sqlite3.IntegrityError as error:
        print(f"Database error: {error}")

    # Close database connection once process is finished.
    finally:
            if database is not None:
                database.close()

# Function to output all flights in a table.
def view_all_flights():
    database = connect_to_database()
    cursor = database.cursor()

    # SQL statement to output all flights in table format. Uses joins to display the airport codes, airport names, and pilot names
    # rather than the less user friendly ID numbers that would have to be used if we just used the flights table.
    cursor.execute('''
                SELECT
                    flights.flight_number,
                    origin.airport_code,
                    origin.airport_name,
                    destination.airport_code,
                    destination.airport_name,
                    pilots.name,
                    flights.departure_datetime,
                    flights.arrival_datetime,
                    flights.status
                FROM flights JOIN airports origin ON flights.origin_id = origin.airport_id
                   JOIN airports destination ON flights.destination_id = destination.airport_id
                   JOIN pilots ON flights.pilot_id = pilots.pilot_id
                   ORDER BY flights.departure_datetime
    ''')

    # Display the retrieved data in a formatted table.
    flights = cursor.fetchall()

    headers = ["Flight Number", "Origin Airport Code", "Origin Airport Name", "Destination Airport Code",
               "Destination Airport Name", "Pilot", "Departure", "Arrival", "Status"]
    
    print(tabulate.tabulate(flights, headers = headers, tablefmt="grid"))

    database.close()

def search_flight_number():
    
    flight_number = input("Enter Flight Number: ")

    database = connect_to_database()
    cursor = database.cursor()

    cursor.execute('''
                    SELECT
                    flights.flight_number,
                    origin.airport_code,
                    origin.airport_name,
                    destination.airport_code,
                    destination.airport_name,
                    pilots.name,
                    flights.departure_datetime,
                    flights.arrival_datetime,
                    flights.status
                FROM flights JOIN airports origin ON flights.origin_id = origin.airport_id
                   JOIN airports destination ON flights.destination_id = destination.airport_id
                   JOIN pilots ON flights.pilot_id = pilots.pilot_id
                   WHERE flights.flight_number = ?
                   ORDER BY flights.departure_datetime 
                   ''', (flight_number,)
                )
    
    flights = cursor.fetchall()

    if flights:
        headers = ["Flight Number", "Origin Airport Code", "Origin Airport Name", "Destination Airport Code",
               "Destination Airport Name", "Pilot", "Departure", "Arrival", "Status"]
    
        print(tabulate.tabulate(flights, headers = headers, tablefmt="grid"))

    else:
        print("No flight found with flight number: " + flight_number)

    database.close()

def search_flight_status():
    status = input("Enter Status: ").lower()

    database = connect_to_database()
    cursor = database.cursor()

    cursor.execute('''
                    SELECT
                    flights.flight_number,
                    origin.airport_code,
                    origin.airport_name,
                    destination.airport_code,
                    destination.airport_name,
                    pilots.name,
                    flights.departure_datetime,
                    flights.arrival_datetime,
                    flights.status
                FROM flights JOIN airports origin ON flights.origin_id = origin.airport_id
                   JOIN airports destination ON flights.destination_id = destination.airport_id
                   JOIN pilots ON flights.pilot_id = pilots.pilot_id
                   WHERE flights.status = ?
                   ORDER BY flights.departure_datetime 
                   ''', (status,)
                )
    
    flights = cursor.fetchall()

    if flights:
        headers = ["Flight Number", "Origin Airport Code", "Origin Airport Name", "Destination Airport Code",
               "Destination Airport Name", "Pilot", "Departure", "Arrival", "Status"]
    
        print(tabulate.tabulate(flights, headers = headers, tablefmt="grid"))

    else:
        print("No flight found with status: " + status)

    database.close()

def view_flights_menu():
    
    while True:
        print("\n--View Flights Menu--")
        print("1. View All Flights")
        print("2. Search by Flight Number")
        print("3. Search by Status")
        print("4. Return")

        choice = input("Select option: ")

        if choice == "1":
            view_all_flights()

        elif choice == "2":
            search_flight_number()

        elif choice == "3":
            search_flight_status()

        elif choice == "4":
            break

        else:
            print("Invalid option. Try again.")

def update_departure_time():
    database = None

    try:
        flight_number = input("Flight Number: ")
        flight_id = get_flight_id(flight_number)

        if flight_id is None:
            print("Invalid Flight Number.")
            return

        new_departure_time = input("New Departure Time (Format YYYY-MM-DD HH:MM:SS): ")

        database = connect_to_database()
        cursor = database.cursor()

        cursor.execute('''
                    UPDATE flights SET departure_datetime = ? WHERE flight_id = ?''', (new_departure_time, flight_id)
                    )
        
        database.commit()

        if cursor.rowcount == 0:
            print("Invalid flight number.")
        else:
            print("Departure time updated.")
        
    finally:
        if database is not None:
            database.close()

def update_arrival_time():
    database = None

    try:
        flight_number = input("Flight Number: ")
        flight_id = get_flight_id(flight_number)

        if flight_id is None:
            print("Invalid Flight Number")
            return

        new_arrival_time = input("New Arrival Time (Format YYYY-MM-DD HH:MM:SS): ")

        database = connect_to_database()
        cursor = database.cursor()

        cursor.execute('''
                    UPDATE flights SET arrival_datetime = ? WHERE flight_id = ?''', (new_arrival_time, flight_id)
                    )
        
        database.commit()

        if cursor.rowcount == 0:
            print("Invalid flight number.")
        else:
            print("Arrival time updated.")
        
    except sqlite3.IntegrityError as error:
        print(f"Error: {error}")
    
    finally:
        if database is not None:
            database.close()

def update_flight_status():
    database = None

    try:
        flight_number = input("Flight Number: ")
        flight_id = get_flight_id(flight_number)

        if flight_id is None:
            print("Invalid Flight Number")
            return

        new_status = input("New Status (scheduled/delayed/completed/cancelled): ").lower()
        valid_statuses = [
            "scheduled",
            "delayed",
            "completed",
            "cancelled"
        ]

        if new_status not in valid_statuses:
            print("Invalid status.")
            return

        database = connect_to_database()
        cursor = database.cursor()

        cursor.execute('''
                    UPDATE flights SET status = ? WHERE flight_id = ?''', (new_status, flight_id)
                    )
        
        database.commit()

        if cursor.rowcount == 0:
            print("Invalid flight number.")
        else:
            print("Status updated.")

    except sqlite3.IntegrityError as error:
        print(f"Error: {error}")
        
    finally:
        if database is not None:
            database.close()

def update_origin():
    database = None

    try:
        flight_number = input("Flight Number: ")
        flight_id = get_flight_id(flight_number)

        if flight_id is None:
            print("Invalid Flight Number")
            return

        show_available_airports()
        new_origin_airport_code = input("New Origin Airport Code: ")
        airport_id = get_airport_id(new_origin_airport_code)

        if airport_id is None:
            print("Invalid Airport Code.")
            return

        database = connect_to_database()
        cursor = database.cursor()

        cursor.execute('''
                    UPDATE flights SET origin_id = ? WHERE flight_id = ?''', (airport_id, flight_id)
                    )
        
        database.commit()

        if cursor.rowcount == 0:
            print("Invalid flight number.")
        else:
            print("Origin airport updated.")

    except sqlite3.IntegrityError:
        print("Origin and Destination Airports cannot be the same.")
        
    finally:
        if database is not None:
            database.close()

def update_destination():
    database = None

    try:
        flight_number = input("Flight Number: ")
        flight_id = get_flight_id(flight_number)

        if flight_id is None:
            print("Invalid Flight Number")
            return

        show_available_airports()
        new_destination_airport_code = input("New Destination Airport Code: ")
        airport_id = get_airport_id(new_destination_airport_code)

        if airport_id is None:
            print("Invalid Airport Code.")
            return

        database = connect_to_database()
        cursor = database.cursor()

        cursor.execute('''
                    UPDATE flights SET destination_id = ? WHERE flight_id = ?''', (airport_id, flight_id)
                    )
        
        database.commit()

        if cursor.rowcount == 0:
            print("Invalid flight number.")
        else:
            print("Destination airport updated.")

    except sqlite3.IntegrityError:
        print("Origin and Destination Airports cannot be the same.")
        
    finally:
        if database is not None:
            database.close()

def print_update_flight_menu():
    print("\n-- Update Flight Information --\n")
    print("1. Update Departure Time")
    print("2. Update Arrival Time")
    print("3. Update Status")
    print("4. Update Origin Airport")
    print("5. Update Destination Airport")
    print("6. Return")

def update_flight_menu():

    while True:

        print_update_flight_menu()

        choice = input("Select option: ")

        if choice == "1":
            update_departure_time()

        elif choice == "2":
            update_arrival_time()

        elif choice == "3":
            update_flight_status()

        elif choice == "4":
            update_origin()

        elif choice == "5":
            update_destination()

        elif choice == "6":
            break

        else:
            print("Invalid option, try again.")

# Assigns a pilot to a flight.
def assign_pilot_to_flight():
    database = None

    # Select the flight that needs changing
    try:
        flight_number = input("Flight Number: ")
        flight_id = get_flight_id(flight_number)

        # Validate input flight number.
        if flight_id is None:
            print("Invalid Flight Number")
            return

        # List all available pilots for ease of use.
        show_available_pilots()
        # Take license number of new pilot.
        new_pilot_license_number = input("New Pilot License Number: ")
        pilot_id = get_pilot_id(new_pilot_license_number)

        # Validate input pilot license number.
        if pilot_id is None:
            print("Invalid Pilot License Number")
            return

        database = connect_to_database()
        cursor = database.cursor()

        # SQL Statement to assign the selected pilot to the selected flight.
        cursor.execute('''
                    UPDATE flights SET pilot_id = ? WHERE flight_id = ?''', (pilot_id, flight_id)
                    )

        # Commit the change to the database.        
        database.commit()

        # Back-up error catching, will print error message if input does not match any existing flight numbers.
        if cursor.rowcount == 0:
            print("Invalid flight number.")
        else:
            print("Pilot assigned successfully.")

    #Print error message if database integrity error is thrown.
    except sqlite3.IntegrityError as error:
        print(f"Database Error: {error}")
        
    # If a connection was made to the database, close it now that operations are finished.
    finally:
        if database is not None:
            database.close()

# Displays the main Flights menu and takes input to select an option.
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
            print("Invalid option, try again.")