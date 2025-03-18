from config import get_log_channel
from discord.ext import commands
import discord
import os
from datetime import datetime


async def setup(bot):
    log_dir = 'logs/messages'
    log_file = os.path.join(log_dir, 'messages.log')
    os.makedirs(log_dir, exist_ok=True)

    def log_to_file(entry):
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(entry + "\n")

    def log_header(guild, channel):
        date = datetime.now().strftime("%d/%m/%y")
        return f"[{date}] Serveur: {guild.name} ({guild.id}) | Salon: {channel.name} ({channel.id})"

    @bot.event
    async def on_message(message):
        if message.author.bot:
            return

        header = log_header(message.guild, message.channel)
        user_info = f"Utilisateur: {message.author.name} ({message.author.id}) a envoyé :"
        content = f"> {message.content}"

        log_entry = f"{header}\n{user_info}\n{content}"
        log_to_file(log_entry)

    @bot.event
    async def on_message_edit(before, after):
        if before.author.bot:
            return

        header = log_header(before.guild, before.channel)
        user_info = f"Utilisateur: {before.author.name} ({before.author.id}) a modifié son message :"
        before_content = f"> Avant: {before.content}"
        after_content = f"> Après: {after.content}"

        log_entry = f"{header}\n{user_info}\n{before_content}\n{after_content}"
        log_to_file(log_entry)

    @bot.event
    async def on_message_delete(message):
        if message.author.bot:
            return

        header = log_header(message.guild, message.channel)
        user_info = f"Message supprimé de: {message.author.name} ({message.author.id})"
        content = f"> Contenu: {message.content}"

        # Cherche qui a supprimé
        deleter_info = "Utilisateur ayant supprimé: Inconnu"
        try:
            entry = None
            async for log in message.guild.audit_logs(limit=1, action=discord.AuditLogAction.message_delete):
                if log.target.id == message.author.id:
                    deleter_info = f"Utilisateur ayant supprimé: {log.user.name} ({log.user.id})"
                    break
        except Exception as e:
            deleter_info = f"Utilisateur ayant supprimé: Erreur audit log ({e})"

        log_entry = f"{header}\n{user_info}\n{deleter_info}\n{content}"
        log_to_file(log_entry)


async def send_log_embed(log_type, embed):
    channel_id = get_log_channel(log_type)
    if channel_id:
        channel = bot.get_channel(channel_id)
        if channel:
            try:
                await channel.send(embed=embed)
            except Exception as e:
                print(f"[ERROR] Log {log_type} : {e}")
