import discord
from discord.ext import commands


class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ✅ Gestion des erreurs de permissions
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ **Vous n'avez pas les permissions nécessaires pour utiliser cette commande !**")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("⚠️ **Argument manquant.** Vérifiez l'utilisation de la commande.")
        else:
            await ctx.send(f"🚨 **Erreur :** {error}")

# ✅ Fonction pour charger le cog


async def setup(bot):
    await bot.add_cog(ErrorHandler(bot))
