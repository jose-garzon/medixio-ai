
from database import get_db_connection

def get_all_appointment_reminders():
    conn = get_db_connection()
    appointment_reminders = conn.execute('SELECT * FROM APPOINTMENT_REMINDERS').fetchall()
    conn.close()
    return [dict(row) for row in appointment_reminders]
