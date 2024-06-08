from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from models import storage  # Import storage here
from flask_login import LoginManager
import secrets
from flask_wtf import CSRFProtect


bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)


    secret_key = secrets.token_urlsafe(32)
    app.secret_key = secret_key
    csrf = CSRFProtect()

    csrf.init_app(app)
    bcrypt.init_app(app)

    # Initialize Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = 'site.login'

    # Import and register blueprints inside the function to avoid circular imports
    from app.api import api
    from app.site import site
    app.register_blueprint(api)
    app.register_blueprint(site)

    @login_manager.user_loader
    def load_user(user_id):
        from models.users import User
        return storage.get(User, user_id)

    return app
