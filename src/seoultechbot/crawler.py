from discord.ext import tasks, commands

class Food(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot