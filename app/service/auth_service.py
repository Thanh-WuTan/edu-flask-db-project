import bcrypt
from app.db.users import get_user_by_email, create_user

def register_user(email, username, password, confirm_password):
    if password != confirm_password:
        return None, "Passwords do not match"
    
    if get_user_by_email(email):
        return None, "Email already exists"
    
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    user_id = create_user(email, username, hashed_password, 'guest')
    return user_id, None

def login_user(email, password):
    user = get_user_by_email(email)
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        return user, None
    return None, "Invalid email or password"