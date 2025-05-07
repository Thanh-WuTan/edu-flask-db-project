from app.db.users import get_db_connection
from mysql.connector import Error

class Course:
    def __init__(self, data):
        self.id = data[0]
        self.course_name = data[1]
        self.department_id = data[2]
        self.instructor_id = data[3]
        self.location = data[4]
        self.schedule = data[5]
        self.semester = data[6]


def get_all_courses():
    connection = get_db_connection()
    if connection is None:
        return []
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT id, course_name, department_id, instructor_id, location, schedule, semester FROM courses")
        courses_data = cursor.fetchall()
        courses = [Course(data) for data in courses_data]
        return courses
    except Error as e:
        print(f"Error fetching courses: {e}")
        return []
    finally:
        cursor.close()
        connection.close()

def create_course(course_name, department_id, instructor_id, location, schedule, semester):
    connection = get_db_connection()
    if connection is None:
        raise Exception("Failed to connect to database")
    try:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO courses (course_name, department_id, instructor_id, location, schedule, semester) VALUES (%s, %s, %s, %s, %s, %s)",
            (course_name, department_id, instructor_id, location, schedule, semester)
        )
        connection.commit()
    except Error as e:
        connection.rollback()
        raise Exception(f"Error creating course: {e}")
    finally:
        cursor.close()
        connection.close()

def update_course(course_id, course_name, department_id, instructor_id, location, schedule, semester):
    connection = get_db_connection()
    if connection is None:
        raise Exception("Failed to connect to database")
    try:
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE courses SET course_name = %s, department_id = %s, instructor_id = %s, location = %s, schedule = %s, semester = %s WHERE id = %s",
            (course_name, department_id, instructor_id, location, schedule, semester, course_id)
        )
        connection.commit()
    except Error as e:
        connection.rollback()
        raise Exception(f"Error updating course: {e}")
    finally:
        cursor.close()
        connection.close()

def delete_course(course_id):
    connection = get_db_connection()
    if connection is None:
        raise Exception("Failed to connect to database")
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM courses WHERE id = %s", (course_id,))
        connection.commit()
    except Error as e:
        connection.rollback()
        raise Exception(f"Error deleting course: {e}")
    finally:
        cursor.close()
        connection.close()