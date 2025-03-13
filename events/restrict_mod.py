import discord
from discord.ext import commands


class RestrictMod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command(self, ctx):
        """Bloque l'accès aux commandes de modération pour les non-administrateurs"""

        moderation_commands = [
            "ban", "kick", "mute", "unmute", "warn", "clear", "lock", "unlock",
            "watchlist", "setlog", "purge", "nuke"
        ]

        if ctx.command and ctx.command.name in moderation_commands:
            if not ctx.author.guild_permissions.administrator:
                await ctx.send("🚫 **Accès refusé !** Seuls les administrateurs peuvent utiliser cette commande.")
                await ctx.message.delete()
                return


async def setup(bot):
    await bot.add_cog(RestrictMod(bot))
