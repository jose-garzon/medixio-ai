
from database import get_db_connection

def get_all_medication_reminders():
    conn = get_db_connection()
    medication_reminders = conn.execute('SELECT * FROM MEDICATION_REMINDERS').fetchall()
    conn.close()
    return [dict(row) for row in medication_reminders]
