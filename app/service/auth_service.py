import bcrypt
import re
from app.db.users import db_get_user_by_email, db_create_user


def is_strong_password(password):
    # At least 8 characters, with at least one uppercase, one lowercase, one digit, and one special character
    return bool(re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password))

def register_user(email, username, password, confirm_password):
    if password != confirm_password:
        return None, "Passwords do not match"
    
    if not is_strong_password(password):
        return None, "Password must be at least 8 characters long and include uppercase, lowercase, number, and special character"

    if db_get_user_by_email(email):
        return None, "Email already exists"
    
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    user_id = db_create_user(email, username, hashed_password, 'guest')
    return user_id, None

def authenticate_user(email, password):
    user = db_get_user_by_email(email)
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        return user, None
    return None, "Invalid email or password"