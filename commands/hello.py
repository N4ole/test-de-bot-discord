from discord.ext import commands


def setup(bot):
    @bot.command(name='hello')
    async def hello(ctx):
        await ctx.send(f"Salut {ctx.author.mention} ! 👋 Je suis en ligne 🟢")
