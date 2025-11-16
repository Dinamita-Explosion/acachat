FROM python:3.12-slim AS server

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    BACKEND_HOST=0.0.0.0 \
    FLASK_ENV=production

WORKDIR /app

# System dependencies for building bcrypt/cryptography
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential && \
    rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gunicorn

COPY backend/ .

RUN useradd --create-home appuser && \
    chown -R appuser:appuser /app

USER appuser

EXPOSE 5001

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "--workers", "3", "run:app"]
