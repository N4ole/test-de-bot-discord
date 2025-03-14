from datetime import datetime, timezone
import dotenv
import os
import json
import asyncio
import discord
from discord.ext import commands
import logging

bot_ready = False

dotenv.load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

CONFIG_FILE = "server_config.json"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)


def load_server_config():
    """Charge le fichier JSON contenant la configuration des serveurs."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}


def save_server_config(config):
    """Sauvegarde la configuration des serveurs."""
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)


def get_server_file(guild_id, filename):
    """Crée un fichier spécifique à un serveur si nécessaire"""
    folder = f"data/{guild_id}/"
    if not os.path.exists(folder):
        os.makedirs(folder)
    return f"{folder}{filename}"


async def log_to_json(event, guild_id, username, user_id, content=None, before=None, after=None, channel=None):
    """Enregistre les logs dans des fichiers séparés pour chaque serveur"""

    config = load_server_config()
    guild_id = str(guild_id)

    setting_key = f"{event}_enabled"
    if guild_id in config and setting_key in config[guild_id] and not config[guild_id][setting_key]:
        logging.info(
            f"⚠️ Logs désactivés pour {event} sur {guild_id}, pas d'enregistrement.")
        return

    log_entry = {
        "username": username,
        "user_id": user_id,
        "channel": channel,
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    }

    if content:
        log_entry["content"] = content
    if before and after:
        log_entry["before"] = before
        log_entry["after"] = after

    file_map = {
        "message_sent": get_server_file(guild_id, "logs_sent.json"),
        "message_deleted": get_server_file(guild_id, "logs_deleted.json"),
        "message_edited": get_server_file(guild_id, "logs_edited.json")
    }

    file_path = file_map.get(event)

    if not file_path:
        logging.warning(f"⚠️ Erreur : Aucun fichier de log pour {event}")
        return

    try:
        if not os.path.exists(file_path):
            with open(file_path, "w") as f:
                json.dump([], f, indent=4)

        with open(file_path, "r") as f:
            logs = json.load(f)

        logs.append(log_entry)

        with open(file_path, "w") as f:
            json.dump(logs, f, indent=4)

        logging.info(f"✅ Log écrit : {file_path}")

        await send_log_to_channel(event, guild_id, log_entry)

    except (json.JSONDecodeError, IOError) as e:
        logging.error(f"❌ Erreur lors de l'écriture du log : {e}")


async def send_log_to_channel(event, guild_id, log_entry):
    """Envoie un log dans le salon défini dans la configuration."""
    config = load_server_config()
    guild_id = str(guild_id)

    if guild_id not in config:
        logging.warning(
            f"⚠️ Aucun salon de log défini pour `{event}` sur le serveur {guild_id}.")
        return

    channel_id = config[guild_id].get(event)

    if not channel_id:
        logging.warning(
            f"⚠️ Aucun salon trouvé pour `{event}` dans la configuration du serveur `{guild_id}`.")
        return

    channel = bot.get_channel(int(channel_id))

    if not channel:
        logging.error(
            f"❌ Impossible de trouver le salon ID: `{channel_id}` sur le serveur `{guild_id}`.")
        return

    logging.info(
        f"✅ Envoi du log `{event}` dans {channel.name} (ID: {channel_id})")

    embed = discord.Embed(
        title=f"📌 Log: {event.replace('_', ' ').title()}",
        color=discord.Color.blue()
    )
    embed.add_field(name="👤 Utilisateur",
                    value=f"{log_entry['username']} ({log_entry['user_id']})", inline=False)
    embed.add_field(name="📍 Salon", value=log_entry["channel"], inline=False)
    embed.add_field(name="🕒 Date", value=log_entry["timestamp"], inline=False)

    if event in ["message_sent", "message_deleted"]:
        embed.add_field(name="💬 Message", value=log_entry.get(
            "content", "Inconnu"), inline=False)
    elif event == "message_edited":
        embed.add_field(name="✏️ Avant", value=log_entry.get(
            "before", "Inconnu"), inline=False)
        embed.add_field(name="🔄 Après", value=log_entry.get(
            "after", "Inconnu"), inline=False)

    await channel.send(embed=embed)


@bot.event
async def on_ready():
    global bot_ready
    if bot_ready:
        return
    bot_ready = True

    logging.info(f"✅ Connecté en tant que {bot.user} (ID: {bot.user.id})")
    logging.info(f"📌 Présent dans {len(bot.guilds)} serveurs.")

    for guild in bot.guilds:
        logging.info(f"🔹 Connecté au serveur : {guild.name} (ID: {guild.id})")

    print(f"\n✅ Bot en ligne en tant que {bot.user}!\n")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await log_to_json("message_sent", message.guild.id, str(message.author), str(message.author.id), content=message.content, channel=str(message.channel))
    await bot.process_commands(message)


@bot.event
async def on_message_delete(message):
    if message.author == bot.user:
        return
    await log_to_json("message_deleted", message.guild.id, str(message.author), str(message.author.id), content=message.content, channel=str(message.channel))


@bot.event
async def on_message_edit(before, after):
    if before.author == bot.user or before.content == after.content:
        return
    await log_to_json("message_edited", before.guild.id, str(before.author), str(before.author.id), before=before.content, after=after.content, channel=str(before.channel))


async def load_cogs():
    for folder in ["commands", "events"]:
        for filename in os.listdir(f"./{folder}"):
            if filename.endswith(".py"):
                try:
                    await bot.load_extension(f"{folder}.{filename[:-3]}")
                    logging.info(f"✅ Module chargé : {folder}/{filename}")
                except Exception as e:
                    logging.error(
                        f"❌ Échec du chargement de {folder}/{filename}: {e}")


async def main():
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)


asyncio.run(main())
