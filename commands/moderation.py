import discord
from discord.ext import commands


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ✅ Commande de bannissement
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ban(self, ctx, member: discord.Member, *, reason="Aucune raison spécifiée"):
        """Bannit un utilisateur du serveur"""
        await member.ban(reason=reason)
        await ctx.send(f"🔨 **{member.mention} a été banni !** Raison : {reason}")

        # ✅ Enregistrer l'action dans les logs
        modlogs_cog = self.bot.get_cog("ModLogs")
        if modlogs_cog:
            modlogs_cog.add_log(member.id, "Ban", ctx.author.name, reason)

    # ✅ Commande d'expulsion (Kick)
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx, member: discord.Member, *, reason="Aucune raison spécifiée"):
        """Expulse un utilisateur du serveur"""
        await member.kick(reason=reason)
        await ctx.send(f"👢 **{member.mention} a été expulsé !** Raison : {reason}")

        # ✅ Enregistrer l'action dans les logs
        modlogs_cog = self.bot.get_cog("ModLogs")
        if modlogs_cog:
            modlogs_cog.add_log(member.id, "Kick", ctx.author.name, reason)

    # ✅ Commande de mute
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def mute(self, ctx, member: discord.Member, *, reason="Aucune raison spécifiée"):
        """Rend un membre muet"""
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not role:
            role = await ctx.guild.create_role(name="Muted", permissions=discord.Permissions(send_messages=False))
            for channel in ctx.guild.channels:
                await channel.set_permissions(role, send_messages=False)

        await member.add_roles(role)
        await ctx.send(f"🔇 **{member.mention} a été mute !** Raison : {reason}")

        # ✅ Enregistrer l'action dans les logs
        modlogs_cog = self.bot.get_cog("ModLogs")
        if modlogs_cog:
            modlogs_cog.add_log(member.id, "Mute", ctx.author.name, reason)


async def setup(bot):
    await bot.add_cog(Moderation(bot))
