import sqlite3


def init_users_db():
    conn = sqlite3.connect("../user_db.db")
    cursor = conn.cursor()

    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS users
                   (
                       username TEXT PRIMARY KEY,
                       password TEXT NOT NULL
                   )
                   """)

    users = [
        ("admin", "admin321"),
        ("office", "rachunek321")
    ]

    cursor.executemany("""
                       INSERT
                       OR IGNORE INTO users (username, password)
    VALUES (?, ?)
                       """, users)

    conn.commit()
    conn.close()


def check_login(username, password):
    conn = sqlite3.connect("../user_db.db")
    cursor = conn.cursor()

    cursor.execute("""
                   SELECT *
                   FROM users
                   WHERE username = ?
                     AND password = ?
                   """, (username, password))

    user = cursor.fetchone()

    conn.close()

    return user is not None
