import numpy as np
from PIL import Image
import torch
from torchvision import models
from torchvision import transforms
from src.configure import ModelConfig as conf


class ImageClassifier:
    """
    画像分類モデル
    """
    def __init__(self,
                 model_name: str = 'resnet101',
                 labels_filepath: str = conf.LABEL_PATH):
        self.model = self.load_model(model_name)
        self.labels = self.load_labels(labels_filepath)

    @staticmethod
    def load_model(model_name: str):
        """
        モデルをロード
        """
        model = getattr(models, model_name)(pretrained=True)
        return model

    @staticmethod
    def load_labels(filepath: str):
        """
        ラベル名をロード
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            labels = [line.strip() for line in f.readlines()]
        return labels

    @staticmethod
    def open_image(img_path: str) -> Image:
        """
        画像ファイルを開いてRGB形式に変換する
        """
        img = Image.open(img_path)
        img = img.convert("RGB")
        return img

    @staticmethod
    def preprocess(img: Image) -> np.ndarray:
        """
        画像前処理
        """
        proc = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
                )
            ])
        preprocessed = torch.unsqueeze(proc(img), 0).numpy()
        return preprocessed

    @staticmethod
    def postprocess(output: np.ndarray, labels: list[str]) -> tuple:
        """
        推論結果からラベル名・確率を取得
        """
        output = output.reshape(-1)
        percentage = np.exp(output)/sum(np.exp(output))
        index = np.argmax(percentage)
        pred_label = labels[index]
        pred_proba = percentage[index]
        return pred_label, pred_proba

    def predict(self, img_path: str) -> dict[str, float]:
        """
        推論処理
        """
        # 画像ファイルの前処理
        img = self.open_image(img_path)
        preprocessed_img = self.preprocess(img)

        # 推論
        self.model.eval()
        output = self.model(preprocessed_img)

        # 推論結果からラベル名と確率を取得
        pred_label, pred_proba = self.postprocess(output, self.labels)
        return {pred_label: pred_proba}


# classifier = ImageClassifier()


if __name__ == '__main__':
    result = classifier.predict(img_path="../../data/sample/bobby.jpg")
    print(result)
