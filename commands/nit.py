from discord.ext import commands

class Nit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.add_listener(self.on_message, "on_message")

    async def on_message(self, message):
        if message.content == "nit":
            await message.channel.send(":nit:")
