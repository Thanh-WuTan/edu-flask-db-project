from flask import Flask
from flask_login import LoginManager
from app.config import Config
from app.db.users import db_get_user_by_id, User, db_get_user_by_email, db_create_user
import bcrypt

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # make frontend code reload as well 
    app.config['TEMPLATES_AUTO_RELOAD'] = True  

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # User loader callback for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        user = db_get_user_by_id(user_id)
        if user:
            return User(user)
        return None

    # Register blueprints
    from .routes import main
    from .auth import auth
    from .admin import admin
    from .instructor import instructor  
    from .student import student  
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(instructor, url_prefix='/instructor')  
    app.register_blueprint(student, url_prefix='/student')
    
    
    # create a default admin user 
    import os 
    default_admin_email = os.environ.get('DEFAULT_ADMIN_EMAIL')
    default_admin_username = os.environ.get('DEFAULT_ADMIN_USERNAME')   
    default_admin_password = os.environ.get('DEFAULT_ADMIN_PASSWORD')
    
    if default_admin_email and default_admin_username and default_admin_password:
        # Check if the admin user already exists
        existing_user = db_get_user_by_email(default_admin_email)
        if not existing_user:
            # Create the admin user
            # print("Creating default admin user...")
            db_create_user(
                email=default_admin_email,
                username=default_admin_username,
                password=bcrypt.hashpw(default_admin_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
                role_name="admin",
                phone=None,
                department_id=5
            )
            
        
    return app