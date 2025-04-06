from discord.ext import commands
from utils.logger import send_log


def setup(bot):
    @bot.command(name='kick')
    @commands.has_permissions(kick_members=True)
    async def kick(ctx, member: commands.MemberConverter, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f"👢 {member.mention} a été kické. Raison: {reason or 'Aucune'}")
        await send_log(bot, ctx.guild.id, f"👢 {member.mention} a été kické par {ctx.author.mention}. Raison : {reason or 'Aucune'}")

    @kick.error
    async def kick_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ Tu n'as pas la permission de kicker.")
