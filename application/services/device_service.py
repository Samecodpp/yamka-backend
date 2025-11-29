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
    def store_report(device: Device, validated_data: dict) -> DeviceReport:
        report = DeviceReport(
            device_id=device.id,
            _location=validated_data['location'],
            speed=validated_data.get('speed'),
            vibration=validated_data.get('vibration'),
            accel=validated_data.get('accel'),
            gyro=validated_data.get('gyro')
        )
        db.session.add(report)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return None

        return report
