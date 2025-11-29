from . import create_app, db
from .celery_app import make_celery
from flask import current_app
from .models import DeviceReport
from .services.pothole_service import PotholeService
import pandas as pd

app = create_app()
celery = make_celery(app)

@celery.task
def process_pothole_report(report_id: int):
    with app.app_context():
        print(f"Processing pothole report {report_id} is started!")

        report = DeviceReport.query.get(report_id)
        if not report:
            print(f"Report {report_id} not found!")
            return

        model = current_app.yamka_model['model']
        scaler = current_app.yamka_model['scaler']

        try:
            accel = report.accel or {}
            gyro = report.gyro or {}
            location = report._location or {}

            features_dict = {
                "speed": float(report.speed or 0.0),
                "accelerometerX": float(accel.get('x', 0.0)),
                "accelerometerY": float(accel.get('y', 0.0)),
                "accelerometerZ": float(accel.get('z', 0.0)),
                "gyroX": float(gyro.get('x', 0.0)),
                "gyroY": float(gyro.get('y', 0.0)),
                "gyroZ": float(gyro.get('z', 0.0)),
            }

            df = pd.DataFrame([features_dict])

            X_scaled = scaler.transform(df)
            prediction = model.predict(X_scaled)[0]

            print(f"Report {report_id}: Prediction = {prediction}")

            if prediction >= 1:
                score = int(prediction) + 1

                lat = location.get('lat')
                lon = location.get('lon')

                if lat and lon:
                    pothole_data = {
                        'lat': float(lat),
                        'lon': float(lon),
                        'score': score,
                    }

                    pothole = PotholeService.register_pothole(pothole_data)

                    if pothole:
                        report.pothole_id = pothole.id
                        db.session.commit()

                        print(f"Report {report_id}: Pothole registered (ID: {pothole.id}, severity: {prediction})")
                        return
                    else:
                        print(f"Report {report_id}: Failed to register pothole")
                        return
                else:
                    print(f"Report {report_id}: Missing location data")
                    return
            else:
                print(f"Report {report_id}: No pothole detected")
                return

        except Exception as e:
            print(f"Report {report_id}: Error - {str(e)}")
            import traceback
            traceback.print_exc()
            db.session.rollback()
            return
