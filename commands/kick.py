from discord.ext import commands
from utils.logger import send_log
import discord
from engine import DEBUG_MODE


def setup(bot):
    @bot.command(name='kick')
    @commands.has_permissions(kick_members=True)
    async def kick(ctx, member: commands.MemberConverter, *, reason=None):
        if DEBUG_MODE:
            await ctx.send(f"🐞 [DEBUG] Le bot aurait kické {member.mention}, mais le mode debug est actif.")
            print(
                f"[DEBUG] KICK simulé : {member} par {ctx.author} | Raison : {reason}")
        else:
            await member.kick(reason=reason)
            await ctx.send(f"👢 {member.mention} a été kické.")
            await send_log(
                bot,
                ctx.guild.id,
                title="👢 Expulsion",
                description=f"**Membre :** {member.mention}\n**Modérateur :** {ctx.author.mention}\n**Raison :** {reason or 'Non précisée'}",
                color=discord.Color.orange()
            )
