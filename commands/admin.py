import discord
from discord.ext import commands


class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ✅ Commande réservée aux administrateurs
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def adminonly(self, ctx):
        """Commande accessible uniquement aux administrateurs"""
        await ctx.send("✅ Vous avez la permission administrateur !")

    # ✅ Commande pour vérifier les permissions d'un utilisateur
    @commands.command()
    async def checkperms(self, ctx, member: discord.Member = None):
        """Vérifie si un membre a la permission administrateur"""
        member = member or ctx.author
        if member.guild_permissions.administrator:
            await ctx.send(f"✅ {member.mention} possède les permissions administrateur.")
        else:
            await ctx.send(f"❌ {member.mention} n'a **pas** les permissions administrateur.")

# ✅ Fonction pour charger le cog


async def setup(bot):
    await bot.add_cog(AdminCommands(bot))
