from __future__ import annotations
import json
import requests
import io
from PIL import Image
from fastapi import APIRouter, Request, UploadFile
# from src.ml.prediction import classifier

router = APIRouter()
PREDICT_URL = "http://host.docker.internal:8080/predictions/resnet101"

def image_to_byte_array(image:Image):
  imgByteArr = io.BytesIO()
  image.save(imgByteArr, format=image.format)
  imgByteArr = imgByteArr.getvalue()
  return imgByteArr


@router.post("/predict")
def predict(file: UploadFile = None):
    img_bytes = file.file._file
    res = requests.post(PREDICT_URL, data=img_bytes)
    if res.status_code == 200:
        output = res.json()
        return output
    return res.json()


@router.get("/predict/test")
def predict_test() -> dict[str, float]:
    img_path = "/app/data/bobby.jpg"
    with Image.open(img_path) as img:
        img_bytes = image_to_byte_array(img)
    res = requests.post(PREDICT_URL, data=img_bytes)
    if res.status_code == 200:
        output = res.json()
        return output
    return res.json()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "Healthy"}


@router.get("/health_torchserve")
def health_torchserve() -> dict[str, str]:
    url = "http://host.docker.internal:8080/ping"
    res = requests.post(url)
    if res.status_code == 200:
        return res.json()
    return {"status": res.json()}
