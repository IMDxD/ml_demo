import os

import cv2
import skvideo.io
import torch
import numpy as np
from torch import nn
from torchvision import transforms
from PIL import Image

from style_models import load_image, convert_from_tensor, load_model


image_dir = 'images'
videos_dir = 'videos'
cache_dir = 'temp'
alpha = 0.95

to_tensor = transforms.Compose([
    transforms.ToTensor(),
    transforms.Lambda(lambda x: x.mul(255))
])


def stylize(content_image: Image, style_model: nn.Module) -> Image:

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    content_image = to_tensor(content_image)
    content_image = content_image.unsqueeze(0).to(device)

    with torch.no_grad():
        output = style_model(content_image).cpu()

    img = convert_from_tensor(output.squeeze(0))
    return img


def stylize_video(filename: str, style: str) -> bool:

    style_model = load_model(style)
    path_to_video = f'{videos_dir}/{filename}'

    cap = skvideo.io.FFmpegReader(path_to_video)
    fps = int(cap.inputfps)
    height = int(cap.inputheight)
    width = int(cap.inputwidth)

    writer = cv2.VideoWriter(f"{cache_dir}/{filename}", cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height))

    last_image = None
    for i, frame in enumerate(cap.nextFrame()):

        frame = Image.fromarray(frame)

        if last_image is None:
            img = frame

        else:
            img = Image.blend(last_image, frame, alpha)

        img = stylize(img, style_model)
        last_image = img
        writer.write(np.array(last_image)[:, :, ::-1])  # OpenCV BGR Format <3

    writer.release()

    os.system(f"ffmpeg -i {cache_dir}/{filename} -vcodec libx264 {path_to_video} -y")
    os.remove(f"{cache_dir}/{filename}")
    return True


def stylize_image(filename: str, style: str) -> bool:

    path_to_photo = f'{image_dir}/{filename}'

    content_image = load_image(path_to_photo)
    style_model = load_model(style)

    img = stylize(content_image, style_model)
    img.save(path_to_photo)

    return True
