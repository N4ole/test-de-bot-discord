import discord
from discord.ext import commands


class Purge(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: str = None):
        """
        Supprime un certain nombre de messages ou 'nuke' le salon.
        Usage :
        - `!purge 10` (supprime 10 messages)
        - `!purge nuke` (supprime le salon et le recrée)
        """

        if amount is None:
            await ctx.send("❌ Usage: `!purge <nombre>` ou `!purge nuke`")
            return

        if amount.lower() == "nuke":
            if not ctx.author.guild_permissions.manage_channels:
                await ctx.send("❌ Vous n'avez pas la permission de gérer les salons.")
                return

            channel = ctx.channel
            new_channel = await channel.clone(reason="Salon recréé après un nuke")
            await channel.delete(reason="Salon supprimé par commande !purge nuke")
            await new_channel.send(f"🔥 Salon recréé par {ctx.author.mention} !")

        else:
            try:
                amount = int(amount)
                if amount < 1 or amount > 100:
                    await ctx.send("❌ Veuillez spécifier un nombre entre 1 et 100.")
                    return

                await ctx.channel.purge(limit=amount + 1)
                confirmation = await ctx.send(f"🧹 {amount} messages ont été supprimés.")
                await confirmation.delete(delay=3)

            except ValueError:
                await ctx.send("❌ Usage: `!purge <nombre>` ou `!purge nuke`")


async def setup(bot):
    await bot.add_cog(Purge(bot))
