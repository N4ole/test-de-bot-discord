import discord
from discord.ext import commands
import json
import os
from datetime import datetime

MODLOGS_FILE = "modlogs.json"


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def load_logs(self):
        """Charge les logs depuis modlogs.json et corrige la structure si nécessaire"""
        if os.path.exists(MODLOGS_FILE):
            try:
                with open(MODLOGS_FILE, "r") as f:
                    logs = json.load(f)

                    if not isinstance(logs, dict):
                        logs = {}
                    return logs
            except json.JSONDecodeError:
                return {}
        return {}

    def save_logs(self, logs):
        """Sauvegarde les logs sans risque de corruption JSON"""
        with open(MODLOGS_FILE, "w") as f:
            json.dump(logs, f, indent=4)

    def add_log(self, user_id, action, moderator, reason="Aucune raison spécifiée"):
        """Ajoute un log de modération dans modlogs.json"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logs = self.load_logs()

        if str(user_id) not in logs:
            logs[str(user_id)] = []

        logs[str(user_id)].append({
            "action": action,
            "moderator": moderator,
            "reason": reason,
            "timestamp": timestamp
        })

        self.save_logs(logs)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, *, reason="Aucune raison spécifiée"):
        """Mute un utilisateur en lui attribuant un rôle 'Muted'"""

        role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not role:
            role = await ctx.guild.create_role(name="Muted", permissions=discord.Permissions(send_messages=False))
            for channel in ctx.guild.channels:
                await channel.set_permissions(role, send_messages=False)

        await member.add_roles(role)
        await ctx.send(f"🔇 **{member.mention} a été mute !** Raison : {reason}")

        self.add_log(member.id, "Mute", ctx.author.name, reason)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member):
        """Retire le mute d'un utilisateur"""
        role = discord.utils.get(ctx.guild.roles, name="Muted")

        if role in member.roles:
            await member.remove_roles(role)
            await ctx.send(f"🔊 **{member.mention} a été unmute !**")
            self.add_log(member.id, "Unmute",
                         ctx.author.name, "Révoqué le mute")
        else:
            await ctx.send(f"⚠️ **{member.mention} n'est pas mute.**")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ban(self, ctx, member: discord.Member, *, reason="Aucune raison spécifiée"):
        """Bannit un utilisateur du serveur"""
        try:
            await member.ban(reason=reason)
            await ctx.send(f"✅ {member.mention} a été **banni** pour : `{reason}`")
            self.add_log(member.id, "Ban", ctx.author.name, reason)
        except discord.Forbidden:
            await ctx.send("❌ Je n'ai pas la permission de bannir cet utilisateur.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx, member: discord.Member, *, reason="Aucune raison spécifiée"):
        """Expulse un utilisateur du serveur"""
        try:
            await member.kick(reason=reason)
            await ctx.send(f"✅ {member.mention} a été **expulsé** pour : `{reason}`")
            self.add_log(member.id, "Kick", ctx.author.name, reason)
        except discord.Forbidden:
            await ctx.send("❌ Je n'ai pas la permission d'expulser cet utilisateur.")


async def setup(bot):
    await bot.add_cog(Moderation(bot))
