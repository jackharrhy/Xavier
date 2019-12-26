import random
from datetime import datetime
from discord.ext import commands
from discord import File

from utils import get_image, save_image
from soup import NLRoadCams, NTVCams
from utils import cozy


class Cam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.nlroadcams = NLRoadCams()
        self.ntvcams = NTVCams()

    @cozy
    async def cam(self, ctx, location, lookup):
        if location is None:
            location = random.choice(list(lookup.keys()))

        if not location in lookup:
            return await ctx.send(f"Invalid location: {location}")

        image = get_image(lookup[location])
        saved_image = save_image(image)
        filename = f"{location} - {datetime.now()}.jpg"
        await ctx.send(filename, file=File(saved_image, filename=filename))

    @commands.command()
    async def ntvcam(self, ctx, location=None):
        """Sends img from an ntv.ca cam, random if no arg."""
        await self.cam(ctx, location, self.ntvcams)

    @commands.command()
    async def nlroadcam(self, ctx, location=None):
        """Sends img from an roads.gov.nl.ca camera, random if no arg."""
        await self.cam(ctx, location, self.nlroadcams)

    @commands.command()
    async def ntvcams(self, ctx):
        """Returns a list of avalible ntv.ca internet cameras"""
        list_of_cams = "\n".join(self.ntvcams.keys())
        await ctx.send(f"Available ntv.ca cameras: ```{list_of_cams}```")

    @commands.command()
    async def nlroadcams(self, ctx):
        """Returns a list of avalible roads.gov.nl.ca internet cameras"""
        list_of_cams = "\n".join(self.nlroadcams.keys())
        await ctx.send(f"Available roads.gov.nl.ca cameras: ```{list_of_cams}```")
