from discord.ext import commands


def setup(bot):
    @bot.command(name='ping')
    async def ping(ctx):
        await ctx.send(f"Pong 🏓! Latence: `{round(bot.latency * 1000)}ms`")
