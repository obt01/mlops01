#!/bin/bash

set -eu

MODEL_NAME=resnet101
MODEL_SERVER_DIR=/home/model-server
MODEL_STORE_DIR=${MODEL_SERVER_DIR}/model-store

# COPY --from=builder ${BUILDER_HOME}/${MODEL_NAME}.pt ${MODEL_SERVER_DIR}
# COPY --from=builder ${BUILDER_HOME}/data ${MODEL_SERVER_DIR}/data

torch-model-archiver \
  --model-name=${MODEL_NAME} \
  --version=1.0 \
  --serialized-file=${MODEL_NAME}.pt \
  --extra-files=./data/resnet_labels.json \
  --handler=image_classifier \
  --export-path=${MODEL_STORE_DIR}

torchserve \
  --start \
  --ncs \
  --model-store ${MODEL_STORE_DIR} \
  --ts-config config.properties \
  --models ${MODEL_NAME}=${MODEL_NAME}.mar
