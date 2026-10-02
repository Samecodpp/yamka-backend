from pydantic import BaseModel


class IngestTelemetriesResponse(BaseModel):
    message: str | None
