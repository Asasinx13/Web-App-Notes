from flask import Blueprint, views, render_template, request, flash, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from .models import Note
from . import db
import json

views = Blueprint("views", __name__)


@views.route("/", methods=["GET", "POST"])
@login_required
def home():
    if request.method == "POST":
        note = request.form.get("note")
        if note is None:
            return render_template("home.html", user=current_user)
        if len(note) < 1:
            flash("Note is too short!", category="error")
        else:
            new_note = Note()
            new_note.data = note
            new_note.user_id = current_user.id
            db.db_connection.session.add(new_note)
            db.db_connection.session.commit()
            flash("Note added!", category="success")

    return render_template("home.html", user=current_user)


@views.route("/delete-note", methods=["POST"])
def delete_note():
    note = json.loads(request.data)
    noteId = note["noteId"]
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.db_connection.session.delete(note)
            db.db_connection.session.commit()
            return jsonify({})

# Module Docstring:

#     Describes the purpose of the module, which is to define routes for handling operations related to notes using Flask.
#     Lists the routes defined in the module (home and delete_note).
#     Lists the dependencies (Flask, Flask-Login, SQLAlchemy, json).
#     Provides usage instructions and an example of how to register the blueprint.

# Imports:

#     from flask import Blueprint, views, render_template, request, flash, jsonify: Imports necessary functions and classes from Flask.
#     from flask_login import login_user, login_required, logout_user, current_user: Imports functions for managing user sessions.
#     from .models import Note: Imports the Note model from the current package.
#     from . import db: Imports the database instance from the current package.
#     import json: Imports the json module for handling JSON data.

# Blueprint Definition:

#     views = Blueprint("views", __name__): Creates a Blueprint named "views" for organizing the routes.

# Home Route (/):

#     @views.route("/", methods=["GET", "POST"]): Defines the route for the home page with GET and POST methods.
#     @login_required: Ensures that the user must be logged in to access this route.
#     home function:
#         Handles GET requests to render the home page template.
#         Handles POST requests to create a new note if the submitted note is valid.
#         Adds the new note to the database and flashes a success message.

# Delete Note Route (/delete-note):

#     @views.route("/delete-note", methods=["POST"]): Defines the route for deleting a note with the POST method.
#     delete_note function:
#         Parses the JSON data from the request to get the note ID.
#         Queries the database to find the note by its ID.
#         Deletes the note if it exists and belongs to the current user.
#         Returns a JSON response indicating success.