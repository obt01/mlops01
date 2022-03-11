FROM python:3.9-slim

RUN apt update && \
    apt upgrade -y && \
    apt install -y nodejs npm && \
    pip install --upgrade pip

WORKDIR /app

COPY requirements.txt ${PWD}

RUN pip install -r requirements.txt

# # PyTorch
# RUN pip install --pre torch torchvision -f https://download.pytorch.org/whl/nightly/cpu/torch_nightly.html

# PyTorch
RUN pip install torch==1.10.2+cpu torchvision==0.11.3+cpu torchaudio==0.10.2+cpu -f https://download.pytorch.org/whl/cpu/torch_stable.html