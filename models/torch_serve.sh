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

torch-model-archiver \
  --model-name=${MODEL_NAME} \
  --version=1.0 \
  --serialized-file=${MODEL_NAME}.pt \
  --extra-files=./data/resnet_labels.json \
  --handler=image_classifier \
  --export-path=

CMD ["torch-model-archiver", \
     "--model-name=${MODEL_NAME}", \
     "--version=1.0", \
     "--serialized-file=${MODEL_NAME}.pt", \
     "--extra-files=${MODEL_SERVER_DIR}/data/resnet_labels.json", \
     "--handler=image_classifier", \
     "--export-path=${MODEL_STORE_DIR}"]

# RUN torch-model-archiver \
#   --model-name=resnet101 \
#   --version=1.0 \
#   --serialized-file=resnet-101.pt \
#   --extra-files=./data/resnet_labels.json \
#   --handler=image_classifier \
#   --export-path=model-store

CMD ["torchserve", "--start", \
     "--ncs", \
     "--model-store", "${MODEL_STORE_DIR}", \
     "--ts-config", "config.properties", \
     "--models", "resnet101=${MODEL_NAME}.mar"]