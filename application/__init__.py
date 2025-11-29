from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
from .services.ml import model_init
from redis import Redis
import os

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
bcrypt = Bcrypt()

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

    yamka_model = model_init.init_model()
    app.yamka_model = yamka_model

    from .celery_app import make_celery
    try:
        celery = make_celery(app)
        app.celery = celery
    except Exception:
        app.celery = None

    from .controllers import auth_bp, device_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(device_bp, url_prefix='/device')

    return app
