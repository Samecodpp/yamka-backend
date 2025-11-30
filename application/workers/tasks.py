from os import name
from .worker import celery, get_prediction

@celery.task(name='worker.predict_pothole_score')
def predict_pothole_score(report_id: int):
    print(f"Processing pothole report with ID: {report_id}")

    return

@celery.task
def test_task(x, y):
    print(f"Test task called with arguments: {x}, {y}")
    return x + y
