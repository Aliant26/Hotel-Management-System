import sqlite3
from geopy.geocoders import Nominatim

class Hotel:

    def __init__(
            self,
            hotel_id,
            name,
            address,
            rooms_total,
            rooms_free,
            lat,
            lon
    ):

        self.id = hotel_id
        self.name = name
        self.address = address
        self.rooms_total = rooms_total
        self.rooms_free = rooms_free

        self.lat = lat
        self.lon = lon

        self.marker = None


class Employee:

    def __init__(
            self,
            employee_id,
            name,
            position,
            contract,
            date,
            hotel_id,
            lat,
            lon
    ):

        self.id = employee_id
        self.name = name
        self.position = position
        self.contract = contract
        self.date = date
        self.hotel_id = hotel_id

        self.lat = lat
        self.lon = lon

        self.marker = None


class Guest:

    def __init__(
            self,
            guest_id,
            name,
            phone,
            email,
            id_type,
            id_number,
            hotel_id,
            lat,
            lon
    ):

        self.id = guest_id
        self.name = name
        self.phone = phone
        self.email = email
        self.id_type = id_type
        self.id_number = id_number
        self.hotel_id = hotel_id
        self.lat = lat
        self.lon = lon

        self.marker = None

class Model:

    def __init__(self):

        self.DB_NAME = "hotels_db.db"

        self.geotag = Nominatim(user_agent="hotel_app")

        self.init_db()

    def connect(self):
        return sqlite3.connect(self.DB_NAME)

    def geocode_address(self, address):

        try:

            location = self.geotag.geocode(
                address + ", Poland"
            )

            if location:
                return (
                    location.latitude,
                    location.longitude
                )

            city = address.split(",")[-1].strip()

            location = self.geotag.geocode(
                city + ", Poland"
            )

            if location:
                return (
                    location.latitude,
                    location.longitude
                )

        except Exception:
            pass

        return None, None
    def init_db(self):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS hotels
                       (
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           name TEXT NOT NULL,
                           address TEXT NOT NULL,
                           rooms_total INTEGER,
                           rooms_free INTEGER,
                           lat REAL,
                           lon REAL
                       )""")

        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS employees
                       (
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           name TEXT NOT NULL,
                           position TEXT NOT NULL,
                           contract TEXT,
                           date TEXT,
                           hotel_id INTEGER,
                           lat REAL,
                           lon REAL
                       )
                       """)

        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS guests
                       (
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           name TEXT NOT NULL,
                           phone TEXT,
                           email TEXT,
                           id_type TEXT,
                           id_number TEXT,
                           hotel_id INTEGER,
                           lat REAL,
                           lon REAL
                       )
                       """)

        conn.commit()
        conn.close()

    def add_hotel(self, name, address, rooms_total, rooms_free):

        lat, lon = self.geocode_address(address)

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO hotels
                (name, address, rooms_total, rooms_free, lat, lon)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (name, address, rooms_total, rooms_free, lat, lon)
        )

        conn.commit()
        conn.close()

    def get_hotels(self):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM hotels")
        data = cursor.fetchall()

        hotels = []

        for row in data:
            hotel = Hotel(
                row[0],
                row[1],
                row[2],
                row[3],
                row[4],
                row[5],
                row[6]
            )

            hotels.append(hotel)

        conn.close()

        return hotels

    def update_hotel(self, hotel_id, name, address, rooms_total, rooms_free):

        lat, lon = self.geocode_address(address)

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
                       UPDATE hotels
                       SET name        = ?,
                           address     = ?,
                           rooms_total = ?,
                           rooms_free  = ?,
                           lat         = ?,
                           lon         = ?
                       WHERE id = ?
                       """,
                       (name, address, rooms_total, rooms_free, lat, lon, hotel_id)
                       )

        conn.commit()
        conn.close()

    def delete_hotel(self, hotel_id):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM hotels WHERE id = ?", (hotel_id,))

        conn.commit()
        conn.close()

    def add_employee(self, name, position, contract, date, hotel_id, address):
        lat, lon = self.geocode_address(address)

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO employees (name, position, contract, date, hotel_id, lat, lon) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (name, position, contract, date, hotel_id, lat, lon)
        )

        conn.commit()
        conn.close()

    def update_employee(
            self,
            employee_id,
            name,
            position,
            contract,
            date,
            hotel_id,
            address
    ):

        lat, lon = self.geocode_address(address)

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE employees
            SET name     = ?,
                position = ?,
                contract = ?,
                date     = ?,
                hotel_id = ?,
                lat      = ?,
                lon      = ?
            WHERE id = ?
            """,
            (
                name,
                position,
                contract,
                date,
                hotel_id,
                lat,
                lon,
                employee_id
            )
        )

        conn.commit()
        conn.close()

    def delete_employee(self, employee_id):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM employees WHERE id = ?",
            (employee_id,)
        )

        conn.commit()
        conn.close()

    def get_employees_by_hotel(self, hotel_id):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM employees WHERE hotel_id = ?",
            (hotel_id,)
        )

        data = cursor.fetchall()
        conn.close()
        employees = []

        for row in data:
            employee = Employee(
                row[0],
                row[1],
                row[2],
                row[3],
                row[4],
                row[5],
                row[6],
                row[7]
            )

            employees.append(employee)

        conn.close()

        return employees

    def add_guest(self, name, phone, email, id_type, id_number, hotel_id):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT lat, lon FROM hotels WHERE id = ?",
            (hotel_id,)
        )

        hotel_coordinates = cursor.fetchone()

        lat = None
        lon = None

        if hotel_coordinates:
            lat = hotel_coordinates[0]
            lon = hotel_coordinates[1]

        cursor.execute(
            "INSERT INTO guests (name, phone, email, id_type, id_number, hotel_id, lat, lon) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (name, phone, email, id_type, id_number, hotel_id, lat, lon)
        )

        conn.commit()
        conn.close()

    def get_guests_by_hotel(self, hotel_id):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM guests WHERE hotel_id = ?",
            (hotel_id,)
        )

        data = cursor.fetchall()
        conn.close()
        guests = []

        for row in data:
            guest = Guest(
                row[0],
                row[1],
                row[2],
                row[3],
                row[4],
                row[5],
                row[6],
                row[7],
                row[8]
            )

            guests.append(guest)

        conn.close()

        return guests

    def update_guest(
            self,
            guest_id,
            name,
            phone,
            email,
            id_type,
            id_number,
            hotel_id
    ):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE guests
            SET name      = ?,
                phone     = ?,
                email     = ?,
                id_type   = ?,
                id_number = ?,
                hotel_id  = ?
            WHERE id = ?
            """,
            (
                name,
                phone,
                email,
                id_type,
                id_number,
                hotel_id,
                guest_id
            )
        )

        conn.commit()
        conn.close()

    def delete_guest(self, guest_id):

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM guests WHERE id = ?",
            (guest_id,)
        )

        conn.commit()
        conn.close()