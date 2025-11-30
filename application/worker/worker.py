from celery import Celery
import os
from dotenv import load_dotenv

load_dotenv()

celery = Celery(
    "worker",
    broker=os.getenv("CELERY_BROKER_URL"),
    backend=os.getenv("CELERY_RESULT_BACKEND")
)

from .tasks import *
if  __name__ == "__main__":
    print("Celery worker is running")
