from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
from redis import Redis
import os

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
bcrypt = Bcrypt()
redis_client = None

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('TRACK_MODIFICATIONS', 'False').lower() == 'true'

    db.init_app(app)
    migrate.init_app(app, db)
    with app.app_context():
        db.create_all()
        print("Database tables created or verified.")

    login_manager.init_app(app)
    bcrypt.init_app(app)

    global redis_client
    redis_client = Redis(host=os.getenv('REDIS_HOST'), port=int(os.getenv('REDIS_PORT', 6379)))

    if redis_client.ping():
        print("Connected to Redis successfully!")

    from .celery_app import make_celery
    app.celery = make_celery(app)

    from .controllers import auth_bp, device_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(device_bp, url_prefix='/device')

    return app
