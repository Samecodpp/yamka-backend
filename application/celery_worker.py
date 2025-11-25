from . import create_app
from .celery_app import make_celery

app = create_app()
celery = make_celery(app) 

@celery.task
def process_pothole_report(report_id: int):
    print(f"Processing pothole report {report_id} is started!")
    return