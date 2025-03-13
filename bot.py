import dotenv
import os
from datetime import datetime
import json
import asyncio
import discord
from discord.ext import commands
import logging


dotenv.load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")


logging.basicConfig(level=logging.INFO)


LOGS_SENT_CHANNEL_ID = int(os.getenv("LOGS_SENT_CHANNEL_ID", 0))
LOGS_DELETED_CHANNEL_ID = int(os.getenv("LOGS_DELETED_CHANNEL_ID", 0))
LOGS_EDITED_CHANNEL_ID = int(os.getenv("LOGS_EDITED_CHANNEL_ID", 0))

print(f"==================================================")
print(f"LOGS_SENT_CHANNEL_ID: {LOGS_SENT_CHANNEL_ID}")
print(f"LOGS_DELETED_CHANNEL_ID: {LOGS_DELETED_CHANNEL_ID}")
print(f"LOGS_EDITED_CHANNEL_ID: {LOGS_EDITED_CHANNEL_ID}")
print(f"==================================================")


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


async def send_log_to_channel(event, log_entry):
    """Envoie un log dans le salon Discord correspondant"""

    log_channels = {
        "message_sent": LOGS_SENT_CHANNEL_ID,
        "message_deleted": LOGS_DELETED_CHANNEL_ID,
        "message_edited": LOGS_EDITED_CHANNEL_ID
    }

    channel_id = log_channels.get(event)
    if not channel_id or channel_id == 0:
        print(f"⚠️ Aucun salon log défini pour {event}.")
        return

    channel = bot.get_channel(channel_id)
    if not channel:
        print(
            f"❌ Impossible de trouver le salon ID: {channel_id}. Vérifiez l'ID et les permissions.")
        return

    embed = discord.Embed(
        title=f"📌 Log: {event.replace('_', ' ').title()}", color=discord.Color.blue())
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


async def log_to_json(event, username, user_id, content=None, before=None, after=None, channel=None):
    log_entry = {
        "username": username,
        "user_id": user_id,
        "channel": channel,
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    }

    if content:
        log_entry["content"] = content
    if before and after:
        log_entry["before"] = before
        log_entry["after"] = after

    file_map = {
        "message_sent": "logs_sent.json",
        "message_deleted": "logs_deleted.json",
        "message_edited": "logs_edited.json"
    }

    file_path = file_map.get(event)
    if not file_path:
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

        await send_log_to_channel(event, log_entry)

    except (json.JSONDecodeError, IOError) as e:
        logging.error(f"❌ Erreur lors de l'écriture du log : {e}")


@bot.event
async def on_ready():
    print(f"==================================================")
    logging.info(f"✅ Connecté en tant que {bot.user} (ID: {bot.user.id})")
    logging.info(f"📌 Présent dans {len(bot.guilds)} serveurs.")
    print(f"\n✅ Bot en ligne en tant que {bot.user}!\n")

    sent_channel = bot.get_channel(LOGS_SENT_CHANNEL_ID)
    deleted_channel = bot.get_channel(LOGS_DELETED_CHANNEL_ID)
    edited_channel = bot.get_channel(LOGS_EDITED_CHANNEL_ID)

    print(f"📩 Salon Logs Envoyés: {sent_channel}")
    print(f"🗑️ Salon Logs Supprimés: {deleted_channel}")
    print(f"✏️ Salon Logs Modifiés: {edited_channel}")
    print(f"==================================================")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await log_to_json("message_sent", str(message.author), str(message.author.id), content=message.content, channel=str(message.channel))
    await bot.process_commands(message)


@bot.event
async def on_message_delete(message):
    if message.author == bot.user:
        return

    await log_to_json("message_deleted", str(message.author), str(message.author.id), content=message.content, channel=str(message.channel))


@bot.event
async def on_message_edit(before, after):
    if before.author == bot.user or before.content == after.content:
        return

    await log_to_json("message_edited", str(before.author), str(before.author.id), before=before.content, after=after.content, channel=str(before.channel))


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
