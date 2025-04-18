from utils.config import get_debug_mode
from collections import defaultdict
import time
import re
import discord
from discord.ext import commands
import os
import importlib
from utils.logger import send_log
from datetime import datetime, timedelta
from utils.time import get_french_datetime
import json
from utils.security import is_owner, add_owner
from utils.logger import send_log
from admin import reload, addowner
import json


CONFIG_PATH = os.path.join(os.path.dirname(__file__), "data", "config.json")
with open(CONFIG_PATH) as f:
    config = json.load(f)


BOT_VERSION = config.get("version", "0.0.0")
DEBUG_MODE = get_debug_mode()


startup_time = get_french_datetime()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)


def load_commands():
    for folder in ["commands", "admin"]:
        commands_dir = os.path.join(os.path.dirname(__file__), folder)
        for filename in os.listdir(commands_dir):
            if filename.endswith(".py") and filename != "__init__.py":
                module_name = f"{folder}.{filename[:-3]}"
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
        raise error


@bot.event
async def on_message_edit(before, after):
    if before.author.bot:
        return

    if before.content == after.content:
        return

    utc_now = datetime.utcnow()
    timestamp = (utc_now + timedelta(hours=2)).strftime("%d/%m/%Y %H:%M:%S")

    description = (
        f"**Auteur :** {before.author.mention}\n"
        f"**Salon :** {before.channel.mention}\n"
        f"**Avant :** {before.content}\n"
        f"**Après :** {after.content}\n"
        f"**Modifié le :** `{timestamp} (heure FR)`"
    )

    await send_log(
        bot,
        before.guild.id,
        title="✏️ Message modifié",
        description=description,
        color=discord.Color.blue()
    )


@bot.event
async def on_message_delete(message):
    if message.author.bot:
        return

    if not message.guild:
        return  # ignore DM

    utc_now = datetime.utcnow()
    timestamp = (utc_now + timedelta(hours=2)).strftime("%d/%m/%Y %H:%M:%S")

    description = (
        f"**Auteur :** {message.author.mention}\n"
        f"**Salon :** {message.channel.mention}\n"
        f"**Contenu supprimé :**\n```{message.content}```\n"
        f"**Supprimé le :** `{timestamp} (heure FR)`"
    )

    await send_log(
        bot,
        message.guild.id,
        title="🗑️ Message supprimé",
        description=description,
        color=discord.Color.red()
    )


@bot.event
async def on_ready():
    # Bonjour dans la console
    print(f"\n[✅] Bot en ligne en tant que {bot.user} !")
    launch_time = datetime.utcnow() + timedelta(hours=2)
    formatted_time = launch_time.strftime("%d/%m/%Y à %H:%M:%S")
    print(
        f"[👋] salut, {bot.user.name} est lancé depuis cette date : {formatted_time}  😎")

    print("\n[⚙️] Intents activés :")
    for name in dir(bot.intents):
        if name.startswith('_'):
            continue
        value = getattr(bot.intents, name)
        if isinstance(value, bool):
            status = "✅" if value else "❌"
            print(f" - {name:<18}: {status}")

    # Liste des commandes chargées
    print("\n[📦] Commandes chargées :")
    for command in bot.commands:
        print(f" - {command.name}")
    if DEBUG_MODE:
        print("[🐞 DEBUG] Mode debug activé")
    else:
        print("[✅] Mode debug désactivé")

    print("\n[🚀] Initialisation terminée.")
