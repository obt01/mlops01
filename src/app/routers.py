from __future__ import annotations
import json
import requests
import io
from PIL import Image
from fastapi import APIRouter, Request, UploadFile
from src.ml.predictions import ImageClassifier


router = APIRouter()


@router.post("/predict")
def predict(file: UploadFile):
    with Image.open(io.BytesIO(file.file.read())) as img:
        res = ImageClassifier.predict(img_data=img, img_format=img.format)
    return res


@router.get("/predict/test")
def predict_test() -> dict[str, float]:
    img_path = "/app/data/bobby.jpg"
    with Image.open(img_path) as img:
        res = ImageClassifier.predict(img_data=img, img_format=img.format, use_cache=False)
    return res


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "Healthy"}


@router.get("/health/torchserve")
def health_torchserve() -> dict[str, str]:
    url = "http://host.docker.internal:8080/ping"
    res = requests.post(url)
    if res.status_code == 200:
        return res.json()
    return {"status": res.json()}
