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
SEMESTERS = ["Fall 2025", "Spring 2026", "Summer 2026"]

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

def create_course(course_name, department_id, instructor_id, location, schedule, semester):
    connection = get_db_connection()
    if connection is None:
        return False
    try:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO courses (course_name, department_id, instructor_id, location, schedule, semester) VALUES (%s, %s, %s, %s, %s, %s)",
            (course_name, department_id, instructor_id, location, schedule, semester)
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
    for _ in range(100):
        course_name = random.choice(COURSE_NAMES)
        department_id = random.randint(1, 5)  # Departments 1-5
        instructor_id = random.choice(instructors) if instructors else None
        location = random.choice(LOCATIONS)
        schedule = random.choice(SCHEDULES)
        semester = random.choice(SEMESTERS)
        success = create_course(course_name, department_id, instructor_id, location, schedule, semester)
        if success:
            print(f"Created course: {course_name}, Instructor ID: {instructor_id}, Schedule: {schedule}")
        else:
            print(f"Failed to create course: {course_name}")

if __name__ == "__main__":
    # Ensure required libraries are installed
    try:
        import dotenv
        import bcrypt
    except ImportError:
        print("Please install required packages: pip install python-dotenv mysql-connector-python bcrypt")
        exit(1)
    
    generate_test_data()
    print("Test data generation completed.")