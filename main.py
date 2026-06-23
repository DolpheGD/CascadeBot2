import os
from dotenv import load_dotenv, dotenv_values
import discord
from discord.ext import commands

bot: commands.Bot = commands.Bot(command_prefix='.', intents=discord.Intents.all())
load_dotenv()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

bot.run(os.getenv('BOT_KEY'))