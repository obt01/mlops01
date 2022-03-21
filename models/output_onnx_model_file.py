import torch
import torchvision
import os
import onnxruntime
from src.ml.prediction_onnx import ImageClassifier
from src.configure import ModelConfig as conf


MODEL_NAME = "resnet101"

def load_model(model_name: str):
    model = getattr(torchvision.models, model_name)(pretrained=True)
    return model

x_dummy = torch.rand((1, 3, 224, 224), device="cpu")
model = load_model(MODEL_NAME)
onnx_filename = MODEL_NAME + ".onnx"

model.eval()
torch.onnx.export(model,
                  x_dummy,
                  onnx_filename,
                  input_names=["input"],
                  output_names=["output"],
                  verbose=True,
                  )

img = ImageClassifier.open_image("../data/sample/bobby.jpg")
preprocessed_img = ImageClassifier.preprocess(img)
sess = onnxruntime.InferenceSession(onnx_filename)
outputs = sess.run(['output'], {'input': preprocessed_img})[0]
print(outputs)
labels = ImageClassifier.load_labels(conf.LABEL_PATH)
res = ImageClassifier.postprocess(outputs, labels)
print(res)

