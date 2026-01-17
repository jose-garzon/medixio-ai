
import sqlite3
from datetime import datetime

def setup_database():
    conn = sqlite3.connect('medixio.db')
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS USERS (
        user_id INTEGER PRIMARY KEY,
        email TEXT UNIQUE,
        hashed_password TEXT,
        first_name TEXT,
        last_name TEXT,
        created_at DATETIME,
        updated_at DATETIME
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS APPOINTMENTS (
        appointment_id INTEGER PRIMARY KEY,
        user_id INTEGER,
        title TEXT,
        doctor_name TEXT,
        location TEXT,
        appointment_time DATETIME,
        status TEXT,
        created_at DATETIME,
        updated_at DATETIME,
        FOREIGN KEY (user_id) REFERENCES USERS(user_id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS APPOINTMENT_REMINDERS (
        reminder_id INTEGER PRIMARY KEY,
        appointment_id INTEGER,
        user_id INTEGER,
        scheduled_reminder_time DATETIME,
        status TEXT,
        created_at DATETIME,
        FOREIGN KEY (appointment_id) REFERENCES APPOINTMENTS(appointment_id),
        FOREIGN KEY (user_id) REFERENCES USERS(user_id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS MEDICINES (
        medicine_id INTEGER PRIMARY KEY,
        user_id INTEGER,
        name TEXT,
        dosage TEXT,
        instructions TEXT,
        start_date DATE,
        end_date DATE,
        frequency_description TEXT,
        created_at DATETIME,
        updated_at DATETIME,
        FOREIGN KEY (user_id) REFERENCES USERS(user_id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS MEDICATION_REMINDERS (
        reminder_id INTEGER PRIMARY KEY,
        medicine_id INTEGER,
        user_id INTEGER,
        scheduled_intake_time DATETIME,
        status TEXT,
        actual_intake_time DATETIME,
        created_at DATETIME,
        FOREIGN KEY (medicine_id) REFERENCES MEDICINES(medicine_id),
        FOREIGN KEY (user_id) REFERENCES USERS(user_id)
    )
    ''')

    # Insert mock data
    now = datetime.now()

    users = [
        (1, 'test@example.com', 'password', 'felipe', 'last_name', now, now),
    ]

    appointments = [
        (1, 1, 'Checkup', 'Dr. Smith', 'Hospital', now, 'Scheduled', now, now),
    ]

    appointment_reminders = [
        (1, 1, 1, now, 'Pending', now),
    ]

    medicines = [
        (1, 1, 'Aspirin', '100mg', 'Take with food', now, now, 'Daily', now, now),
    ]

    medication_reminders = [
        (1, 1, 1, now, 'Pending', None, now),
    ]

    cursor.executemany('INSERT OR IGNORE INTO USERS VALUES (?, ?, ?, ?, ?, ?, ?)', users)
    cursor.executemany('INSERT OR IGNORE INTO APPOINTMENTS VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', appointments)
    cursor.executemany('INSERT OR IGNORE INTO APPOINTMENT_REMINDERS VALUES (?, ?, ?, ?, ?, ?)', appointment_reminders)
    cursor.executemany('INSERT OR IGNORE INTO MEDICINES VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', medicines)
    cursor.executemany('INSERT OR IGNORE INTO MEDICATION_REMINDERS VALUES (?, ?, ?, ?, ?, ?, ?)', medication_reminders)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    setup_database()
    print("Database setup complete.")
