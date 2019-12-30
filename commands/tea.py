import random
import asyncio
from discord.ext import commands

from utils import decorators


class KettleState:
    def __init__(self):
        self.exists = False
        self.ready = False
        self.cups_left = 0


class Tea(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.add_listener(self.on_message, "on_message")

        self.methods = {
            "put on kettle": self.put_on_kettle,
            "spill the kettle": self.spill_the_kettle,
        }

        self.state = KettleState()

    async def spill_the_kettle(self, message):
        self.state.exists = False
        self.state.ready = False
        self.state.cups_left = 0
        await message.channel.send(
            f"kettle has been spilt on the floor, no more cup and no longer exist"
        )

    async def put_on_kettle(self, message):
        if not self.state.exists:
            self.state.exists = True
            self.state.ready = False
            await message.channel.send("putting on the kettle")

            await asyncio.sleep(1)

            self.state.ready = True
            self.state.cups_left = 4

            await message.channel.send(
                f"kettle ready, {self.state.cups_left} cups ready to be poured!"
            )
        else:
            await message.channel.send(
                "kettle is already exist, cannot make more than one kettle only one kettle .-."
            )

    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if message.content in self.methods:
            await self.methods[message.content](message)
