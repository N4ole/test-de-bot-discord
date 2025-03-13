import discord
from discord.ext import commands


class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def poll(self, ctx, *, message: str):
        """
        Crée un sondage.
        Usage : !poll Question ? | Option 1 | Option 2 | Option 3
        """

        parts = message.split("|")
        if len(parts) < 2:
            await ctx.send("❌ Usage: `!poll Question ? | Option 1 | Option 2 | ...` (Minimum 2 options)")
            return

        question = parts[0].strip()
        options = [opt.strip() for opt in parts[1:]]

        if len(options) < 2 or len(options) > 10:
            await ctx.send("❌ Vous devez fournir entre **2 et 10 options** pour le sondage.")
            return

        emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣",
                  "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]

        embed = discord.Embed(
            title=f"📊 Sondage : {question}", color=discord.Color.blue())
        embed.set_footer(text=f"Sondage créé par {ctx.author.name}")

        description = ""
        for i, option in enumerate(options):
            description += f"{emojis[i]} {option}\n"

        embed.description = description

        poll_message = await ctx.send(embed=embed)

        for i in range(len(options)):
            await poll_message.add_reaction(emojis[i])


async def setup(bot):
    await bot.add_cog(Poll(bot))
