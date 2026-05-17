import sqlite3
from geopy.geocoders import Nominatim


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

        except ValueError:
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
                           hotel_id INTEGER
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

        conn.close()
        return data

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

    def get_employees_by_hotel(self, hotel_id):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM employees WHERE hotel_id = ?",
            (hotel_id,)
        )

        data = cursor.fetchall()
        conn.close()
        return data

    def add_guest(self, name, phone, email, id_type, id_number, hotel_id):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO guests (name, phone, email, id_type, id_number, hotel_id) VALUES (?, ?, ?, ?, ?, ?)",
            (name, phone, email, id_type, id_number, hotel_id)
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
        return data
