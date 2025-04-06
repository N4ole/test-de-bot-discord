from discord.ext import commands
from utils.logger import send_log


def setup(bot):
    @bot.command(name='clear')
    @commands.has_permissions(manage_messages=True)
    async def clear(ctx, amount: int = 5):
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"🧼 {amount} messages supprimés.", delete_after=3)
        await send_log(bot, ctx.guild.id, f"🧼 {ctx.author.mention} a supprimé {amount} messages dans {ctx.channel.mention}")

    @clear.error
    async def clear_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ Tu n'as pas la permission d'utiliser cette commande.")
