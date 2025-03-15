import discord
from discord.ext import commands


class StatusUpdate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def update_bot_status(self):
        """Met à jour le statut du bot avec le nombre de serveurs actuels."""
        total_guilds = len(self.bot.guilds)
        activity = discord.Game(name=f"Présent sur {total_guilds} serveurs")
        await self.bot.change_presence(activity=activity)

    @commands.Cog.listener()
    async def on_ready(self):
        """Mise à jour du statut au démarrage du bot."""
        await self.update_bot_status()

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        """Mise à jour du statut lorsque le bot rejoint un nouveau serveur."""
        await self.update_bot_status()

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        """Mise à jour du statut lorsque le bot quitte un serveur."""
        await self.update_bot_status()


async def setup(bot):
    await bot.add_cog(StatusUpdate(bot))
