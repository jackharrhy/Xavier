import requests
import io
from wand.image import Image

from utils import soups


def get_image(url):
    """Retrieve an image object from a URL"""
    print(f"requesting url: {url}")
    resp = requests.get(url, headers=soups.headers)
    return Image(file=io.BytesIO(resp.content))


def save_image(image):
    """Save an image to a file-like object"""
    saved_image = io.BytesIO()
    image.save(file=saved_image)
    image.close()
    saved_image.seek(0)
    return saved_image
