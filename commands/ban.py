from discord.ext import commands
from utils.logger import send_log
import discord
from engine import DEBUG_MODE


def setup(bot):
    @bot.command(name='ban')
    @commands.has_permissions(ban_members=True)
    async def ban(ctx, member: commands.MemberConverter, *, reason=None):
        if DEBUG_MODE:
            await ctx.send(f"🐞 [DEBUG] Le bot aurait banni {member.mention}, mais le mode debug est actif.")
            print(
                f"[DEBUG] BAN simulé : {member} par {ctx.author} | Raison : {reason}")
        else:
            await member.ban(reason=reason)
            await ctx.send(f"🔨 {member.mention} a été banni.")
            await send_log(
                bot,
                ctx.guild.id,
                title="🔨 Bannissement",
                description=f"**Membre :** {member.mention}\n**Modérateur :** {ctx.author.mention}\n**Raison :** {reason or 'Non précisée'}",
                color=discord.Color.red()
            )
