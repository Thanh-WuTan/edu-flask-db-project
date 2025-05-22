from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user

def role_required(required_role, redirect_endpoint='main.index'):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role != required_role:
                flash('Unauthorized access.', 'danger')
                return redirect(url_for(redirect_endpoint))
            return f(*args, **kwargs)
        return decorated_function   
    return decorator
