
from database import get_db_connection

def get_all_users():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM USERS').fetchall()
    conn.close()
    return [dict(row) for row in users]
