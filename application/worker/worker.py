from celery import Celery
import os
from dotenv import load_dotenv
import grpc
from . import ml_service_pb2
from . import ml_service_pb2_grpc

load_dotenv()

# Create Flask app for database access
def create_flask_app():
    from flask import Flask
    from application import db

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    return app

flask_app = create_flask_app()

celery = Celery(
    "worker",
    broker=os.getenv("CELERY_BROKER_URL", "amqp://guest:guest@rabbitmq:5672//"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0")
)

celery.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

def get_prediction(features: list):
    """Call ML service via gRPC to get pothole prediction"""
    try:
        channel = grpc.insecure_channel("ml-service:50051")
        stub = ml_service_pb2_grpc.MLServiceStub(channel)

        # features is already a list
        print(f"Sending features to ML service: {features}")
        request = ml_service_pb2.PredictRequest(features=features)
        response = stub.Predict(request)
        return response.prediction
    except Exception as e:
        print(f"Error calling ML service: {e}")
        raise

from .tasks import *

if __name__ == "__main__":
    celery.start()
