from discord.ext import commands

class Pot(commands.Cog):
    def __init__(self, bot, stackcoin_client):
        self.bot = bot
        self.stackcoin_client = stackcoin_client

    def handle_event(self, event):
        print("Got event: ", event)
