from __future__ import annotations
from fastapi import APIRouter
from src.ml.prediction import classifier

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    """
    ヘルスチェック
    """
    return {"health": "ok"}


@router.get("/predict/test")
def predict_test() -> dict[str, float]:
    """
    推論テスト
    """
    img_path = "/app/data/sample/bobby.jpg"
    pred = classifier.predict(img_path)
    return pred
