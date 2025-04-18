import json
import os
import discord

CONFIG_PATH = os.path.join(os.path.dirname(
    __file__), "../data/log_config.json")
os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)


def load_log_config():
    if not os.path.exists(CONFIG_PATH):
        return {}
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)


def save_log_config(config):
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)


async def send_log(bot, guild_id, title: str, description: str, color=discord.Color.orange()):
    config = load_log_config()
    if str(guild_id) in config:
        channel_id = int(config[str(guild_id)])
        channel = bot.get_channel(channel_id)
        if channel:
            embed = discord.Embed(
                title=title, description=description, color=color)
            embed.set_footer(text="Log de modération")
            await channel.send(embed=embed)
