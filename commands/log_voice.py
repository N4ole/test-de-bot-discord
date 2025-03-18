from config import get_log_channel
from discord.ext import commands
import discord
import os
from datetime import datetime


async def setup(bot):
    log_dir = 'logs/voice'
    log_file = os.path.join(log_dir, 'voice.log')
    os.makedirs(log_dir, exist_ok=True)

    def log_to_file(entry):
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(entry + "\n")

    def timestamp():
        return datetime.now().strftime("[%d/%m/%y %H:%M:%S]")

    @bot.event
    async def on_voice_state_update(member, before, after):
        time = timestamp()
        base_info = f"{time} Utilisateur: {member.name} ({member.id})"

        events = []

        # Connexion / Déconnexion / Changement de salon
        if before.channel != after.channel:
            if before.channel is None and after.channel:
                events.append(
                    f"s'est CONNECTÉ à {after.channel.name} ({after.channel.id})")
            elif after.channel is None and before.channel:
                events.append(
                    f"s'est DÉCONNECTÉ de {before.channel.name} ({before.channel.id})")
            else:
                events.append(
                    f"a CHANGÉ de {before.channel.name} ({before.channel.id}) ➜ {after.channel.name} ({after.channel.id})")

        # Mute micro
        if before.self_mute != after.self_mute:
            action = "s'est MUTÉ (micro)" if after.self_mute else "s'est DÉMUTÉ (micro)"
            events.append(action)

        # Mute casque
        if before.self_deaf != after.self_deaf:
            action = "a MUTÉ son casque" if after.self_deaf else "a DÉMUTÉ son casque"
            events.append(action)

        # Log si au moins 1 événement détecté
        if events:
            log_entry = f"{base_info} ➜ " + " | ".join(events)
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
