from app.db.connector import get_db_connection
from mysql.connector import Error

def db_get_user_role_counts():
    connection = get_db_connection()
    if connection is None:
        return []
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.callproc('get_user_role_counts')
        user_role_counts = next(cursor.stored_results()).fetchall()
        return user_role_counts
    except Error as e:
        print(f"Error fetching user role counts: {e}")
        return []
    finally:
        cursor.close()
        connection.close()

def db_get_course_department_counts():
    connection = get_db_connection()
    if connection is None:
        return []
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.callproc('get_course_department_counts')
        course_dept_counts = next(cursor.stored_results()).fetchall()
        return course_dept_counts
    except Error as e:
        print(f"Error fetching course department counts: {e}")
        return []
    finally:
        cursor.close()
        connection.close()

def db_get_student_department_counts():
    connection = get_db_connection()
    if connection is None:
        return []
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.callproc('get_student_department_counts')
        student_dept_counts = next(cursor.stored_results()).fetchall()
        return student_dept_counts
    except Error as e:
        print(f"Error fetching student department counts: {e}")
        return []
    finally:
        cursor.close()
        connection.close()