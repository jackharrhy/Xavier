from discord.ext import commands
from apixu.client import ApixuClient
import requests

class WeatherStack:
    API_BASE = "http://api.weatherstack.com"

    def __init__(self, api_key):
        self.api_key = api_key

    def location_info(self, location):
        params = {
            'access_key': self.api_key,
            'query': location,
        }
        api_result = requests.get(f"{WeatherStack.API_BASE}/current", params)

        return api_result.json()

class Weather(commands.Cog):
    def __init__(self, bot, api_key):
        self.bot = bot
        self.weatherstack = WeatherStack(api_key)

        print(self.weatherstack.location_info("Saint John's, Newfoundland and Labrador, Canada"))

        exit(0)

        #bot.add_listener(self.on_message, "on_message")

    async def on_message(self, message):
        if message.content == "weather":
            await message.channel.send("weather")
