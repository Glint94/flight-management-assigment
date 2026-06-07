import sqlite3
from database_setup import create_tables, populate_database_sample_data

create_tables()
populate_database_sample_data()

while True:

    print("\n--Flight Management System--\n\n")
    print("Main Menu")
    print("1. View Flights")
    print("2. View Airports")
    print("3. View Pilots")
    print("4. Add Airport")
    print("5. Add Pilot")
    print("6. Add Flight")
    print("7. Exit")
    print("\nInput option number and press enter to select.")

    choice = input("Select option: ")
        
