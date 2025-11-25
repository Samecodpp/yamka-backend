from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
from application import db
from application.models import Pothole
import math

class PotholeService:
    @staticmethod
    def _distance_expr(lat_col, lon_col, lat_value, lon_value):
        R = 6371000.0
        dlat = func.radians(lat_value - lat_col)
        dlon = func.radians(lon_value - lon_col)
        a = (
            func.pow(func.sin(dlat / 2.0), 2)
            + func.cos(func.radians(lat_col))
            * func.cos(func.radians(lat_value))
            * func.pow(func.sin(dlon / 2.0), 2)
        )
        c = 2.0 * func.asin(func.sqrt(a))
        return R * c
    
    @staticmethod
    def register_pothole(data: dict) -> Pothole:
        existing = Pothole.query.filter(
            PotholeService._distance_expr(Pothole.latitude, Pothole.longitude, data['lat'], data['lon']) <= 5.0
        ).first()
        
        if existing:
            existing.report_count += 1
            existing.score = data['score']
            return existing
        
        pothole = Pothole(
            latitude=data['lat'],
            longitude=data['lon'],
            score=data['score'],
            report_count=1
            )
        
        db.session.add(pothole)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return None
        
        return pothole
            
    @staticmethod
    def evaluate(data: dict):
        accel = math.sqrt(math.pow(data["accel_x"], 2) + math.pow(data["accel_y"], 2) + math.pow(data["accel_z"], 2))
        gyro = math.sqrt(math.pow(data["gyro_x"], 2) + math.pow(data["gyro_y"], 2) + math.pow(data["gyro_z"], 2))
        score = int(0.5 * accel + 0.5 * gyro + 0.5 * data["speed"] + 0.5 * data["vibration"])
        return score