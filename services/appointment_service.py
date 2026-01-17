
from database import get_db_connection

def get_all_appointments():
    conn = get_db_connection()
    appointments = conn.execute('SELECT * FROM APPOINTMENTS').fetchall()
    conn.close()
    return [dict(row) for row in appointments]
