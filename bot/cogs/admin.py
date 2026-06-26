# functions for general user utilities, such as help commands, user info, etc.
import discord

from discord.ext import commands
from discord import app_commands

from bot.config import SERVER_ID
from bot.database.models.user_model import UserProfile
from bot.database.session import SessionLocal

class AdminUtils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    # TODO: MOVE THIS LOGIC LATER


    # COMMAND: /clear
    # This command clears database history from a user
    @app_commands.guilds(discord.Object(id=SERVER_ID))  # remove when you want to make the command global
    @app_commands.command(
        name = "clear",
        description = "Clears database history from a user"
    )
    @app_commands.describe(
        user="The user whose history will be cleared"
    )
    @app_commands.default_permissions(administrator=True)
    async def clear(self, ctx: discord.Interaction, user: discord.Member):
        db = SessionLocal()

        try:
            profile = db.query(UserProfile).filter_by(
                discord_id=str(user.id)
            ).first()

            if not profile:
                await ctx.response.send_message(
                    "User has no danger history.",
                    ephemeral=True
                )
                return

            db.delete(profile)
            db.commit()

            await ctx.response.send_message(
                f"Cleared danger history for {user.display_name}."
            )

        finally:
            db.close()
        

async def setup(bot):
    await bot.add_cog(AdminUtils(bot))