import discord
from bot.ml.classifier import classify_danger_level

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


def get_danger_color(danger):
    if danger > 1.0:
        color = 0 #black
    elif danger > 0.9:
        color = discord.Color.dark_red()
    elif danger > 0.8:
        color = discord.Color.red()
    elif danger > 0.65:
        color = discord.Color.orange()
    elif danger > 0.5:
        color = discord.Color.yellow()
    else:
        color = discord.Color.green()

    return color
    
