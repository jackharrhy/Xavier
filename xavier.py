from discord.ext import commands
from dotenv import load_dotenv
from commands.cam import Cam
from commands.tea import Tea
from commands.nit import Nit
from commands.weather import Weather
import discord
import os

load_dotenv()

XAVIER_TOKEN = os.getenv("XAVIER_TOKEN")
XAVIER_PREFIX = os.getenv("XAVIER_PREFIX")
XAVIER_WEATHERSTACK_API_KEY = os.getenv("XAVIER_WEATHERSTACK_API_KEY")

bot = commands.Bot(command_prefix=XAVIER_PREFIX, description="Xavier")


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.check
async def globally_block_dms(ctx):
    return ctx.guild is not None


if __name__ == "__main__":
    # bot.add_cog(Cam(bot))
    # bot.add_cog(Nit(bot))
    # bot.add_cog(Tea(bot))
    bot.add_cog(Weather(bot, XAVIER_WEATHERSTACK_API_KEY))
    bot.run(XAVIER_TOKEN)
