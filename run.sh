#!/bin/bash

set -eu

APP_NAME="src.app.main:app"
HOST="0.0.0.0"
PORT="8000"
WORKERS=2
UVICORN_WORKER="uvicorn.workers.UvicornWorker"
LOG_LEVEL="info"
BACKLOG=2048
MAX_REQUESTS=8192
MAX_REQUESTS_JITTER=512

uvicorn ${APP_NAME} \
    --host ${HOST} \
    --port ${PORT} \
    --reload

# gunicorn ${APP_NAME} \
#     -b ${HOST}:${PORT} \
#     -w ${WORKERS} \
#     -k ${UVICORN_WORKER} \
#     --log-level ${LOG_LEVEL} \
#     # --log-config ${LOGCONFIG} \
#     --backlog ${BACKLOG} \
#     --max-requests ${MAX_REQUESTS} \
#     --max-requests-jitter ${MAX_REQUESTS_JITTER} \
#     --reload
