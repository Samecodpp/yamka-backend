from sqlalchemy.exc import IntegrityError
from application import db
from application.models import Device, DeviceReport

class DeviceService:
    @staticmethod
    def registred_device(device_name: str, mac_address: str) -> Device:
        existing = Device.query.filter_by(mac_address=mac_address).first()
        if existing:
            return existing

        device = Device(device_name=device_name, mac_address=mac_address)
        db.session.add(device)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return None

        return device
    
    @staticmethod
    def valid_data(data: dict) -> bool:
        required_keys = {"device_name", "mac_address", "lat", "lon", "speed", "accel_x", "accel_y", "accel_z", "gyro_x", "gyro_y", "gyro_z"}
        return required_keys.issubset(set(data.keys()))
    
    @staticmethod
    def store_report(device: Device, payload: dict) -> DeviceReport:
        report =  DeviceReport(
            device_id=device.id,
            _location={"lat": payload['lat'], "lon": payload['lon']},
            speed=payload['speed'],
            vibration=payload['vibration'],
            accel={"x": payload['accel_x'], "y": payload['accel_y'], "z": payload['accel_z']},
            gyro={"x": payload['gyro_x'], "y": payload['gyro_y'], "z": payload['gyro_z']}
        )
        db.session.add(report)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return None
        
        return report