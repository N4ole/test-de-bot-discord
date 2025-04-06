from collections import defaultdict
import time
import re
import discord
from discord.ext import commands
import os
import importlib

# Init bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)


# Dynamically load all command modules from /commands


def load_commands():
    commands_dir = os.path.join(os.path.dirname(__file__), "commands")
    for filename in os.listdir(commands_dir):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = f"commands.{filename[:-3]}"
            module = importlib.import_module(module_name)
            if hasattr(module, "setup"):
                module.setup(bot)


def run_bot():
    load_commands()
    return bot


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("⚠️ Il manque un argument dans ta commande.")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("❓ Commande inconnue. Tape `!help` pour voir les commandes.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("❌ Argument invalide ou mal écrit.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("🚫 Tu n’as pas la permission pour cette commande.")
    else:
        await ctx.send("❌ Une erreur est survenue.")
        raise error  # Pour le debug en console
