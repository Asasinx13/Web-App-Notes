from website import create_app
from db_singleton import SQLSingleton


if __name__ == "__main__":
    app = create_app()

    app.run(debug=True)
    
# Module Docstring:

#     Describes the purpose of the module, which is to initialize and run the Flask web application.
#     Lists the imported modules (create_app and SQLSingleton).
#     Provides usage instructions and an example of how to run the script.

# Imports:

#     from website import create_app: Imports the create_app function from the website module. This function is expected to create and configure a Flask application instance.
#     from db_singleton import SQLSingleton: Imports the SQLSingleton class, which is a singleton pattern implementation for managing a database connection. It is imported but not used directly in this script, so it might be used within the create_app function or other parts of the application.

# Main Execution Block:

#     if __name__ == "__main__":: Ensures that the script runs only if it is executed directly, not when it is imported as a module in another script.
#     app = create_app(): Calls the create_app function to create a Flask application instance.
#     app.run(debug=True): Starts the Flask application in debug mode, which provides detailed error messages and enables auto-reloading of the application when code changes are detected.