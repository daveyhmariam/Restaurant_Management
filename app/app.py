#!/usr/bin/python3
from app import create_app
from flask_cors import CORS
from flask import make_response, jsonify
from flasgger import Swagger
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_session import Session
import secrets

# Create the Flask application
app = create_app()

# Set the secret key and other configurations
app.config['SECRET_KEY'] = secrets.token_hex(32)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['SWAGGER'] = {
    'title': 'Restaurant Management Portfolio Project Restful API',
    'uiversion': 3
}

app.config['SESSION_COOKIE_SECURE'] = False
app.config['CSRF_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['REMEMBER_COOKIE_SECURE'] = True
app.config['REMEMBER_COOKIE_HTTPONLY'] = True
from datetime import timedelta

app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=1)  
app.config['WTF_CSRF_ENABLED'] = False
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1)

app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

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
