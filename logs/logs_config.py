import os
import json
import discord
from discord.ext import commands
import logging
from logs.logging_utils import log_to_json, send_log_to_channel

CONFIG_FILE = "server_config.json"


class LogsConfig(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.server_config = self.load_server_config()

    def load_server_config(self):
        """Charge la configuration des logs depuis le fichier JSON."""
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        return {}

    def save_server_config(self, config):
        """Sauvegarde la configuration des logs dans le fichier JSON."""
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=4)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setlog(self, ctx, log_type: str, channel: discord.TextChannel):
        """
        Change le salon où les logs sont envoyés.
        Utilisation : `!setlog <sent/deleted/edited/voice> #channel`
        """
        guild_id = str(ctx.guild.id)
        config = self.load_server_config()

        log_types = {
            "sent": "message_sent",
            "deleted": "message_deleted",
            "edited": "message_edited",
            "voice": "voice_log_channel"  # ✅ Ajout du log vocal
        }

        if log_type not in log_types:
            await ctx.send("❌ Type de log invalide. Utilisez `sent`, `deleted`, `edited`, ou `voice`.")
            return

        if guild_id not in config:
            config[guild_id] = {}

        config[guild_id][log_types[log_type]] = channel.id
        self.save_server_config(config)

        self.bot.server_config = self.load_server_config()

        await ctx.send(f"✅ Salon des logs `{log_type}` changé pour {channel.mention}.")

        updated_config = self.load_server_config()
        if updated_config.get(guild_id, {}).get(log_types[log_type]) == channel.id:
            await ctx.send(f"🔄 Vérification réussie : `{log_type}` est bien défini sur {channel.mention}.")
        else:
            await ctx.send("⚠️ Erreur : le changement de salon n'a pas été sauvegardé correctement.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def showlogs(self, ctx):
        """
        Affiche les salons de logs actuels pour le serveur.
        """
        guild_id = str(ctx.guild.id)
        config = self.load_server_config()

        if guild_id not in config:
            await ctx.send("⚠️ Aucun salon de logs défini pour ce serveur.")
            return

        embed = discord.Embed(
            title="📜 Configuration des Logs",
            color=discord.Color.blue()
        )

        log_types = {
            "message_sent": "📩 Messages envoyés",
            "message_deleted": "🗑️ Messages supprimés",
            "message_edited": "✏️ Messages modifiés",
            "voice_log_channel": "🎙️ Logs vocaux"  # ✅ Ajout des logs vocaux
        }

        for log_key, log_name in log_types.items():
            channel_id = config[guild_id].get(log_key, None)
            if channel_id:
                channel = self.bot.get_channel(channel_id)
                embed.add_field(
                    name=log_name,
                    value=channel.mention if channel else f"❌ `{channel_id}` (invalide)",
                    inline=False
                )
            else:
                embed.add_field(
                    name=log_name, value="❌ Aucun salon défini", inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def clearlogs(self, ctx, log_type: str):
        """
        Supprime les logs de `sent`, `deleted`, `edited`, ou `voice`.
        """
        guild_id = str(ctx.guild.id)
        config = self.load_server_config()

        log_files = {
            "sent": f"data/{guild_id}/logs_sent.json",
            "deleted": f"data/{guild_id}/logs_deleted.json",
            "edited": f"data/{guild_id}/logs_edited.json",
            # ✅ Ajout des logs vocaux
            "voice": f"data/{guild_id}/logs_voice.json"
        }

        if log_type not in log_files:
            await ctx.send("❌ Usage: `!clearlogs [sent/deleted/edited/voice]`")
            return

        file_path = log_files[log_type]

        if os.path.exists(file_path):
            with open(file_path, "w") as f:
                f.write("[]")
            await ctx.send(f"🗑️ Les logs `{log_type}` ont été supprimés.")
        else:
            await ctx.send(f"⚠️ Aucun fichier de logs `{log_type}` trouvé.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def debuglog(self, ctx, log_type: str):
        """Affiche le salon actuel utilisé pour un type de logs."""
        config = self.load_server_config()
        guild_id = str(ctx.guild.id)

        log_types = {
            "sent": "message_sent",
            "deleted": "message_deleted",
            "edited": "message_edited",
            "voice": "voice_log_channel"  # ✅ Ajout de la vérification pour logs vocaux
        }

        if log_type not in log_types:
            await ctx.send("❌ Type invalide. Utilisez `sent`, `deleted`, `edited`, ou `voice`.")
            return

        channel_id = config.get(guild_id, {}).get(log_types[log_type])

        if channel_id:
            channel = self.bot.get_channel(channel_id)
            if channel:
                await ctx.send(f"✅ Salon actuel pour `{log_type}` : {channel.mention} (ID: `{channel_id}`)")
            else:
                await ctx.send(f"⚠️ Le salon `{channel_id}` semble invalide ou supprimé.")
        else:
            await ctx.send(f"❌ Aucun salon défini pour `{log_type}`.")


async def setup(bot):
    await bot.add_cog(LogsConfig(bot))
