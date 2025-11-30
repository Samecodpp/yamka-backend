import grpc
from concurrent import futures
from model_init import init_model, predict
import ml_service_pb2
import ml_service_pb2_grpc

yamka_model = init_model()
print("ML model initialized and ready to serve.")

class MLServiceServicer(ml_service_pb2_grpc.MLServiceServicer):
    def Predict(self, request, context):
        features = request.features
        prediction = predict(yamka_model, features)
        return ml_service_pb2.PredictResponse(prediction=prediction)

server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
ml_service_pb2_grpc.add_MLServiceServicer_to_server(MLServiceServicer(), server)
server.add_insecure_port('[::]:50051')
server.start()
print("gRPC server listening on port 50051")
server.wait_for_termination()
