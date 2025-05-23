from .connector import get_db_connection
from mysql.connector import Error

class Course:
    def __init__(self, data):
        dept_name = {
            1: "CECS",
            2: "CAS",
            3: "CBM",
            4: "CHS",
        }
        self.id = data[0]
        self.course_name = data[1]
        self.department_id = data[2]
        self.instructor_id = data[3]
        self.location = data[4]
        self.schedule = data[5]
        self.semester = data[6]
        self.department_name = dept_name.get(data[2], "Unknown")
        self.availability = data[7]
    
def get_filtered_courses(search_query=None, department_id=None, schedule=None, instructor_id=None, page=1, per_page=10):
    connection = get_db_connection()
    if connection is None:
        return [], 0
    try:
        cursor = connection.cursor()
        query = """
            SELECT c.id, c.course_name, c.department_id, c.instructor_id, c.location, c.schedule, c.semester, c.availability, d.department_name
            FROM courses c
            JOIN departments d ON c.department_id = d.id
            WHERE 1=1
        """
        params = []
        if search_query:
            query += " AND c.course_name LIKE %s"
            params.append(f"%{search_query}%")
        if department_id:
            query += " AND c.department_id = %s"
            params.append(department_id)
        if schedule:
            query += " AND c.schedule LIKE %s"
            params.append(f"{schedule}")
        if instructor_id:
            query += " AND c.instructor_id = %s"
            params.append(instructor_id)
        
        # Count total for pagination
        count_query = "SELECT COUNT(*) FROM courses c JOIN departments d ON c.department_id = d.id WHERE 1=1"
        count_params = []
        if search_query:
            count_query += " AND c.course_name LIKE %s"
            count_params.append(f"%{search_query}%")
        if department_id:
            count_query += " AND c.department_id = %s"
            count_params.append(department_id)
        if schedule:
            count_query += " AND c.schedule = %s"
            count_params.append(schedule)
        if instructor_id:
            count_query += " AND c.instructor_id = %s"
            count_params.append(instructor_id)
        
        cursor.execute(count_query, count_params)
        total_courses = cursor.fetchone()[0]

        # Add pagination
        query += " ORDER BY c.id LIMIT %s OFFSET %s"
        params.extend([per_page, (page - 1) * per_page])

        cursor.execute(query, params)
        courses_data = cursor.fetchall()
        courses = [Course(data) for data in courses_data]
        return courses, total_courses
    except Error as e:
        print(f"Error fetching filtered courses: {e}")
        return [], 0
    finally:
        cursor.close()
        connection.close()

def create_course(course_name, department_id, instructor_id, location, schedule, semester, availability):
    connection = get_db_connection()
    if connection is None:
        raise Exception("Failed to connect to database")
    try:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO courses (course_name, department_id, instructor_id, location, schedule, semester, availability) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (course_name, department_id, instructor_id, location, schedule, semester, availability)
        )
        connection.commit()
    except Error as e:
        connection.rollback()
        raise Exception(f"Error creating course: {e}")
    finally:
        cursor.close()
        connection.close()

def update_course(course_id, course_name, department_id, instructor_id, location, schedule, semester, availability):
    connection = get_db_connection()
    if connection is None:
        raise Exception("Failed to connect to database")
    try:
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE courses SET course_name = %s, department_id = %s, instructor_id = %s, location = %s, schedule = %s, semester = %s, availability = %s WHERE id = %s",
            (course_name, department_id, instructor_id, location, schedule, semester, availability, course_id)
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

def db_get_course_by_instructor_id(instructor_id):
    connection = get_db_connection()
    if connection is None:
        return Exception("Failed to connect to database")
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM courses WHERE instructor_id = %s", (instructor_id,))
        courses = cursor.fetchall()
        return [Course(data) for data in courses]
    except Error as e:
        print(f"Error fetching courses by instructor ID: {e}")
        return []
    finally:
        cursor.close()
        connection.close()

def db_get_course_by_student_id(student_id):
    connection = get_db_connection()
    if connection is None:
        return Exception("Failed to connect to database")
    try:
        cursor = connection.cursor()        
        query = """
            SELECT 
                c.id, c.course_name, c.department_id, c.instructor_id,
                c.location, c.schedule, c.semester, 
                d.department_name, c.availability
            FROM enrollments e
            JOIN courses c ON e.course_id = c.id
            JOIN departments d ON c.department_id = d.id
            LEFT JOIN users u ON c.instructor_id = u.id
            WHERE e.student_id = %s
        """
        cursor.execute(query, (student_id,))
        courses_data = cursor.fetchall()
        return [Course(data) for data in courses_data]
    except Error as e:
        print(f"Error fetching courses by student ID: {e}")
        return []
    finally:
        cursor.close()
        connection.close()

def get_course_view_by_id(course_id):
    connection = get_db_connection()
    if connection is None:
        return None
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM view_course_details WHERE course_id = %s", (course_id,))
        course = cursor.fetchone()
        return course
    except Error as e:
        print(f"Error fetching course view by ID: {e}")
        return None
    finally:
        cursor.close()
        connection.close()