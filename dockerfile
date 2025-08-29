# syntax=docker/dockerfile:1
FROM python:3.12.3-slim

# ---- Base env ----
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=8000 \
    WEB_CONCURRENCY=2 \
    APP_HOME=/app \
    VIRTUAL_ENV=/opt/venv

WORKDIR $APP_HOME

# ---- System deps (add build-essential only if wheels fail) ----
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# ---- Virtualenv for clean site-packages ----
RUN python -m venv $VIRTUAL_ENV && $VIRTUAL_ENV/bin/pip install --upgrade pip wheel
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# ---- Install Python deps (cached layer) ----
COPY requirements.txt .
RUN pip install -r requirements.txt

# ---- Non-root user ----
RUN adduser --disabled-password --gecos '' appuser
USER appuser

# ---- App code ----
COPY . .

EXPOSE 8000

# If your entrypoint isn’t main:app, change it (e.g., src.api:app)
CMD ["sh", "-c", "gunicorn -k uvicorn.workers.UvicornWorker -w ${WEB_CONCURRENCY:-2} -b 0.0.0.0:${PORT:-8000} main:app"]
