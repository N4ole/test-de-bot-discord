import discord
from discord.ext import commands
import json
import os
from datetime import datetime
from logs.logging_utils import log_to_json, send_log_to_channel, load_server_config, save_server_config


# Fichier de configuration des logs
VOICE_LOGS_DIR = "../data/voice_logs"


class VoiceLogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        os.makedirs(VOICE_LOGS_DIR, exist_ok=True)

    def get_log_file(self, guild_id):
        """Retourne le chemin du fichier de logs vocaux d'un serveur."""
        guild_folder = f"{VOICE_LOGS_DIR}/{guild_id}"
        os.makedirs(guild_folder, exist_ok=True)
        return f"{guild_folder}/voice_logs.json"

    def log_voice_event(self, guild_id, log_entry):
        """Sauvegarde un événement vocal dans le fichier JSON du serveur."""
        log_file = self.get_log_file(guild_id)

        if os.path.exists(log_file):
            with open(log_file, "r") as f:
                try:
                    logs = json.load(f)
                    if not isinstance(logs, list):
                        logs = []
                except json.JSONDecodeError:
                    logs = []
        else:
            logs = []

        logs.append(log_entry)

        with open(log_file, "w") as f:
            json.dump(logs, f, indent=4)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        """Détecte et log les changements d'état vocal."""
        guild_id = str(member.guild.id)
        log_entry = {
            "username": str(member),
            "user_id": str(member.id),
            "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
            "event": None
        }

        if before.channel is None and after.channel is not None:
            log_entry["event"] = f"🔊 {member.mention} a rejoint **{after.channel.name}**"
        elif before.channel is not None and after.channel is None:
            log_entry["event"] = f"🔇 {member.mention} a quitté **{before.channel.name}**"
        elif before.channel != after.channel:
            log_entry["event"] = f"🔁 {member.mention} est passé de **{before.channel.name}** à **{after.channel.name}**"

        if before.self_mute != after.self_mute:
            if after.self_mute:
                log_entry["event"] = f"🔕 {member.mention} s'est muté"
            else:
                log_entry["event"] = f"🔊 {member.mention} s'est démuté"

        if before.self_deaf != after.self_deaf:
            if after.self_deaf:
                log_entry["event"] = f"🔇 {member.mention} s'est rendu sourd"
            else:
                log_entry["event"] = f"🔉 {member.mention} a réactivé le son"

        if before.mute != after.mute:
            if after.mute:
                log_entry["event"] = f"⚠️ {member.mention} a été muté par un administrateur"
            else:
                log_entry["event"] = f"✅ {member.mention} a été démuté par un administrateur"

        if before.deaf != after.deaf:
            if after.deaf:
                log_entry["event"] = f"⚠️ {member.mention} a été rendu sourd par un administrateur"
            else:
                log_entry["event"] = f"✅ {member.mention} a été réactivé par un administrateur"

        if log_entry["event"]:
            self.log_voice_event(guild_id, log_entry)
            await self.send_log_to_channel(member.guild, log_entry)

    async def send_log_to_channel(self, guild, log_entry):
        """Envoie un log dans le salon de logs vocaux si configuré."""
        config_file = "server_config.json"

        if os.path.exists(config_file):
            with open(config_file, "r") as f:
                config = json.load(f)
        else:
            config = {}

        guild_id = str(guild.id)
        log_channel_id = config.get(guild_id, {}).get("voice_log_channel")

        if log_channel_id:
            channel = self.bot.get_channel(int(log_channel_id))
            if channel:
                embed = discord.Embed(
                    title="🎙️ Log vocal",
                    description=log_entry["event"],
                    color=discord.Color.blue(),
                    timestamp=datetime.utcnow()
                )
                embed.set_footer(text=f"Utilisateur: {log_entry['username']}")

                await channel.send(embed=embed)

    @commands.command(name="setvoicelog")
    @commands.has_permissions(administrator=True)
    async def setvoicelog(self, ctx, log_type: str, channel: discord.TextChannel):
        """Définit le salon pour les logs vocaux."""

        guild_id = str(ctx.guild.id)
        config = self.load_server_config()

        if guild_id not in config:
            config[guild_id] = {}

        config[guild_id]["voice_log_channel"] = channel.id
        self.save_server_config(config)

        await ctx.send(f"✅ Salon des logs vocaux défini sur {channel.mention}.")

        if log_type.lower() != "voice":
            await ctx.send("❌ Type de log invalide. Utilisez `voice` pour les logs vocaux.")
            return

        config_file = "server_config.json"
        guild_id = str(ctx.guild.id)

        if os.path.exists(config_file):
            with open(config_file, "r") as f:
                config = json.load(f)
        else:
            config = {}

        if guild_id not in config:
            config[guild_id] = {}

        config[guild_id]["voice_log_channel"] = channel.id

        with open(config_file, "w") as f:
            json.dump(config, f, indent=4)

        await ctx.send(f"✅ Salon de logs vocaux défini sur {channel.mention}")


async def setup(bot):
    await bot.add_cog(VoiceLogs(bot))


@commands.command(name="showvoicelog")
@commands.has_permissions(administrator=True)
async def showvoicelog(self, ctx):
    """
    Affiche le salon actuel utilisé pour les logs vocaux.
    Utilisation : `!showvoicelog`
    """
    guild_id = str(ctx.guild.id)
    config = self.load_server_config()

    channel_id = config.get(guild_id, {}).get("voice_log_channel")

    if channel_id:
        channel = self.bot.get_channel(channel_id)
        if channel:
            await ctx.send(f"📢 Le salon actuel des logs vocaux est {channel.mention}.")
        else:
            await ctx.send(f"⚠️ Le salon `{channel_id}` n'existe plus ou n'est pas valide.")
    else:
        await ctx.send("❌ Aucun salon défini pour les logs vocaux.")
