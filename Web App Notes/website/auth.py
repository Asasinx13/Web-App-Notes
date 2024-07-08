from os import error
from unicodedata import category
from xmlrpc.client import boolean
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from db_singleton import SQLSingleton

db = SQLSingleton()
auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user is not None and password is not None:
            if check_password_hash(user.password, password):
                flash("Logged in successfully!", category="success")
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Incorrect password,try again.", category="error")
        else:
            flash("Email does not exist or password is missing.", category="error")

    return render_template("login.html", text="Testing", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        first_name = request.form.get("firstName")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        user = User.query.filter_by(email=email).first()
        # print("email", email)
        # print("first_name", first_name)
        # print("password1", password1)
        # print("password2", password2)
        # print("user", user)

        if email is None or first_name is None or password1 is None:
            return render_template("sign_up.html", user="None")
            # Raise la errors
        if user:
            flash("Email already exists.", category="error")
        elif len(email) < 4:
            flash("Email must be greater than 3 characters.", category="error")
        elif len(first_name) < 2:
            flash("First name must be greater than 1 characters.", category="error")
        elif password1 != password2:
            flash("Your passwords do not match.", category="error")
        elif len(password1) < 7:
            flash("Password must be minimum 8 characters.", category="error")
        else:
            new_user = User()
            new_user.email = email
            new_user.first_name = first_name
            new_user.password = generate_password_hash(password1)
            # new_user = User(
            #     email=email,
            #     first_name=first_name,
            #     password=generate_password_hash(password1, method="sha256"),
            # )
            db.db_connection.session.add(new_user)
            db.db_connection.session.commit()
            login_user(new_user, remember=True)
            flash("Account created!", category="success")
            return redirect(url_for("views.home"))

    return render_template("sign_up.html", user=current_user)

# Dependencies

#     Flask: Web framework.
#     Flask-Login: User session management.
#     Flask-SQLAlchemy: SQLAlchemy integration for Flask.
#     Werkzeug: Password hashing utilities.
#     db_singleton: Custom module for managing a singleton database connection.
#     models: Module defining the User model.

# Routes

#     login: Handles user login.
#     logout: Handles user logout.
#     sign_up: Handles user registration.

# Usage

#     The login route handles user login, including form submission and authentication.
#     The logout route logs the user out and redirects to the login page.
#     The sign_up route handles user registration, including form submission and user creation.

# Detailed Route Descriptions

#     Login Route (/login):
#         Methods: GET, POST
#         Functionality:
#             Handles GET requests to render the login page template.
#             Handles POST requests to authenticate the user and log them in if the provided credentials are valid.
#             Flashes appropriate messages for successful login, incorrect password, or non-existent email, and redirects to the home page upon successful login.

#     Logout Route (/logout):
#         Methods: GET
#         Functionality:
#             Logs the user out and redirects to the login page.
#             Ensures that the user must be logged in to access this route via the @login_required decorator.

#     Sign-Up Route (/sign-up):
#         Methods: GET, POST
#         Functionality:
#             Handles GET requests to render the sign-up page template.
#             Handles POST requests to create a new user account if the provided information is valid.
#             Flashes appropriate messages for existing email, short email, short first name, mismatched passwords, and short password, and redirects to the home page upon successful account creation.

# Additional Information

#     Blueprint Definition:
#         A Blueprint named "auth" is created for organizing the authentication routes.
#     Database Connection:
#         The SQLAlchemy database connection is obtained from the singleton instance of SQLSingleton.
#     Security:
#         Passwords are hashed using Werkzeug's generate_password_hash and checked using check_password_hash.
#     User Session Management:
#         Managed via Flask-Login's login_user, logout_user, and current_user functions.