# functions for general user utilities, such as help commands, user info, etc.
import discord
from discord.ext import commands
from discord import app_commands

from bot.config import SERVER_ID

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.guilds(discord.Object(id=SERVER_ID))  # remove when you want to make the command global
    @app_commands.command(
        name = "help",
        description = "Lists all bot commands"
    )
    async def help(self, interaction):
        await interaction.response.send_message(f"Here are the available commands:", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Help(bot))