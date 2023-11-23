import os

from . import PMRID
import torch
from PIL import Image
from torchvision import transforms


def generate_processed_picture(entry_path: str, output_path: str):
    model = PMRID()
    model = model.to('cpu')
    checkpoint = torch.load(os.getcwd()+'/util/PMRIDmodel.pth', map_location=torch.device('cpu'))
    model.eval()

    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Resize((800, 800)),
        transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
    ])
    image = Image.open(entry_path)
    image = transform(image).unsqueeze(0)
    image_fake = model(image)

    image = image * 0.5 + 0.5
    toPIL = transforms.ToPILImage()  # 这个函数可以将张量转为PIL图片，由小数转为0-255之间的像素值
    pic = toPIL((image.squeeze(0)))
    pic.save(output_path)