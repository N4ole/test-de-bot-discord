import json
import os
import discord

CONFIG_PATH = os.path.join(os.path.dirname(
    __file__), "../data/log_config.json")


def load_log_config():
    if not os.path.exists(CONFIG_PATH):
        return {}
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)


def save_log_config(config):
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)


async def send_log(bot, guild_id, message: str):
    config = load_log_config()
    if str(guild_id) in config:
        channel_id = int(config[str(guild_id)])
        channel = bot.get_channel(channel_id)
        if channel:
            await channel.send(message)
