import io
import os
import discord
from discord import app_commands
from playwright.async_api import async_playwright
from dotenv import load_dotenv

load_dotenv()

XAVIER_TOKEN = os.getenv("XAVIER_TOKEN")
XAVIER_GUILD = int(os.getenv("XAVIER_GUILD"))

MY_GUILD = discord.Object(id=XAVIER_GUILD)


class Xavier(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)

    async def setup_hook(self):
        global tree
        tree.copy_global_to(guild=MY_GUILD)
        await tree.sync(guild=MY_GUILD)


intents = discord.Intents.default()
client = Xavier(intents=intents)
tree = app_commands.CommandTree(client)


@client.event
async def on_ready():
    print(f"Logged in as {client.user} (ID: {client.user.id})")


@tree.command()
async def hello(interaction: discord.Interaction):
    """Says hello!"""
    await interaction.response.send_message(f"Hi, {interaction.user.mention}")


@tree.command()
@app_commands.describe(
    message="Message for Mitch to Splain",
)
async def mitchsplain(interaction: discord.Interaction, message: str):
    """Displays mitchsplain for a given message"""

    url = f"http://localhost:3000/splain?message={message}"

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.set_viewport_size({"width": 0, "height": 0})
        await page.goto(url, wait_until="networkidle")
        elm = await page.query_selector(".lone-splain-container")
        screenshot_bytes = io.BytesIO(await elm.screenshot())
        screenshot_file = discord.File(screenshot_bytes, filename=f"mitchsplain.png")
        await browser.close()

    await interaction.response.send_message("", file=screenshot_file)


# This context menu command only works on messages
@tree.context_menu(name="mitchsplain")
async def mitchsplain_via_context_menu(
    interaction: discord.Interaction, message: discord.Message
):
    pass


client.run(XAVIER_TOKEN)
