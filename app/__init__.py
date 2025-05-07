from flask import Flask
from flask_login import LoginManager
from app.config import Config
from app.db.users import get_user_by_id, User

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # User loader callback for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        user = get_user_by_id(user_id)
        if user:
            return User(user)
        return None

    # Register blueprints
    from .routes import main
    from .auth import auth
    from .admin import admin
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(admin, url_prefix='/admin')

    return app