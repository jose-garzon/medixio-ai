
from database import get_db_connection

def get_all_medicines():
    conn = get_db_connection()
    medicines = conn.execute('SELECT * FROM MEDICINES').fetchall()
    conn.close()
    return [dict(row) for row in medicines]
