from sqlalchemy.exc import IntegrityError
from application import db
from .cache_service import CacheService
from application.models import User

def register_user(username:str, email: str, password: str):
    try:
        existing = CacheService.get_json(f"user:{email}")
    except Exception:
        print("Failed to retrieve user data from cache")
        existing = None

    if existing:
        return None

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
        print("Failed to commit user to database")
        return None

    try:
        CacheService.set_json(f"user:{email}", {
            "id": user.id,
            "username": user.username,
            "email": user.email,
        }, ttl=3600)
    except Exception:
        print("Failed to cache user data")

    return user

def authenticate_user(email: str, password: str):
    try:
        cached_user = CacheService.get_json(f"user:{email}")
    except Exception:
        cached_user = None
    if not cached_user:
        user = User.query.filter_by(email=email).first()
    else:
        user = User.query.get(cached_user['id'])
    if not user:
        return None
    if not user.check_password(password):
        return None
    try:
        CacheService.set_json(f"user:{email}", {"id": user.id, "username": user.username, "email": user.email}, ttl=3600)
    except Exception:
        print("Failed to cache user data")
    return user
