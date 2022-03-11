import os


class ModelConfig:
    APP_DIR = os.environ["APP_DIR"]
    LABEL_PATH = os.path.join(APP_DIR, "models/data/imagenet_classes.txt")
    PREDICTION_PATH = os.path.join(APP_DIR, "models/prediction.pkl")
    ONNX_MODEL_PATH = os.path.join(APP_DIR, "models/resnet101.onnx")


class AppConfig:
    pass
