import discord
from discord.ext import commands
import json
import os


class Warnings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.file_path = "warnings.json"

        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as f:
                json.dump({}, f, indent=4)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, member: discord.Member, *, reason="Aucune raison spécifiée"):
        """Avertit un utilisateur et enregistre l'avertissement"""

        with open(self.file_path, "r") as f:
            warnings = json.load(f)

        user_id = str(member.id)

        if user_id not in warnings:
            warnings[user_id] = []

        warnings[user_id].append({
            "moderator": str(ctx.author),
            "reason": reason
        })

        with open(self.file_path, "w") as f:
            json.dump(warnings, f, indent=4)

        await ctx.send(f"⚠️ {member.mention} a été averti pour : `{reason}`")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def warnings(self, ctx, member: discord.Member):
        """Affiche la liste des avertissements d'un utilisateur"""

        with open(self.file_path, "r") as f:
            warnings = json.load(f)

        user_id = str(member.id)

        if user_id not in warnings or len(warnings[user_id]) == 0:
            await ctx.send(f"✅ {member.mention} n'a aucun avertissement.")
            return

        embed = discord.Embed(
            title=f"⚠️ Avertissements de {member.name}", color=discord.Color.orange())
        for i, warn in enumerate(warnings[user_id], start=1):
            embed.add_field(
                name=f"#{i} - Modérateur : {warn['moderator']}", value=f"📝 {warn['reason']}", inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clearwarns(self, ctx, member: discord.Member):
        """Efface tous les avertissements d'un utilisateur"""

        with open(self.file_path, "r") as f:
            warnings = json.load(f)

        user_id = str(member.id)

        if user_id not in warnings or len(warnings[user_id]) == 0:
            await ctx.send(f"✅ {member.mention} n'a aucun avertissement à supprimer.")
            return

        warnings[user_id] = []

        with open(self.file_path, "w") as f:
            json.dump(warnings, f, indent=4)

        await ctx.send(f"🗑️ Tous les avertissements de {member.mention} ont été supprimés.")


async def setup(bot):
    await bot.add_cog(Warnings(bot))
