#!/bin/bash

set -eu

HTTP_PORT=8001
GRPC_PORT=50051
NUM_HTTP_THREADS=2
MODEL_PATH="/app/models/resnet101.onnx"

./onnxruntime_server \
    --http_port=${HTTP_PORT} \
    --grpc_port=${GRPC_PORT} \
    --num_http_threads=${NUM_HTTP_THREADS} \
    --model_path=${MODEL_PATH}
