'''from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from settings import Config
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    from .models import User  # Import User here to avoid circular import
    return User.query.get(int(user_id))  # Load the user from the database by ID

def create_app():
    # Create Flask app instance
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions with the app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'  # Redirect unauthenticated users to the login page

    with app.app_context():
        # Import and register the Blueprint
        from .routes import main  # Import the Blueprint
        app.register_blueprint(main)  # Register the Blueprint

        # Flask-Admin setup
        from .models import User, Housekeeper, Rating  # Import models for admin panel
        admin = Admin(app, name='Admin Panel', template_mode='bootstrap3')
        admin.add_view(ModelView(User, db.session))
        admin.add_view(ModelView(Housekeeper, db.session))
        admin.add_view(ModelView(Rating, db.session))

        # Create database tables
        db.create_all()

    return app
    '''
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app.config import Config

db = SQLAlchemy()
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    from app.models import User  # Import User model here to avoid circular imports
    return User.query.get(int(user_id))  # Load the user from the database by ID

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'  # Redirect unauthenticated users to the login page

    # Register Blueprints
    from .routes import main
    app.register_blueprint(main)

    return app