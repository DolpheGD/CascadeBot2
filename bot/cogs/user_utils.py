# functions for general user utilities, such as help commands, user info, etc.
import discord

from discord.ext import commands
from discord import app_commands
from bot.services.get_users import get_ten_higher_danger
from bot.utils.guild_decorator import guild_decorator
from bot.utils.embedder import get_danger_color, leaderboard_danger_output

from bot.config import SERVER_ID


@guild_decorator
class UserUtils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # COMMAND: /help
    # This command lists all available bot commands to the user.
    @app_commands.command(
        name = "help",
        description = "Lists all bot commands"
    )
    async def help(self, ctx: discord.Interaction):
        output = "Here are the available commands:\n" \
        "`/classify text <text>` - Classifies the provided text.\n" \
        "`/classify id <message_id>` - Classifies the message with the given ID.\n" \
        "`/classify user <user> <verbose [Optional]>` - Classifies the user with a danger rating and dangerous messages.\n" \
        "`/rankings` - Displays the top 10 most dangerous users.\n" \
        "`/clear <user> [ADMIN]` - Clears user's history.\n" \
        "`/help` - Displays this help message."
        
        await ctx.response.send_message(output, ephemeral=True)


    # COMMAND: /leaderboard
    # FIX THIS LATER (MOVE)
    @app_commands.command(
        name = "leaderboard",
        description = "Lists the rankings of the most dangerous users"
    )
    async def leaderboard(self, ctx):
        users = get_ten_higher_danger()

        if not users:
            await ctx.response.send_message(
                "No users found."
            )
            return

        color = get_danger_color(users[0].danger_score)
        embed = discord.Embed(
            title="🏆 Danger Leaderboard 🏆",
            color=color
        )

        if users[0].avatar_url:
            embed.set_thumbnail(url=users[0].avatar_url)


        for i, user in enumerate(users, start=1):
            if user.display_name:
                name = user.display_name
            else:
                try:
                    member = await ctx.guild.fetch_member(
                        int(user.discord_id)
                    )
                    name = member.display_name
                except discord.NotFound:
                    name = "Unknown User"


            embed.add_field(
                name=f"{i}. {name} ({user.danger_score:.2%})\n",
                value="",
                inline=False
            )
        

        await ctx.response.send_message(embed=embed)



async def setup(bot):
    await bot.add_cog(UserUtils(bot))