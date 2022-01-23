import cv2
import numpy as np
from PIL import Image, ImageChops, ImageFilter


def normalize(img: Image.Image) -> Image.Image:
    if img.height > 100:
        img.thumbnail((img.width, 100))
    return img


def crop_image(img: Image.Image) -> Image.Image:
    """Remove margin

    Args:
        img (Image): Input image

    Returns:
        Image: Crop image
    """
    # Create background image
    bg = Image.new("RGB", img.size, img.getpixel((0, 0)))

    # Create a difference image between the background color image and the original image
    diff = ImageChops.difference(img, bg)

    # Crop the image for the border with the background color
    croprange = diff.convert("RGB").getbbox()
    return img.crop(croprange)


def get_edge(img: Image.Image, blur_radius: float = 0.5) -> Image.Image:
    """Extract edges

    Args:
        img (Image.Image): Input image
        blur_radius (float, optional): Gaussian blur filter radius. Defaults to 0.5.

    Returns:
        Image.Image: Edges
    """
    img_gray = img.convert("L")
    img_blur = img_gray.filter(ImageFilter.GaussianBlur(blur_radius))
    med_val = float(np.median(img_blur))
    sigma = 0.33
    min_val = int(max(0, (1.0 - sigma) * med_val))
    max_val = int(max(255, (1.0 + sigma) * med_val))

    return Image.fromarray(cv2.Canny(np.asarray(img_blur), min_val, max_val))


def img_process(img: Image.Image) -> Image.Image:
    """Edit the image

    Args:
        img (Image.Image): Input image

    Returns:
        Image.Image: Processed image
    """
    return normalize(get_edge(crop_image(img), 1))


if __name__ == "__main__":
    img_process(Image.open("image/map.png")).save("dist/edge.png")
