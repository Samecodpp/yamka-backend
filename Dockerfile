FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev gcc \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd -ms /bin/bash appuser && chown -R appuser:appuser /app
USER appuser

ENV FLASK_APP=app.py
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:8000", "app:app"]
