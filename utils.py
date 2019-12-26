import requests
import io
from functools import wraps
from wand.image import Image

from soup import headers


def cozy(f):
    """Wraps a discord command in a typing context, and spits out errors on them occuring"""

    @wraps(f)
    async def inner(self, ctx, *args, **kwargs):
        async with ctx.channel.typing():
            try:
                return await f(self, ctx, *args, **kwargs)
            except Exception as e:
                await ctx.send(f"Something is borked!:```{e}```")
                raise e

    return inner


def get_image(url):
    """Retrieve an image object from a URL"""
    print(f"requesting url: {url}")
    resp = requests.get(url, headers=headers)
    return Image(file=io.BytesIO(resp.content))


def save_image(image):
    """Save an image to a file-like object"""
    saved_image = io.BytesIO()
    image.save(file=saved_image)
    image.close()
    saved_image.seek(0)
    return saved_image
