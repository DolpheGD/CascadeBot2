import discord
from bot.ml.classifier import classify_danger_level
from bot.services.get_users import get_top_ten_and_avg, get_ten_higher_danger

def classify_with_output(message):
    """
    classify_danger_level output, using discord embeds
    """
    results = classify_danger_level(message)

    desc = ""
    for category, score in results.items():
        desc += f'{category}: {score:.2%}\n'

    color = get_danger_color(results["Danger"])

    embed = discord.Embed(
       title="**Results**",
       description=desc,
       color=color
    )

    return embed



def classify_user_with_output(user: discord.Member, verbose = False):
    top_ten, avg_danger = get_top_ten_and_avg(user.id)
    color = get_danger_color(avg_danger)
    is_no_data = False
    
    if len(top_ten) <= 0:
        desc = "*[No Data]*"
        is_no_data = True
    else:
        desc = f"Danger Score: {avg_danger:.2%}"

    
    embed = discord.Embed(
       title=f"**⚠️ {user.display_name}'s Danger ⚠️**",
       color=color,
       description=desc
    )
    
    if user.avatar:
        embed.set_thumbnail(url=user.avatar.url)
    
    if is_no_data:
        return embed
    

    for num, message in enumerate(top_ten, start=1):
        name_text = f'{num}. '
        if len(message.content) >= 50:
            name_text += f'{message.content[:50]} ...'
            if verbose:
                name_text += f' ({len(message.content) - 50} more)'
        else:
            name_text += message.content

        value_text = ""
        if verbose:
            value_text += f'(Danger: {message.danger_score:.2%}) (Hate: {message.hate_score:.2%}) (Sexual: {message.sexual_score:.2%}) (Sexual: {message.concern_score:.2%}) (ID: {message.message_id})\n'

        embed.add_field(name=name_text, value=value_text, inline=False)

    return embed


def leaderboard_danger_output(users):

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
            name = 'Unkonwn User'

        embed.add_field(
            name=f"{i}. {name} ({user.danger_score:.2%})\n",
            value="",
            inline=False
        )


    return embed






def get_danger_color(danger):
    if danger > 1.2:
        color = discord.Color.dark_purple()
    elif danger > 1.0:
        color = 0 #black
    elif danger > 0.85:
        color = discord.Color.dark_red()
    elif danger > 0.7:
        color = discord.Color.red()
    elif danger > 0.55:
        color = discord.Color.orange()
    elif danger > 0.40:
        color = discord.Color.yellow()
    elif danger > 0.20:
        color = discord.Color.green()
    else:
        color = discord.Color.blue()
    return color
    