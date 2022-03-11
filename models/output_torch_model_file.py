import torch
from torchvision import models  # type: ignore


def load_model(model_name: str = "resnet101") -> models:
    model = getattr(models, model_name)(pretrained=True)
    return model


def save_model(model: models) -> None:
    model.eval()
    example_input = torch.rand(1, 3, 224, 224)
    traced_script_module = torch.jit.trace(model, example_input)
    traced_script_module.save("resnet-101.pt")


if __name__ == "__main__":
    model = load_model()
    save_model(model)
