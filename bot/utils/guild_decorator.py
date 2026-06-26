from bot.config import DEV_MODE, SERVER_ID
import discord
from discord import app_commands

guild_decorator = (
    app_commands.guilds(discord.Object(id=SERVER_ID))
    if DEV_MODE
    else (lambda x: x)
)