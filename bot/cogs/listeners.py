# listeners to update data
import discord

from discord.ext import commands
from discord import app_commands
from bot.config import SERVER_ID
from bot.services.update_user import update_user
from bot.utils import guild_decorator

@guild_decorator
class Listeners(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # LISTENER: on_message
    # This listener triggers whenever a message is sent in the server
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if message.author.bot:
            return
    
        user_id = str(message.author.id)
        message_id = str(message.id)
        content = str(message.clean_content)
        message_time = message.created_at

        username = message.author.name
        display_name = message.author.display_name
        avatar_url = message.author.avatar.url

        update_user(user_id, message_id, content, message_time, username, display_name, avatar_url)
        


async def setup(bot):
    await bot.add_cog(Listeners(bot))