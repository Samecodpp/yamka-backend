import io

import boto3
import joblib

from ...domain.interfaces.artifact_loader import IArtifactLoader
from ..ml.exported_model import ExportedModel, ExportedNormalizer


class S3ArtifactLoader(IArtifactLoader):

    def __init__(
        self,
        bucket: str,
        model_key: str,
        scaler_key: str,
        region_name: str,
    ) -> None:
        self._bucket = bucket
        self._model_key = model_key
        self._scaler_key = scaler_key
        self._s3 = boto3.client("s3", region_name=region_name)

    def load_model(self) -> ExportedModel:
        return self._load(self._model_key)

    def load_scaler(self) -> ExportedNormalizer:
        return self._load(self._scaler_key)

    def _load(self, key: str):
        response = self._s3.get_object(Bucket=self._bucket, Key=key)
        buffer = io.BytesIO(response["Body"].read())
        return joblib.load(buffer)
