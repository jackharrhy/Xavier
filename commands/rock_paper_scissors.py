import discord
from discord.ext import commands

from utils import decorators

ROCK = "🗿"
PAPER = "🧻"
SCISSORS = "✂️"

messages = {}

class Game:
    def __init__(self, user_a, user_b, output_channel):
        self.user_a = user_a
        self.user_b = user_b
        self.output_channel = output_channel

        self.user_a_choice = None
        self.user_b_choice = None

    async def start(self):
        await self.send_user_rps_direct_message(self.user_a, self.user_b)
        await self.send_user_rps_direct_message(self.user_b, self.user_a)

        await message.channel.send(
            f"New game #{id(self)} created, check your direct messages!"
        )

    async def send_user_rps_direct_message(self, user, other_user):
        message = await user.send(
            f"You VS {other_user.name}: Rock, paper, scissors? (game #{id(self)})"
        )
        await message.add_reaction(ROCK)
        await message.add_reaction(PAPER)
        await message.add_reaction(SCISSORS)

        messages[message.id] = (self, user)

    async def handle_reaction(self, message, user, reaction):
        if reaction.emoji == "🗿":
            choice = ROCK
        elif reaction.emoji == "🧻":
            choice = PAPER
        elif reaction.emoji == "✂️":
            choice = SCISSORS

        if user == self.user_a:
            self.user_a_choice = choice
        else:
            self.user_b_choice = choice

        if choice is not None:
            del messages[message.id]

        await self.check_if_game_is_done()

    async def check_if_game_is_done(self):
        if self.user_a_choice is not None and self.user_b_choice is not None:
            await self.end_game()

    async def end_game(self):
        winner = None

        if self.user_a_choice == ROCK:
            if self.user_b_choice == PAPER:
                winner = self.user_b
            elif self.user_b_choice == SCISSORS:
                winner = self.user_a

        elif self.user_a_choice == PAPER:
            if self.user_b_choice == SCISSORS:
                winner = self.user_b
            elif self.user_b_choice == ROCK:
                winner = self.user_a

        elif self.user_a_choice == SCISSORS:
            if self.user_b_choice == ROCK:
                winner = self.user_b
            elif self.user_b_choice == PAPER:
                winner = self.user_a

        if winner:
            postfix = f"{winner} wins!"
        else:
            postfix = "tie!"

        await self.output_channel.send(
            f"Game #{id(self)} results: {self.user_a.name} {self.user_a_choice} VS {self.user_b.name} {self.user_b_choice}, {postfix}"
        )


async def handle_user_game(message):
    new_game = Game(message.author, message.mentions[0], message.channel)
    await new_game.start()
    await message.channel.send(
        f"New game #{id(new_game)} created, check your direct messages!"
    )


class RockPaperScissors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.add_listener(self.on_reaction_add, "on_reaction_add")

    async def on_reaction_add(self, reaction, user):
        if user == self.bot.user:
            return

        if reaction.message.id in messages:
            game, user = messages[reaction.message.id]
            await game.handle_reaction(reaction.message, user, reaction)

    @decorators.cozy
    async def initialize_game(self, ctx, user):
        await Game(ctx.message.author, user, ctx.message.channel).start()

    @commands.command()
    async def rps(self, ctx, user: discord.Member):
        await self.initialize_game(ctx, user)
