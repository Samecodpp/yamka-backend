from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
bcrypt = Bcrypt()
from .celery_app import make_celery

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('TRACK_MODIFICATIONS')
    
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    # initialize celery and attach to app so web process can enqueue tasks
    try:
        celery = make_celery(app)
        app.celery = celery
    except Exception:
        # if celery cannot be initialized here, continue without it
        app.celery = None
    
    from .controllers import auth_bp, device_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(device_bp, url_prefix='/device')
    
    return app