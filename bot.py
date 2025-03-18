from datetime import datetime
import dotenv
import os
import json
import asyncio
import shutil
import discord
from discord.ext import commands
import logging


from logs.logging_utils import log_to_json, send_log_to_channel


bot_ready = False

dotenv.load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
print(f"===============================================")
print(f"TOKEN récupéré: {TOKEN}")


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


CONFIG_FILE = "server_config.json"
WATCHLIST_FILE = "data/watchlist.json"
MODLOGS_FILE = "data/modlogs.json"
WARNINGS_FILE = "data/warnings.json"


intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)


async def update_bot_status():
    """Met à jour le statut du bot avec le nombre de serveurs actuels."""
    total_guilds = len(bot.guilds)
    activity = discord.Game(name=f"Présent sur {total_guilds} serveurs")
    await bot.change_presence(activity=activity)


@bot.event
async def on_guild_join(guild):
    """Met à jour le statut et affiche un message en console quand le bot rejoint un serveur."""
    owner = await bot.fetch_user(guild.owner_id)
    logging.info(
        f"✅ Rejoint un nouveau serveur : {guild.name} (ID: {guild.id})")
    logging.info(f"👑 Propriétaire: {owner} (ID: {guild.owner_id})")
    await update_bot_status()


@bot.event
async def on_guild_remove(guild):
    """Met à jour le statut du bot et supprime les données lorsqu'il quitte un serveur."""
    logging.info(f"❌ Supprimé du serveur : {guild.name} (ID: {guild.id})")
    delete_server_data(guild.id)
    await update_bot_status()


# ✅ Événement `on_ready`
@bot.event
async def on_ready():
    global bot_ready
    if bot_ready:
        return
    bot_ready = True

    print(f"\n{'='*60}")
    logging.info(f"✅ Connecté en tant que {bot.user} (ID: {bot.user.id})")
    logging.info(f"📌 Présent dans {len(bot.guilds)} serveurs.")
    print(f"{'='*60}\n")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await log_to_json(bot, "message_sent", message.guild.id, str(message.author), str(message.author.id), content=message.content, channel=str(message.channel))
    await bot.process_commands(message)


async def on_message_delete(message):
    if message.author == bot.user:
        return
    await log_to_json(bot, "message_deleted", message.guild.id, str(message.author), str(message.author.id), content=message.content, channel=str(message.channel))


@bot.event
async def on_message_edit(before, after):
    if before.author == bot.user or before.content == after.content:
        return
    await log_to_json(bot, "message_edited", before.guild.id, str(before.author), str(before.author.id), before=before.content, after=after.content, channel=str(before.channel))


async def load_cogs():
    """Charge tous les fichiers de commandes et d'événements."""
    logging.info("🔄 Chargement des modules en cours...")
    for folder in ["commands", "events", "logs"]:
        for filename in os.listdir(f"./{folder}"):
            if filename.endswith(".py") and filename != "logging_utils.py":
                try:
                    await bot.load_extension(f"{folder}.{filename[:-3]}")
                    logging.info(f"✅ Module chargé : {folder}/{filename}")
                except Exception as e:
                    logging.error(
                        f"❌ Échec du chargement de {folder}/{filename}: {e}")
print(f"===============================================")


async def main():
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)


asyncio.run(main())
