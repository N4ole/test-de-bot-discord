from discord.ext import commands
from utils.logger import send_log


def setup(bot):
    @bot.command(name='ban')
    @commands.has_permissions(ban_members=True)
    async def ban(ctx, member: commands.MemberConverter, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f"🔨 {member.mention} a été banni. Raison: {reason or 'Aucune'}")
        await send_log(bot, ctx.guild.id, f"🔨 {member.mention} a été banni par {ctx.author.mention}. Raison : {reason or 'Aucune'}")

    @ban.error
    async def ban_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ Tu n'as pas la permission de bannir.")
