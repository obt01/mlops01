from __future__ import annotations
import requests
import json
from fastapi import APIRouter
import urllib.request
import urllib.parse
# from src.ml.prediction import classifier

router = APIRouter()


# data = urllib.parse.urlencode({'foo': 'bar'}).encode('utf-8')
# request = urllib.request.Request('http://www.example.com', data)
# response = urllib.request.urlopen(request)
# print(response.getcode())
# html = response.read()
# print(html.decode('utf-8'))

@router.get("/health")
def health() -> dict[str, str]:
    """
    ヘルスチェック
    """
    return {"health": "ok"}


@router.get("/health_torchserve")
def health_torchserve() -> dict[str, str]:
    """
    ヘルスチェック
    """
    res = urllib.request.urlopen("http://localhost:8080/ping")
    # res = urllib.request.urlopen("https://google.com")
    # res = requests.get("http://host.docker.internal:8080/ping")
    # res = requests.get("https://google.com")
    return {"health": res}


@router.get("/predict/test")
def predict_test() -> dict[str, float]:
    """
    推論テスト
    """
    img_path = "/app/data/bobby.jpg"
    url = "http://host.docker.internal:8080/predictions/resnet101"
    with open(img_path, "rb") as img:
        data = json.dumps({"data": img})
        # print(vars(img))
        res = requests.post(url, files=data)
    return res
