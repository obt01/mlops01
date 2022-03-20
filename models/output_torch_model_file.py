import os
import torch
from torchvision import models  # type: ignore

DEFAULT_MODEL_NAME = os.environ["MODEL_NAME"]


class TorchModel:
    def __init__(self, model_name: str = DEFAULT_MODEL_NAME):
        self.model_name = model_name

    def load_model(self) -> models:
        model = getattr(models, self.model_name)(pretrained=True)
        return model

    def save_model(self, model: models) -> None:
        model.eval()
        example_input = torch.rand(1, 3, 224, 224)
        traced_script_module = torch.jit.trace(model, example_input)
        traced_script_module.save(f"{self.model_name}.pt")


if __name__ == "__main__":
    torch_model = TorchModel()
    model = torch_model.load_model()
    torch_model.save_model(model)
