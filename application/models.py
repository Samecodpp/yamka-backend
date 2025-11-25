from application import db, bcrypt
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)


class Device(db.Model):
    __tablename__ = 'devices'
    id = db.Column(db.Integer, primary_key=True)
    device_name = db.Column(db.String(255), nullable=False)
    mac_address = db.Column(db.String(17), unique=True, nullable=False)
    registred_at = db.Column(db.DateTime, default=datetime.utcnow)
    activated_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)
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
    reported_at = db.Column(db.DateTime, default=datetime.utcnow)
    pothole_id = db.Column(db.Integer, db.ForeignKey('potholes.id'))
    pothole = db.relationship('Pothole', backref=db.backref('reports', lazy=True))

class Pothole(db.Model):
    __tablename__ = 'potholes'
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Double, nullable=False)
    longitude = db.Column(db.Double, nullable=False)
    score = db.Column(db.Integer, nullable=False)
    report_count = db.Column(db.Integer, default=1)
    confirmed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)