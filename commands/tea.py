import random
import asyncio
from discord.ext import commands

from utils import decorators


class Mug:
    time_to_fill = 1

    class State:
        def __init__(self):
            self.exists = False
            self.cold = True
            self.sips_left = 0

    def __init__(self, guild_id=None):
        self.guild_id = guild_id
        self.methods = {
            "grab a mug": self.grab_a_mug,
            "smash mug": self.smash_mug,
            "fill up mug": self.fill_up_mug,
            "spill the mug": self.spill_the_mug,
        }
        self.state = Mug.State()

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
        if not self.guild_id in Tea.kettles:
            await message.channel.send(
                "There exists NO kettle here to even fill your mug with!!!"
            )
            return
        elif not self.state.exists:
            await message.channel.send(
                "YOU do not have mug you cannot SPILL tea into the air are you mad?"
            )
            return

        guild_kettle = Tea.kettles[self.guild_id]

        if guild_kettle.state.ready:
            if guild_kettle.state.cups_left <= 0:
                await message.channel.send("no more cups of TEA left in the kettle!!!")
                return

            guild_kettle.state.cups_left -= 1
            self.cold = guild_kettle.state.cold
            self.sips_left = 8

            if not self.cold:
                await message.channel.send(
                    f"Ah there yes nice mug FILLED, you have a _toasty_ {self.sips_left} sips of TEA left :) :) :)"
                )
            else:
                await message.channel.send(
                    f"The KETTLE was COLD when you poured this tea now you have a _chilly_ {self.sips_left} sips left.-."
                )

        else:
            pass

    async def spill_the_mug(self, message):
        await message.channel.send("stub")
        pass


class Kettle:
    time_to_boil = 1
    time_to_cold = 10
    cups_to_make = 4

    class State:
        def __init__(self):
            self.exists = False
            self.ready = False
            self.cold = True
            self.cups_left = 0

    def __init__(self):
        self.methods = {
            "put on kettle": self.put_on_kettle,
            "spill the kettle": self.spill_the_kettle,
        }
        self.state = Kettle.State()

    async def spill_the_kettle(self, message):
        self.state.exists = False
        self.state.ready = False
        self.state.cold = True
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
            self.state.cold = False
            self.state.cups_left = Kettle.cups_to_make

            await message.channel.send(
                f"kettle ready, {self.state.cups_left} cups ready to be poured!"
            )

            await asyncio.sleep(Kettle.time_to_cold)

            self.state.cold = True

            if self.state.cups_left > 0:
                await message.channel.send(
                    f"kettle has been LEFT for too long, {self.state.cups_left} COLD cups still awaiting to be poured tho"
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

        self.kettle_methods = list(Kettle().methods)
        self.mug_methods = list(Mug().methods)

        bot.add_listener(self.on_message, "on_message")

    @commands.command()
    async def tea(self, ctx):
        """Returns a list of avalible tea-related commands"""
        list_of_methods = "\n".join(self.kettle_methods + self.mug_methods)
        await ctx.send(f"Available tea-related commands: ```{list_of_methods}```")

    async def handle_kettle(self, message):
        if not message.guild.id in Tea.kettles:
            Tea.kettles[message.guild.id] = Kettle()

        kettle = Tea.kettles[message.guild.id]

        await kettle.methods[message.content](message)

    async def handle_mug(self, message):
        if not message.guild.id in Tea.mugs:
            Tea.mugs[message.guild.id] = {}

        tray = Tea.mugs[message.guild.id]

        if not message.author.id in tray:
            tray[message.author.id] = Mug(message.guild.id)

        mug = tray[message.author.id]

        await mug.methods[message.content](message)

    # TODO wrap in cozy decorator
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if message.content in self.kettle_methods:
            await self.handle_kettle(message)

        if message.content in self.mug_methods:
            await self.handle_mug(message)
