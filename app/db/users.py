from .connector import get_db_connection
from mysql.connector import Error

class User:
    def __init__(self, user_data):
        self.id = user_data['id']
        self.email = user_data['email']
        self.role = user_data['role_name']
    
    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.id)

def create_user(email, username, password, role_name, phone=None, department_id=5):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM roles WHERE role_name = %s", (role_name,))
    role_id = cursor.fetchone()[0]
    cursor.execute(
        "INSERT INTO users (email, username, password, role, phone, department_id) VALUES (%s, %s, %s, %s, %s, %s)",
        (email, username, password, role_id, phone, department_id)
    )
    conn.commit()
    user_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return user_id

def update_user(user_id, username, email, role_name, phone, department_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM roles WHERE role_name = %s", (role_name,))
    role_id = cursor.fetchone()[0]
    cursor.execute(
        "UPDATE users SET username = %s, email = %s, role = %s, phone = %s, department_id = %s WHERE id = %s",
        (username, email, role_id, phone, department_id, user_id)
    )
    conn.commit()
    cursor.close()
    conn.close()

def get_user_by_email(email):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT u.*, r.role_name FROM users u JOIN roles r ON u.role = r.id WHERE u.email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

def get_user_by_id(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT u.*, r.role_name FROM users u JOIN roles r ON u.role = r.id WHERE u.id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

def get_all_users():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT u.*, r.role_name FROM users u JOIN roles r ON u.role = r.id")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return users

def delete_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    conn.commit()
    cursor.close()
    conn.close()

def get_filtered_users(email=None, department_id=None, role_name=None, page=1, per_page=10):
    connection = get_db_connection()
    if connection is None:
        return [], 0
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT u.id, u.username, u.role, u.phone, u.email, u.department_id, r.role_name, d.department_name
            FROM users u
            JOIN roles r ON u.role = r.id
            JOIN departments d ON u.department_id = d.id
            WHERE 1=1
        """
        params = []
        if email:
            query += " AND u.email LIKE %s"
            params.append(f"%{email}%")
        if department_id and int(department_id) > 0:
            query += " AND u.department_id = %s"
            params.append(department_id)
        if role_name:
            query += " AND r.role_name = %s"
            params.append(role_name)

        # Count total for pagination
        count_query = "SELECT COUNT(*) FROM users u JOIN roles r ON u.role = r.id WHERE 1=1"
        count_params = []
        if email:
            count_query += " AND u.email LIKE %s"
            count_params.append(f"%{email}%")
        if department_id and int(department_id) > 0:
            count_query += " AND u.department_id = %s"
            count_params.append(department_id)
        if role_name:
            count_query += " AND r.role_name = %s"
            count_params.append(role_name)

        cursor.execute(count_query, count_params)
        total_users = cursor.fetchone()['COUNT(*)']

        # Add pagination
        query += " ORDER BY u.id LIMIT %s OFFSET %s"
        params.extend([per_page, (page - 1) * per_page])

        cursor.execute(query, params)
        users = cursor.fetchall()
        return users, total_users
    except Error as e:
        print(f"Error fetching filtered users: {e}")
        return [], 0
    finally:
        cursor.close()
        connection.close()