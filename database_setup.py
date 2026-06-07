import sqlite3

def connect_to_database():
    # Connect to the databse.
    database = sqlite3.connect('database.db')
    # Enable foreign key constraints so that the database does not accept invalid foreign keys.
    database.execute("PRAGMA foreign_keys = ON")

    return database

def create_tables():
    database = connect_to_database()
    cursor = database.cursor()

    # Setup - If they already exist, drop all tables to get fresh version of database on each execution. In a real world application we would not do this.
    cursor.execute('''DROP TABLE IF EXISTS flights''')
    cursor.execute('''DROP TABLE IF EXISTS airports''')
    cursor.execute('''DROP TABLE IF EXISTS pilots''')

    # Create airport table
    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS airports (
                        airport_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        airport_code TEXT UNIQUE NOT NULL,
                        airport_name TEXT NOT NULL,
                        city TEXT NOT NULL,
                        country TEXT NOT NULL
                    );
    ''')

    # Create pilots table
    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS pilots (
                        pilot_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        license_number TEXT UNIQUE NOT NULL
                    );
    ''')

    # Create flights table
    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS flights (
                        flight_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        flight_number TEXT NOT NULL,
                        origin_id INTEGER NOT NULL REFERENCES airports(airport_id),
                        destination_id INTEGER NOT NULL REFERENCES airports(airport_id),
                        pilot_id INTEGER NOT NULL REFERENCES pilots(pilot_id),
                        departure_datetime TEXT NOT NULL,
                        arrival_datetime TEXT NOT NULL,
                        status TEXT NOT NULL DEFAULT "scheduled",
                        CHECK (origin_id <> destination_id),
                        CHECK (datetime(arrival_datetime) > datetime(departure_datetime))
                        CHECK status IN ("scheduled", "delayed", "completed", "cancelled")
                    );
    ''')

    database.commit()
    database.close()

def populate_database_sample_data():

    database = connect_to_database()
    cursor = database.cursor()

    # Populate airports table with sample data.
    cursor.execute('''
                    INSERT INTO airports
                    (airport_code, airport_name, city, country)
                    VALUES
                    ('LHR', 'Heathrow Airport', 'London', 'United Kingdom'),
                    ('JFK', 'John F. Kennedy International Airport', 'New York', 'United States'),
                    ('CDG', 'Charles de Gaulle Airport', 'Paris', 'France'),
                    ('FRA', 'Frankfurt Airport', 'Frankfurt', 'Germany'),
                    ('AMS', 'Amsterdam Schiphol Airport', 'Amsterdam', 'Netherlands'),
                    ('MAD', 'Adolfo Suarez Madrid-Barajas Airport', 'Madrid', 'Spain'),
                    ('FCO', 'Leonardo da Vinci Airport', 'Rome', 'Italy'),
                    ('DXB', 'Dubai International Airport', 'Dubai', 'United Arab Emirates'),
                    ('SIN', 'Singapore Changi Airport', 'Singapore', 'Singapore'),
                    ('HND', 'Haneda Airport', 'Tokyo', 'Japan'),
                    ('SYD', 'Sydney Airport', 'Sydney', 'Australia'),
                    ('YYZ', 'Toronto Pearson Airport', 'Toronto', 'Canada'),
                    ('ORD', 'O Hare International Airport', 'Chicago', 'United States'),
                    ('LAX', 'Los Angeles International Airport', 'Los Angeles', 'United States'),
                    ('DUB', 'Dublin Airport', 'Dublin', 'Ireland')
    ''')

    # Populate pilots table with sample data.
    cursor.execute('''
                    INSERT INTO pilots
                    (name, license_number)
                    VALUES
                    ('James Carter', 'LIC1001'),
                    ('Emma Thompson', 'LIC1002'),
                    ('Michael Evans', 'LIC1003'),
                    ('Sophia Hughes', 'LIC1004'),
                    ('Daniel Roberts', 'LIC1005'),
                    ('Olivia Walker', 'LIC1006'),
                    ('Benjamin Hall', 'LIC1007'),
                    ('Charlotte Green', 'LIC1008'),
                    ('William Lewis', 'LIC1009'),
                    ('Amelia Young', 'LIC1010'),
                    ('Henry King', 'LIC1011'),
                    ('Grace Wright', 'LIC1012'),
                    ('Thomas Scott', 'LIC1013'),
                    ('Isabella Baker', 'LIC1014'),
                    ('George Adams', 'LIC1015');
    ''')

    # Populate flights table with sample data.
    cursor.execute('''
                    INSERT INTO flights
                    (flight_number, origin_id, destination_id, pilot_id, departure_datetime, arrival_datetime, status)
                    VALUES
                    ('BA101', 1, 2, 1, '2026-06-01 08:00:00', '2026-06-01 16:00:00', 'scheduled'),
                    ('AF202', 3, 1, 2, '2026-06-01 09:30:00', '2026-06-01 10:45:00', 'completed'),
                    ('LH303', 4, 5, 3, '2026-06-02 07:15:00', '2026-06-02 08:30:00', 'scheduled'),
                    ('KL404', 5, 3, 4, '2026-06-02 12:00:00', '2026-06-02 13:20:00', 'scheduled'),
                    ('IB505', 6, 7, 5, '2026-06-03 10:00:00', '2026-06-03 12:15:00', 'delayed'),
                    ('AZ606', 7, 6, 6, '2026-06-03 14:30:00', '2026-06-03 16:45:00', 'scheduled'),
                    ('EK707', 8, 9, 7, '2026-06-04 06:00:00', '2026-06-04 13:30:00', 'scheduled'),
                    ('SQ808', 9, 10, 8, '2026-06-04 15:00:00', '2026-06-04 22:00:00', 'completed'),
                    ('JL909', 10, 11, 9, '2026-06-05 08:00:00', '2026-06-05 18:00:00', 'scheduled'),
                    ('QF110', 11, 10, 10, '2026-06-05 20:00:00', '2026-06-06 06:00:00', 'scheduled'),
                    ('AC211', 12, 13, 11, '2026-06-06 09:00:00', '2026-06-06 10:30:00', 'scheduled'),
                    ('UA312', 13, 14, 12, '2026-06-06 13:15:00', '2026-06-06 17:45:00', 'cancelled'),
                    ('DL413', 14, 12, 13, '2026-06-07 07:30:00', '2026-06-07 14:30:00', 'scheduled'),
                    ('EI514', 15, 1, 14, '2026-06-07 16:00:00', '2026-06-07 18:00:00', 'delayed'),
                    ('VS615', 1, 15, 15, '2026-06-08 11:00:00', '2026-06-08 13:00:00', 'scheduled');
    ''')

    database.commit()
    database.close()
