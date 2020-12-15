import re

import torch
from torch import nn
from PIL import Image

from .transformer_net import TransformerNet


def load_image(filename: str) -> Image:
    img = Image.open(filename)
    img = img.convert('RGB')
    return img


def convert_from_tensor(data: torch.Tensor) -> Image:
    img = data.clone().clamp(0, 255).numpy()
    img = img.transpose(1, 2, 0).astype("uint8")
    return Image.fromarray(img)


def load_model(style: str) -> nn.Module:

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    style_model = TransformerNet()
    state_dict = torch.load(f'styles/{style}.pth')

    for k in list(state_dict.keys()):
        if re.search(r'in\d+\.running_(mean|var)$', k):
            del state_dict[k]
    style_model.load_state_dict(state_dict)
    style_model.to(device)
    return style_model
