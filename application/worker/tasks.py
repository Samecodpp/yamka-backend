from os import name
from .worker import celery, get_prediction

@celery.task(name='worker.predict_pothole_score')
def predict_pothole_score(report_id: int):
    print(f"Processing pothole report with ID: {report_id}")
    prediction = get_prediction({'speed': 50.0, 'accelerometerX': 0.1, 'accelerometerY': 0.2, 'accelerometerZ': 0.3,
                                 'gyroX': 0.01, 'gyroY': 0.02, 'gyroZ': 0.03})
    print(f"Predicted pothole severity for report {report_id}: {prediction}")
    return

@celery.task
def test_task(x, y):
    print(f"Test task called with arguments: {x}, {y}")
    return x + y

