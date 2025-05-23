from .connector import get_db_connection
from mysql.connector import Error

def db_get_all_departments():
    connection = get_db_connection()
    if connection is None:
        return []
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT id, department_name FROM departments")
        departments = cursor.fetchall()
        return departments
    except Error as e:
        print(f"Error fetching departments: {e}")
        return []
    finally:
        cursor.close()
        connection.close()