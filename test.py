import os
import random
import string
import bcrypt
import mysql.connector
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database configuration from .env
DB_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "db"),
    "user": os.getenv("MYSQ_USER", "root"), 
    "password": os.getenv("MYSQL_PASSWORD", "abc123"),
    "database": os.getenv("MYSQL_DB", "edudb"),
    "port": int(os.getenv("MYSQL_PORT", 3306))
}

# Sample course names and locations
COURSE_NAMES = [
    "Introduction to Python", "Data Structures", "Algorithms", "Web Development",
    "Database Systems", "Machine Learning", "Operating Systems", "Networking",
    "Software Engineering", "Artificial Intelligence", "Cloud Computing",
    "Cybersecurity", "Mobile App Development", "DevOps", "Big Data"
]
LOCATIONS = ["Room 101", "Room 102", "Room 103", "Room 104", "Room 105", "Online"]
# Generate semesters from 2019 to 2040
SEASONS = ["Spring", "Summer", "Fall"]
SEMESTERS = [f"{season} {year}" for year in range(2019, 2041) for season in SEASONS]


# Schedule combinations (M, T, W, R, F only)
SCHEDULES = ["M", "T", "W", "R", "F", "MW", "TR", "MF", "TW", "MTR"]

def get_db_connection():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def generate_random_email(username):
    domains = ["gmail.com", "yahoo.com", "hotmail.com", "example.com"]
    return f"{username.lower()}@{random.choice(domains)}"

def generate_random_password(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def create_instructor(username, email, password):
    connection = get_db_connection()
    if connection is None:
        return None
    try:
        cursor = connection.cursor()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        cursor.execute(
            "INSERT INTO users (username, email, password, role, department_id) VALUES (%s, %s, %s, %s, %s)",
            (username, email, hashed_password, 2, random.randint(1, 5))  # role_id 2 is 'instructor'
        )
        connection.commit()
        cursor.execute("SELECT LAST_INSERT_ID()")
        instructor_id = cursor.fetchone()[0]
        return instructor_id
    except mysql.connector.Error as e:
        connection.rollback()
        print(f"Error creating instructor {username}: {e}")
        return None
    finally:
        cursor.close()
        connection.close()

def create_course(course_name, department_id, instructor_id, location, schedule, semester, availability):
    connection = get_db_connection()
    if connection is None:
        return False
    try:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO courses (course_name, department_id, instructor_id, location, schedule, semester, availability) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (course_name, department_id, instructor_id, location, schedule, semester, availability)
        )
        connection.commit()
        return True
    except mysql.connector.Error as e:
        connection.rollback()
        print(f"Error creating course {course_name}: {e}")
        return False
    finally:
        cursor.close()
        connection.close()

def generate_test_data():
    # Create 20 random instructors
    instructors = []
    for i in range(20):
        username = f"instructor_{i+20:02d}"
        email = generate_random_email(username)
        password = generate_random_password()
        instructor_id = create_instructor(username, email, password)
        if instructor_id:
            instructors.append(instructor_id)
            print(f"Created instructor: {username}, ID: {instructor_id}, Email: {email}, Password: {password}")
        else:
            print(f"Failed to create instructor: {username}")

    # Create 100 random courses
    for _ in range(1000):
        course_name = random.choice(COURSE_NAMES)
        department_id = random.randint(1, 5)  # Departments 1-5
        instructor_id = random.choice(instructors) if instructors else None
        location = random.choice(LOCATIONS)
        schedule = random.choice(SCHEDULES)
        semester = random.choice(SEMESTERS)
        availability = random.randint(20, 100)  # Random availability between 20 and 100
        success = create_course(course_name, department_id, instructor_id, location, schedule, semester, availability)
         # Assuming the create_course function has been modified to accept availability
        if success:
            print(f"Created course: {course_name}, Instructor ID: {instructor_id}, Schedule: {schedule}")
        else:
            print(f"Failed to create course: {course_name}")

def generate_students(): 
    # create 200 random students 
    connection = get_db_connection()
    students = []
    for i in range(10):
        username = f"student_{i+1:03d}"
        email = generate_random_email(username)
        password = generate_random_password()
        try:
            cursor = connection.cursor()
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            cursor.execute(
                "INSERT INTO users (username, email, password, role, department_id) VALUES (%s, %s, %s, %s, %s)",
                (username, email, hashed_password, 3, random.randint(1, 5))  # role_id 3 is 'student'
            )
            connection.commit()
            cursor.execute("SELECT LAST_INSERT_ID()")
            student_id = cursor.fetchone()[0]
            students.append(student_id)
            print(f"Created student: {username}, ID: {student_id}, Email: {email}, Password: {password}")
        except mysql.connector.Error as e:
            connection.rollback()
            print(f"Error creating student {username}: {e}")
        finally:
            cursor.close()

def generate_enrollments():
    # create around 10000 random enrollments. Enroll each student in 1-5 courses 
    
    connection = get_db_connection()
    if connection is None:
        return
    try:
        cursor = connection.cursor()
        for student_id in range(1, 2000):  # Assuming student IDs are from 1001 to 1999
            # Enroll each student in 1-5 random courses
            num_courses = random.randint(1, 5)
            course_ids = random.sample(range(161, 171), num_courses)  # Assuming 150 courses exist
            print(f"Enrolling student {student_id} in {num_courses} courses: {course_ids}")
            try:
                for course_id in course_ids:
                    print(f"Enrolling student {student_id} in course {course_id}")
                    cursor.execute(
                        "INSERT INTO enrollments (student_id, course_id) VALUES (%s, %s)",
                        (student_id, course_id)
                    )
            except Exception as e: 
                continue
        connection.commit()
    except mysql.connector.Error as e:
        connection.rollback()
        print(f"Error generating enrollments: {e}")
    finally:
        cursor.close()
        connection.close()
if __name__ == "__main__":
    # Ensure required libraries are installed
    try:
        import dotenv
        import bcrypt
    except ImportError:
        print("Please install required packages: pip install python-dotenv mysql-connector-python bcrypt")
        exit(1)
        
    generate_test_data()
    generate_enrollments()
    generate_students()
    print("Test data generation completed.")