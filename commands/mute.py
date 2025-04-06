from discord.ext import commands
import discord
from utils.logger import send_log


async def get_or_create_muted_role(guild: discord.Guild):
    muted_role = discord.utils.get(guild.roles, name="Muted")
    if not muted_role:
        muted_role = await guild.create_role(name="Muted", reason="Création du rôle pour mute")

        for channel in guild.text_channels:
            await channel.set_permissions(muted_role, send_messages=False, add_reactions=False)
    return muted_role


def setup(bot):
    @bot.command(name='mute')
    @commands.has_permissions(manage_roles=True)
    async def mute(ctx, member: discord.Member, *, reason=None):
        muted_role = await get_or_create_muted_role(ctx.guild)
        await member.add_roles(muted_role, reason=reason)
        await ctx.send(f"🔇 {member.mention} a été mute. Raison: {reason or 'Non précisée'}")

    @mute.error
    async def mute_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("🚫 Tu n’as pas la permission de mute.")
        else:
            await ctx.send("❌ Erreur dans la commande `!mute`.")

    @bot.command(name='unmute')
    @commands.has_permissions(manage_roles=True)
    async def unmute(ctx, member: discord.Member):
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if muted_role and muted_role in member.roles:
            await member.remove_roles(muted_role)
            await ctx.send(f"🔊 {member.mention} a été unmute.")
        else:
            await ctx.send(f"ℹ️ {member.mention} n'était pas mute.")

    @unmute.error
    async def unmute_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("🚫 Tu n’as pas la permission de unmute.")
        else:
            await ctx.send("❌ Erreur dans la commande `!unmute`.")
