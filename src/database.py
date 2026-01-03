import sqlite3
from datetime import datetime
import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_dir = os.path.join(base_dir, "database")

if not os.path.exists(db_dir):
    os.makedirs(db_dir)

DB_PATH = os.path.join(db_dir, "parking.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plate TEXT NOT NULL,
            entry_time TEXT NOT NULL,
            status TEXT DEFAULT 'INSIDE'
        )
    ''')
    conn.commit()
    conn.close()

def is_already_inside(plate):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM entries WHERE plate = ? AND (status = 'INSIDE' OR status = 'PAID')", (plate,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def save_entry(plate):
    if is_already_inside(plate):
        return False
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO entries (plate, entry_time) VALUES (?, ?)", (plate, now))
    conn.commit()
    conn.close()
    return True

def check_exit_status(plate):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT status, entry_time FROM entries WHERE plate = ? ORDER BY id DESC LIMIT 1", (plate,))
    result = cursor.fetchone()
    conn.close()
    return result

def remove_from_db(plate):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM entries WHERE plate = ? AND status = 'PAID'", (plate,))
    conn.commit()
    conn.close()