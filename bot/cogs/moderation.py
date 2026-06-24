from discord.ext import commands
from discord import app_commands
from bot.ml.classifier import classify_message

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        results = classify_message(message.content)
        output = "\n".join([f"{label}: {prob:.4f}" for label, prob in results.items()])
        await message.channel.send(f"Classification results:\n{output}")



async def setup(bot):
    await bot.add_cog(Moderation(bot))