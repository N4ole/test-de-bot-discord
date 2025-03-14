from discord.ext import commands
import random


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def roll(self, ctx):
        """lance un dés à 6 faces"""
        number = random.randint(1, 6)
        await ctx.send(f"🎲 You rolled a {number}!")


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def eightball(self, ctx, *, question: str):
        """Posez une question à la boule magique"""
        responses = [
            "Yes!", "No!", "Maybe...", "Ask again later!",
            "I don't think so.", "Absolutely!", "Not a chance!"
        ]
        await ctx.send(f"🎱 {random.choice(responses)}")

    @commands.command()
    async def meme(self, ctx):
        """Envoie un meme aléatoire"""
        memes = [
            "https://i.imgur.com/W3duR07.png",
            "https://i.imgur.com/aQw5bLw.jpeg",
            "https://i.imgur.com/Jt1Ry6v.jpg"
        ]
        await ctx.send(random.choice(memes))


async def setup(bot):
    await bot.add_cog(Fun(bot))
