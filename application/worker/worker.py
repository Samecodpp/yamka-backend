from celery import Celery
import os
from dotenv import load_dotenv
import grpc
from . import ml_service_pb2
from . import ml_service_pb2_grpc

load_dotenv()

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

def get_prediction(features: dict):
    """Call ML service via gRPC to get pothole prediction"""
    try:
        channel = grpc.insecure_channel("ml-service:50051")
        stub = ml_service_pb2_grpc.MLServiceStub(channel)

        feature_list = [features['speed'], features['accelerometerX'], features['accelerometerY'],
                        features['accelerometerZ'], features['gyroX'], features['gyroY'], features['gyroZ']]

        request = ml_service_pb2.PredictRequest(features=feature_list)
        response = stub.Predict(request)
        return response.prediction
    except Exception as e:
        raise

from .tasks import *

if __name__ == "__main__":
    celery.start()
