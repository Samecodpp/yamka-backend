from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

_ENV_FILE = Path(__file__).parent.parent.parent / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=_ENV_FILE)

    GRPC_PORT: int = 50052
    GRPC_MAX_WORKERS: int = 4

    AWS_REGION: str
    S3_BUCKET: str
    S3_MODEL_KEY: str
    S3_SCALER_KEY: str


_settings: Settings | None = None


def get_settings() -> Settings:
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
