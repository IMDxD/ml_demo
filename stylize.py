import torch
from torch import nn
from torchvision import transforms
from PIL import Image

from style_models import load_image, convert_from_tensor, load_model


TO_TENSOR = transforms.Compose([
    transforms.Resize(512),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])


def stylize(content_image: Image, style_model: nn.Module) -> Image:

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    content_image = TO_TENSOR(content_image)
    content_image = content_image.unsqueeze(0).to(device)

    with torch.no_grad():
        output = style_model(content_image).cpu()

    img = convert_from_tensor(output.squeeze(0))
    return img


def stylize_image(file, style: str) -> Image:

    content_image = load_image(file)
    orig_size = content_image.size
    style_model = load_model(style)

    img = stylize(content_image, style_model)
    img = img.resize(orig_size)
    return img
