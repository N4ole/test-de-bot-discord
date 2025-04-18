import discord
from discord.ext import commands
import asyncio
import sys
from utils.logger import send_log


def setup(bot):
    @bot.command(name='shutdown')
    @commands.has_permissions(administrator=True)
    async def shutdown_bot(ctx):
        await ctx.send("🛑 Extinction du bot en cours...")
        print("[⛔] Arrêt demandé par", ctx.author)

        await send_log(
            bot,
            ctx.guild.id,
            title="⛔ Arrêt du bot",
            description=f"Commande exécutée par : {ctx.author.mention}",
            color=discord.Color.red()
        )

        await bot.close()
        await asyncio.sleep(1)
        sys.exit(0)
