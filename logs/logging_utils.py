import os
import json
import logging
from datetime import datetime
import discord

CONFIG_FILE = "server_config.json"


def load_server_config():
    """Charge la configuration des serveurs."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}


def save_server_config(config):
    """Sauvegarde la configuration des serveurs."""
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)


def get_server_file(guild_id, filename):
    """Retourne le chemin d'un fichier spécifique à un serveur"""
    folder = f"data/{guild_id}/"
    os.makedirs(folder, exist_ok=True)
    return f"{folder}{filename}"


async def log_to_json(bot, event, guild_id, username, user_id, content=None, before=None, after=None, channel=None):
    """Enregistre les logs dans des fichiers JSON et les envoie dans le salon approprié."""

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
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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
        logging.warning(f"⚠️ Aucun fichier de log défini pour {event}")
        return

    try:
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                logs = json.load(f)
                if not isinstance(logs, list):
                    logs = []
        else:
            logs = []

        logs.append(log_entry)

        with open(file_path, "w") as f:
            json.dump(logs, f, indent=4)

        logging.info(f"✅ Log écrit : {file_path}")

        await send_log_to_channel(bot, event, guild_id, log_entry)

    except (json.JSONDecodeError, IOError) as e:
        logging.error(f"❌ Erreur lors de l'écriture du log : {e}")


async def send_log_to_channel(bot, event, guild_id, log_entry):
    """Envoie un log dans le salon défini dans la configuration."""

    config = load_server_config()
    guild_id = str(guild_id)

    if guild_id not in config or event not in config[guild_id]:
        return

    channel_id = config[guild_id].get(event)

    if channel_id:
        channel = bot.get_channel(int(channel_id))
        if channel:
            embed = discord.Embed(
                title=f"📌 Log: {event.replace('_', ' ').title()}",
                color=discord.Color.blue()
            )
            embed.add_field(name="👤 Utilisateur",
                            value=f"{log_entry['username']} ({log_entry['user_id']})", inline=False)
            embed.add_field(
                name="📍 Salon", value=log_entry["channel"], inline=False)
            embed.add_field(
                name="🕒 Date", value=log_entry["timestamp"], inline=False)

            if event in ["message_sent", "message_deleted"]:
                embed.add_field(name="💬 Message", value=log_entry.get(
                    "content", "Inconnu"), inline=False)
            elif event == "message_edited":
                embed.add_field(name="✏️ Avant", value=log_entry.get(
                    "before", "Inconnu"), inline=False)
                embed.add_field(name="🔄 Après", value=log_entry.get(
                    "after", "Inconnu"), inline=False)

            await channel.send(embed=embed)
