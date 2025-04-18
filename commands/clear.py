from discord.ext import commands
from utils.logger import send_log
from utils.logger import send_log
import discord


def setup(bot):
    @bot.command(name='clear')
    @commands.has_permissions(manage_messages=True)
    async def clear(ctx, amount: int = 5):
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"🧼 {amount} messages supprimés.", delete_after=3)
        await send_log(
            bot,
            ctx.guild.id,
            title="🧼 Messages supprimés",
            description=f"**Modérateur :** {ctx.author.mention}\n**Quantité :** {amount}\n**Salon :** {ctx.channel.mention}",
            color=discord.Color.gold()
        )
