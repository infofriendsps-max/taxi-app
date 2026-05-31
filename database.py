import sqlite3

DB_NAME = "taxi.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            driver_name TEXT NOT NULL,
            trip_description TEXT,
            trip_cost REAL NOT NULL,
            trip_date TEXT NOT NULL,
            is_paid INTEGER DEFAULT 0,
            created_date TEXT DEFAULT CURRENT_DATE,
            is_highlighted INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

def add_trip(customer_name, driver_name, trip_description, trip_cost, trip_date, is_paid=0):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO trips (customer_name, driver_name, trip_description, trip_cost, trip_date, is_paid) VALUES (?,?,?,?,?,?)',
                   (customer_name, driver_name, trip_description, trip_cost, trip_date, is_paid))
    conn.commit()
    conn.close()

def get_all_trips():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM trips ORDER BY id DESC')
    return cursor.fetchall()

def delete_trip(trip_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM trips WHERE id=?', (trip_id,))
    conn.commit()
    conn.close()

def set_highlight(trip_id, highlighted):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE trips SET is_highlighted=? WHERE id=?', (1 if highlighted else 0, trip_id))
    conn.commit()
    conn.close()

def get_highlighted_trips():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM trips WHERE is_highlighted=1')
    return [row[0] for row in cursor.fetchall()]
