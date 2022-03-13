import os
import torch
from torchvision import models  # type: ignore

model_name = os.environ["MODEL_NAME"]


def load_model(model_name: str = model_name) -> models:
    model = getattr(models, model_name)(pretrained=True)
    return model


def save_model(model: models) -> None:
    model.eval()
    example_input = torch.rand(1, 3, 224, 224)
    traced_script_module = torch.jit.trace(model, example_input)
    traced_script_module.save(f"{model_name}.pt")


if __name__ == "__main__":
    model = load_model()
    save_model(model)
