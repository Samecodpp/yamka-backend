from application import db, bcrypt
from sqlalchemy.dialects.postgresql import JSONB, TIMESTAMP
from sqlalchemy import func

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)


class Device(db.Model):
    __tablename__ = 'devices'
    id = db.Column(db.Integer, primary_key=True)
    device_name = db.Column(db.String(255), nullable=False)
    mac_address = db.Column(db.String(17), unique=True, nullable=False)
    registered_at = db.Column(db.DateTime, default=func.now())
    activated_at = db.Column(db.DateTime, default=func.now(), nullable=True)
    reports = db.relationship('DeviceReport', backref='device', lazy=True, cascade="all, delete-orphan")


class DeviceReport(db.Model):
    __tablename__ = 'device_reports'
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey('devices.id', ondelete='CASCADE'), nullable=False)
    _location = db.Column(JSONB, nullable=False)
    speed = db.Column(db.Float)
    vibration = db.Column(db.Integer)
    accel = db.Column(JSONB)
    gyro = db.Column(JSONB)
    reported_at = db.Column(db.DateTime, default=func.now())
    pothole_id = db.Column(db.Integer, db.ForeignKey('potholes.id'))
    pothole = db.relationship('Pothole', backref=db.backref('reports', lazy=True))

class Pothole(db.Model):
    __tablename__ = 'potholes'
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    score = db.Column(db.Integer, nullable=False)
    report_count = db.Column(db.Integer, default=1)
    confirmed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())
