from discord.ext import commands


class Math(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def add(self, ctx, a: float, b: float):
        """Add two numbers together"""
        await ctx.send(f"➕ {a} + {b} = {a + b}")

    @commands.command()
    async def multiply(self, ctx, a: float, b: float):
        """Multiply two numbers together"""
        await ctx.send(f"✖ {a} × {b} = {a * b}")

    @commands.command()
    async def divide(self, ctx, a: float, b: float):
        """Divide two numbers"""
        if b == 0:
            await ctx.send("❌ Cannot divide by zero!")
        else:
            await ctx.send(f"➗ {a} ÷ {b} = {a / b}")


async def setup(bot):
    await bot.add_cog(Math(bot))
