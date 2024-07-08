from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.sql import func
from db_singleton import SQLSingleton

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SECRET_KEY"] = "WHATEVER"
db: SQLAlchemy = SQLSingleton().db_connection


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship("Note")

# Module Docstring:

#     Describes the purpose of the module, which is to define the Flask application setup, database models, and configuration.
#     Lists the imported modules and their purposes.
#     Lists the classes defined in the module (Note and User).
#     Provides usage instructions and an example of how to run the application.

# Imports:

#     from flask import Flask: Imports the Flask class from the flask package.
#     from flask_sqlalchemy import SQLAlchemy: Imports the SQLAlchemy class from the flask_sqlalchemy package.
#     from flask_login import UserMixin: Imports the UserMixin class from the flask_login package.
#     from sqlalchemy.sql import func: Imports the func module from sqlalchemy.sql for SQL functions.
#     from db_singleton import SQLSingleton: Imports the SQLSingleton class for managing a singleton database connection.

# Flask Application Initialization:

#     app = Flask(__name__): Initializes the Flask application.
#     app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db": Configures the database URI for SQLAlchemy.
#     app.config["SECRET_KEY"] = "WHATEVER": Sets the secret key for the Flask application (used for sessions, CSRF protection, etc.).

# Database Connection:

#     db: SQLAlchemy = SQLSingleton().db_connection: Gets the SQLAlchemy database connection from the singleton instance of SQLSingleton.

# Note Model:

#     class Note(db.Model): Defines the Note model, representing a note in the database.
#     id: Primary key of the note.
#     data: Content of the note.
#     date: Date and time when the note was created, with a default value of the current time.
#     user_id: Foreign key referencing the User model.

# User Model:

#     class User(db.Model, UserMixin): Defines the User model, representing a user in the database.
#     id: Primary key of the user.
#     email: Email address of the user, must be unique.
#     password: Password of the user.
#     first_name: First name of the user.
#     notes: Relationship to the Note model, representing the list of notes associated with the user.