from flask_login import LoginManager

from flask import Flask
from pydantic import SecretStr
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path
from db_singleton import SQLSingleton

login_manager = LoginManager()
DB_NAME = "database.db"
db = None


def create_app():
    global db
    app = Flask(__name__)
    app.config["SECRET_KEY"] = " WHATEVER"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    db = SQLSingleton(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User, Note

    create_database(app)
    login_manager = LoginManager()

    login_manager.login_view = "auth.login"  # type:ignore

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    login_manager.init_app(app)
    return app


def create_database(app: Flask):
    if not path.exists("website/" + DB_NAME):
        with app.app_context() as context:
            db.db_connection.create_all()
            print("Created Database!")

# Dependencies

#     Flask: Web framework.
#     Flask-Login: User session management.
#     Flask-SQLAlchemy: SQLAlchemy integration for Flask.
#     pydantic: Used for managing secret keys securely.
#     db_singleton: Custom module for managing a singleton database connection.
#     os.path: For filesystem path operations.

# Components

#     Global Variables
#         login_manager: Instance of LoginManager from Flask-Login for managing user sessions.
#         DB_NAME: Name of the SQLite database file.
#         db: Placeholder for the SQLAlchemy database connection.

#     Function: create_app()
#         Purpose: Initializes and configures the Flask application.
#         Configuration:
#             Sets the SECRET_KEY for session management.
#             Defines the SQLite database URI using SQLALCHEMY_DATABASE_URI.
#             Initializes the SQLAlchemy database connection via SQLSingleton.
#         Blueprint Registration:
#             Registers blueprints (views and auth) for organizing application routes.
#         Database Initialization:
#             Creates necessary database tables using create_database() function.
#         Login Management:
#             Configures login_manager:
#                 Sets the login view to "auth.login".
#                 Implements a user loader function (load_user) to retrieve users based on their ID.
#                 Initializes login_manager with the Flask application (app).

#     Function: create_database(app: Flask)
#         Purpose: Checks if the SQLite database file exists; if not, creates it and initializes tables.
#         Usage: Called during application setup to ensure the database is ready for use.

# Detailed Setup

#     Flask Application Setup:
#         Configures Flask app with a secret key (SECRET_KEY) for secure session management.
#         Specifies the SQLite database URI (SQLALCHEMY_DATABASE_URI) for connecting to the database file (DB_NAME).
#         Registers blueprints (views and auth) to organize routes related to application views and authentication.

#     Database Management:
#         Utilizes SQLSingleton from db_singleton to ensure a single database connection across the application.
#         Uses SQLAlchemy's create_all() method within create_database() to create necessary database tables if they don't exist.

#     Authentication and User Session Management:
#         Integrates LoginManager from Flask-Login to manage user sessions.
#         Defines a login view ("auth.login") and a user loader function (load_user) to facilitate user authentication and session management.