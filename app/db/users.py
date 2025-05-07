from .con import get_db_connection

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

def create_user(email, username, password, role_name, phone=None, department_id=1):
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