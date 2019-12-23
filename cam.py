import random
import requests
import io
from datetime import datetime
from discord import File
from discord.ext import commands
from wand.image import Image

def get_image(url):
    """Retrieve an image object from a URL"""
    resp = requests.get(url)
    return Image(file=io.BytesIO(resp.content))

def save_image(image):
    """Save an image to a file-like object."""
    saved_image = io.BytesIO()
    image.save(file=saved_image)
    image.close()
    saved_image.seek(0)
    return saved_image

cams = {
    "georgestreet": "https://www221.mangocam.com/c/georgestreet/img.php"
}

class Cam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def cam(self, ctx, location=None):
        """Returns an image from a internet camera, random if no argument given"""
        if location is None:
            location = random.choice(list(cams.keys()))

        if not location in cams:
            await ctx.send(f"Invalid location: {location}")
            return

        image = get_image(cams[location])
        saved_image = save_image(image)
        filename = f"{location} - {datetime.now()}.jpg"
        await ctx.send(file=File(saved_image, filename=filename))
