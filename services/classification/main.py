import logging
import warnings
from concurrent import futures

import grpc

from .infrastructure.core.settings import get_settings
from .infrastructure.core.grpc import classification_pb2_grpc
from .infrastructure.loaders.artefact_loader import S3ArtifactLoader
from .infrastructure.ml.classifier_impl import Classifier
from .infrastructure.ml.normalizer_impl import Normalizer
from .application.use_cases.classify_anomaly_use_case import ClassifyAnomalyUseCase
from .presentation.grpc.classification_servicer import AnomalyClassificationServicer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
for _noisy in ("botocore", "boto3", "urllib3", "s3transfer"):
    logging.getLogger(_noisy).setLevel(logging.WARNING)
warnings.filterwarnings("ignore", category=UserWarning, module="sklearn")
warnings.filterwarnings("ignore", category=UserWarning, module="xgboost")
logger = logging.getLogger(__name__)


def main() -> None:
    settings = get_settings()

    loader = S3ArtifactLoader(
        bucket=settings.S3_BUCKET,
        model_key=settings.S3_MODEL_KEY,
        scaler_key=settings.S3_SCALER_KEY,
        region_name=settings.AWS_REGION,
    )

    logger.info("Loading model from S3: %s", settings.S3_MODEL_KEY)
    model = loader.load_model()
    logger.info("Model loaded. metadata=%s", model.metadata)

    logger.info("Loading scaler from S3: %s", settings.S3_SCALER_KEY)
    exported_normalizer = loader.load_scaler()
    logger.info("Scaler loaded. metadata=%s", exported_normalizer.metadata)

    normalizer = Normalizer(exported_normalizer)
    classifier = Classifier(model)
    use_case = ClassifyAnomalyUseCase(normalizer=normalizer, classifier=classifier)
    servicer = AnomalyClassificationServicer(use_case)

    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=settings.GRPC_MAX_WORKERS)
    )
    classification_pb2_grpc.add_AnomalyClassificationServiceServicer_to_server(
        servicer, server
    )
    server.add_insecure_port(f"[::]:{settings.GRPC_PORT}")
    server.start()
    logger.info("Classification gRPC server started on port %s", settings.GRPC_PORT)
    server.wait_for_termination()


if __name__ == "__main__":
    main()
