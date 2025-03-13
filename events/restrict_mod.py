import discord
from discord.ext import commands


class RestrictMod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ✅ Vérifie chaque commande avant exécution
    @commands.Cog.listener()
    async def on_command(self, ctx):
        """Bloque l'accès aux commandes de modération pour les non-administrateurs"""

        # ✅ Liste mise à jour des commandes de modération de TON BOT
        moderation_commands = [
            "ban", "kick", "mute", "unmute", "warn", "clear", "lock", "unlock",
            "watchlist", "setlog", "purge", "nuke"
        ]

        # ✅ Vérifie si la commande exécutée est une commande de modération
        if ctx.command and ctx.command.name in moderation_commands:
            if not ctx.author.guild_permissions.administrator:
                await ctx.send("🚫 **Accès refusé !** Seuls les administrateurs peuvent utiliser cette commande.")
                await ctx.message.delete()  # Supprime la commande pour éviter les abus
                return

# ✅ Fonction pour charger le cog


async def setup(bot):
    await bot.add_cog(RestrictMod(bot))
