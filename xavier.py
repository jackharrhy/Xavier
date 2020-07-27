import os
import asyncio

from dotenv import load_dotenv
import discord
from discord.ext import commands

from commands.cam import Cam
from commands.tea import Tea
from commands.nit import Nit
from commands.pot import Pot

load_dotenv()

XAVIER_TOKEN = os.getenv("XAVIER_TOKEN")
XAVIER_PREFIX = os.getenv("XAVIER_PREFIX")

bot = commands.Bot(command_prefix=XAVIER_PREFIX, description="Xavier")

# some hacks to work around pulling in stackcoin a directory above
import sys
import os.path

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
)
# you don't need this in your code :)

from stackcoin import StackCoin
from stackcoin.types import TransferSuccess

stackcoin_client = StackCoin(
    base_http_url="http://localhost:3000",
    base_ws_url="ws://localhost:3000/ws",
    token="abc",
    user_id=123,
)


@stackcoin_client.notification()
def return_to_sender(event):
    """
    Once sent STK, returns to sender
    """
    if isinstance(event, TransferSuccess):
        stackcoin_client.transfer(event.from_id, event.amount)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.check
async def globally_block_dms(ctx):
    return ctx.guild is not None


async def main():
    await asyncio.gather(stackcoin_client.connect())


if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    bot.add_cog(Cam(bot))
    bot.add_cog(Nit(bot))
    # bot.add_cog(Tea(bot))
    bot.add_cog(Pot(bot, stackcoin_client))

    try:
        loop.create_task(bot.start(XAVIER_TOKEN))
        loop.create_task(stackcoin_client.start())
        loop.run_forever()
    finally:
        loop.stop()
