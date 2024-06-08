#!/usr/bin/python3
from app import create_app
from flask_cors import CORS
from flask import make_response, jsonify
from flasgger import Swagger


# Create the Flask application
app = create_app()

# Set the secret key and other configurations

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['SWAGGER'] = {
    'title': 'Restaurant Management Portfolio Project Restful API',
    'uiversion': 3
}

app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['REMEMBER_COOKIE_SECURE'] = True
app.config['REMEMBER_COOKIE_HTTPONLY'] = True
from datetime import timedelta

app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=1)  
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

Swagger(app)

@app.teardown_appcontext
def close_db(error):
    """Close Storage"""
    pass

# Error handler for 404 errors
@app.errorhandler(404)
def not_found(error):
    """
    404 Error
    ---
    responses:
      404:
        description: A resource was not found
    """
    return make_response(jsonify({'error': "Not found"}), 404)

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
