from discord.ext import commands
import discord


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def userinfo(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        embed = discord.Embed(
            title=f"User Info - {member}", color=discord.Color.blue())
        embed.set_thumbnail(url=member.avatar.url)
        embed.add_field(name="Username", value=member.name, inline=True)
        embed.add_field(name="User ID", value=member.id, inline=True)
        embed.add_field(name="Joined Server", value=member.joined_at.strftime(
            "%Y-%m-%d"), inline=True)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Info(bot))
