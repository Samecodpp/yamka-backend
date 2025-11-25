from sqlalchemy.exc import IntegrityError
from application import db, bcrypt
from application.models import User


def register_user(username:str, email: str, password: str):
    existing = User.query.filter_by(email=email).first()
    if existing:
        return None

    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return None

    return user


def authenticate_user(email: str, password: str):
    user = User.query.filter_by(email=email).first()
    if not user:
        return None
    if user.check_password(password):
        return user
    return None
