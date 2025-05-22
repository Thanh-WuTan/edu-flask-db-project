from .connector import get_db_connection
from mysql.connector import Error
 
    
def get_enrolled_students(course_id):
    connection = get_db_connection()
    if connection is None:
        return []
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT u.id, u.email, u.username, d.department_name
            FROM enrollments e
            JOIN users u ON e.student_id = u.id
            JOIN departments d ON u.department_id = d.id
            WHERE e.course_id = %s AND u.role = (SELECT id FROM roles WHERE role_name = 'student')
        """
        cursor.execute(query, (course_id,))
        students = cursor.fetchall()
        return students
    except Error as e:
        print(f"Error fetching enrolled students: {e}")
        return []
    finally:
        cursor.close()
        connection.close()

def get_available_students(course_id):
    connection = get_db_connection()
    if connection is None:
        return []
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT u.id, u.email, u.username, d.department_name
            FROM users u
            JOIN departments d ON u.department_id = d.id
            WHERE u.role = (SELECT id FROM roles WHERE role_name = 'student')
            AND u.id NOT IN (SELECT student_id FROM enrollments WHERE course_id = %s)
        """
        cursor.execute(query, (course_id,))
        students = cursor.fetchall()
        return students
    except Error as e:
        print(f"Error fetching available students: {e}")
        return []
    finally:
        cursor.close()
        connection.close()

def db_enroll_student(student_id, course_id):
    connection = get_db_connection()
    if connection is None:
        raise Exception("Failed to connect to database")
    try:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO enrollments (student_id, course_id) VALUES (%s, %s)",
            (student_id, course_id)
        )
        connection.commit()
    except Error as e:
        connection.rollback()
        raise Exception(f"Error enrolling student: {e}")
    finally:
        cursor.close()
        connection.close()

def db_unenroll_student(student_id, course_id):
    connection = get_db_connection()
    if connection is None:
        raise Exception("Failed to connect to database")
    try:
        cursor = connection.cursor()
        cursor.execute(
            "DELETE FROM enrollments WHERE student_id = %s AND course_id = %s",
            (student_id, course_id)
        )
        connection.commit()
    except Error as e:
        connection.rollback()
        raise Exception(f"Error unenrolling student: {e}")
    finally:
        cursor.close()
        connection.close()