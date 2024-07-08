from __future__ import annotations
from typing import Optional

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


class Singleton(type):
    _references = {}

    def __call__(cls, *args, **kwargs) -> Singleton:
        if cls not in cls._references:
            cls._references[cls] = super().__call__(*args, **kwargs)
        return cls._references[cls]


class SQLSingleton(metaclass=Singleton):
    def __init__(self, app: Optional[Flask] = None) -> None:
        if app is not None:
            self.db_connection = SQLAlchemy(app)

# Module Docstring:

#     Describes the purpose of the module, which is to define a singleton pattern implementation for managing a database connection using SQLAlchemy within a Flask application.
#     Lists the classes defined in the module (Singleton and SQLSingleton).
#     Provides usage instructions and an example of how to use the SQLSingleton class.

# Imports:

#     from __future__ import annotations: Ensures forward compatibility of type annotations.
#     from typing import Optional: Imports the Optional type hint.
#     from flask import Flask: Imports the Flask class from the flask package.
#     from flask_sqlalchemy import SQLAlchemy: Imports the SQLAlchemy class from the flask_sqlalchemy package.

# Singleton Class:

#     A metaclass that implements the singleton pattern.
#     Contains a _references dictionary to store single instances of classes.
#     The __call__ method ensures that only one instance of a class is created, returning the same instance for subsequent calls.

# SQLSingleton Class:

#     A singleton class for initializing and managing the SQLAlchemy database connection.
#     Uses the Singleton metaclass to ensure only one instance is created.
#     The __init__ method initializes the SQLAlchemy database connection if a Flask app is provided.