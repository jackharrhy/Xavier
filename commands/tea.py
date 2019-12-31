import random
import asyncio
from discord.ext import commands

from utils import decorators


class MugState:
    def __init__(self):
        self.exists = False
        self.cold = True
        self.sips_left = 0


class Mug:
    time_to_fill = 1

    def __init__(self):
        self.methods = {
            "grab a mug": self.grab_a_mug,
            "smash mug": self.smash_mug,
            "fill up mug": self.fill_up_mug,
            "spill the mug": self.spill_the_mug,
        }
        self.state = MugState()

    async def smash_mug(self, message):
        if self.state.exists:
            self.state.exists = False
            self.cold = True
            self.sips_left = 0
            await message.channel.send(
                "and just like that you disrepect my family and my mug i hope you are happy it no longer exist"
            )
        else:
            await message.channel.send(
                "YOU cannot smash MUG that do NOT exist that is breaking the universe law"
            )

    async def grab_a_mug(self, message):
        if not self.state.exists:
            self.state.exists = True
            await message.channel.send(
                "here is a mug with your name on it your name is not actually on it but here is enjoy"
            )
        else:
            await message.channel.send(
                "mug is already exist, you have ALREADY grab no MORE grab no more grab"
            )

    async def fill_up_mug(self, message):
        pass

    async def spill_the_mug(self, message):
        pass


class KettleState:
    def __init__(self):
        self.exists = False
        self.ready = False
        self.cups_left = 0


class Kettle:
    time_to_boil = 1
    cups_to_make = 4

    def __init__(self):
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

            await asyncio.sleep(Kettle.time_to_boil)

            self.state.ready = True
            self.state.cups_left = Kettle.cups_to_make

            await message.channel.send(
                f"kettle ready, {self.state.cups_left} cups ready to be poured!"
            )
        else:
            await message.channel.send(
                "kettle is already exist, cannot make more than one kettle only one kettle .-."
            )


class Tea(commands.Cog):
    kettles = {}
    mugs = {}

    def __init__(self, bot):
        self.bot = bot
        bot.add_listener(self.on_message, "on_message")

    async def on_message(self, message):
        # TODO wrap in cozy decorator
        if message.author == self.bot.user:
            return

        if not message.guild.id in Tea.kettles:
            Tea.kettles[message.guild.id] = Kettle()

        kettle = Tea.kettles[message.guild.id]

        if message.content in kettle.methods:
            await kettle.methods[message.content](message)

        if not message.author.id in Tea.mugs:
            Tea.kettles[message.author.id] = Mug()

        mug = Tea.mugs[message.author.id]

        if message.content in mug.methods:
            await mug.methods[message.content](message)
