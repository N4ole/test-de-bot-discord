import os
import json
import discord
from discord.ext import commands
import logging

CONFIG_FILE = "server_config.json"


class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
    async def adminonly(self, ctx):
        """Commande accessible uniquement aux administrateurs"""
        await ctx.send("✅ Vous avez la permission administrateur !")

    @commands.command()
    async def checkperms(self, ctx, member: discord.Member = None):
        """Vérifie si un membre a la permission administrateur"""
        member = member or ctx.author
        if member.guild_permissions.administrator:
            await ctx.send(f"✅ {member.mention} possède les permissions administrateur.")
        else:
            await ctx.send(f"❌ {member.mention} n'a **pas** les permissions administrateur.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def reload(self, ctx, extension: str):
        """Recharge un module sans redémarrer le bot (ex: !reload moderation)"""
        try:
            await self.bot.reload_extension(f"commands.{extension}")
            await ctx.send(f"✅ Module `{extension}` rechargé avec succès !")
            logging.info(
                f"🔄 Le module '{extension}' a été rechargé par {ctx.author}.")
        except commands.ExtensionError as e:
            await ctx.send(f"❌ Erreur lors du rechargement de `{extension}` : {e}")
            logging.error(f"❌ Échec du rechargement de '{extension}': {e}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def togglelog(self, ctx, log_type: str):
        """Active ou désactive un type de logs (ex: `!togglelog sent`)."""
        guild_id = str(ctx.guild.id)
        config = self.load_server_config()

        log_types = {
            "sent": "message_sent",
            "deleted": "message_deleted",
            "edited": "message_edited"
        }

        if log_type not in log_types:
            await ctx.send("⚠️ Type de log invalide. Utilisez `sent`, `deleted`, ou `edited`.")
            return

        if guild_id not in config:
            config[guild_id] = {}

        setting_key = f"{log_types[log_type]}_enabled"
        config[guild_id][setting_key] = not config[guild_id].get(
            setting_key, True)

        self.save_server_config(config)

        status = "✅ **activé**" if config[guild_id][setting_key] else "❌ **désactivé**"
        await ctx.send(f"🔄 Logs `{log_type}` {status} pour ce serveur.")


async def setup(bot):
    await bot.add_cog(AdminCommands(bot))
