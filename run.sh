#!/bin/bash

set -eu

APP_NAME="src.app.main:app"
APP_HOST="0.0.0.0"
APP_PORT="8010"
# WORKERS=2
# UVICORN_WORKER="uvicorn.workers.UvicornWorker"
# LOG_LEVEL="info"
# BACKLOG=2048
# MAX_REQUESTS=8192
# MAX_REQUESTS_JITTER=512

uvicorn ${APP_NAME} \
    --host ${APP_HOST} \
    --port ${APP_PORT} \
    --reload

# gunicorn ${APP_NAME} \
#     -b ${APP_HOST}:${APP_PORT} \
#     -w ${WORKERS} \
#     -k ${UVICORN_WORKER} \
#     --log-level ${LOG_LEVEL} \
#     # --log-config ${LOGCONFIG} \
#     --backlog ${BACKLOG} \
#     --max-requests ${MAX_REQUESTS} \
#     --max-requests-jitter ${MAX_REQUESTS_JITTER} \
#     --reload
