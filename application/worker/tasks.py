from .worker import celery, get_prediction, flask_app
from application.models import DeviceReport
from application.services.pothole_service import PotholeService
from application import db

@celery.task(name='worker.predict_pothole_score')
def predict_pothole_score(report_id: int):
    """Process device report and predict pothole severity"""
    with flask_app.app_context():
        print(f"Processing pothole report with ID: {report_id}")

        # Get report from database
        report = DeviceReport.query.get(report_id)
        if not report:
            print(f"Report with ID {report_id} not found")
            return {"error": "Report not found"}

        # Extract features from report
        features = [
            float(report.speed or 0.0),
            float(report.accel.get('x', 0.0)) if report.accel else 0.0,
            float(report.accel.get('y', 0.0)) if report.accel else 0.0,
            float(report.accel.get('z', 0.0)) if report.accel else 0.0,
            float(report.gyro.get('x', 0.0)) if report.gyro else 0.0,
            float(report.gyro.get('y', 0.0)) if report.gyro else 0.0,
            float(report.gyro.get('z', 0.0)) if report.gyro else 0.0,
        ]

        print(f"Features extracted: {features}")

        try:
            prediction = get_prediction(features)
            print(f"Predicted pothole severity for report {report_id}: {prediction}")

            # Register pothole with prediction
            pothole = PotholeService.register_pothole({
                "score": prediction,
                "lat": report._location.get('lat'),
                "lon": report._location.get('lon')
            })

            # Link report to pothole
            if pothole:
                report.pothole_id = pothole.id
                db.session.commit()
                print(f"Report {report_id} linked to pothole {pothole.id}")

            return {"status": "success", "report_id": report_id, "prediction": prediction, "pothole_id": pothole.id if pothole else None}
        except Exception as e:
            print(f"Error getting prediction: {str(e)}")
            return {"error": str(e)}

@celery.task
def test_task(x, y):
    print(f"Test task called with arguments: {x}, {y}")
    return x + y
