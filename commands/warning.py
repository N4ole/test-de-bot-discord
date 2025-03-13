import discord
from discord.ext import commands
import json
import os
from datetime import datetime

WARNINGS_FILE = "warnings.json"
MODLOGS_FILE = "modlogs.json"


class Warnings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.load_files()

    def load_files(self):
        """Charge les fichiers JSON"""
        for file in [WARNINGS_FILE, MODLOGS_FILE]:
            if not os.path.exists(file):
                with open(file, "w") as f:
                    json.dump({}, f, indent=4)

    def save_data(self, file, data):
        """Sauvegarde les données dans un fichier JSON"""
        with open(file, "w") as f:
            json.dump(data, f, indent=4)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, member: discord.Member, *, reason="Aucune raison spécifiée"):
        """Avertit un utilisateur et enregistre l'avertissement"""

        with open(WARNINGS_FILE, "r") as f:
            warnings = json.load(f)

        with open(MODLOGS_FILE, "r") as f:
            modlogs = json.load(f)

        user_id = str(member.id)
        mod_id = str(ctx.author.id)

        if user_id not in warnings:
            warnings[user_id] = []

        warnings[user_id].append({
            "moderator": str(ctx.author),
            "reason": reason,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        self.save_data(WARNINGS_FILE, warnings)

        if mod_id not in modlogs:
            modlogs[mod_id] = []

        modlogs[mod_id].append({
            "action": "Warn",
            "user": str(member),
            "reason": reason,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        self.save_data(MODLOGS_FILE, modlogs)

        await ctx.send(f"⚠️ {member.mention} a été averti par {ctx.author.mention} pour : `{reason}`")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def warnings(self, ctx, member: discord.Member):
        """Affiche la liste des avertissements d'un utilisateur"""

        with open(WARNINGS_FILE, "r") as f:
            warnings = json.load(f)

        user_id = str(member.id)

        if user_id not in warnings or len(warnings[user_id]) == 0:
            await ctx.send(f"✅ {member.mention} n'a aucun avertissement.")
            return

        embed = discord.Embed(
            title=f"⚠️ Avertissements de {member.name}", color=discord.Color.orange())
        for i, warn in enumerate(warnings[user_id], start=1):
            embed.add_field(
                name=f"#{i} - Modérateur : {warn['moderator']} ({warn['timestamp']})",
                value=f"📝 {warn['reason']}", inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clearwarns(self, ctx, member: discord.Member):
        """Efface tous les avertissements d'un utilisateur"""

        with open(WARNINGS_FILE, "r") as f:
            warnings = json.load(f)

        user_id = str(member.id)

        if user_id not in warnings or len(warnings[user_id]) == 0:
            await ctx.send(f"✅ {member.mention} n'a aucun avertissement à supprimer.")
            return

        warnings[user_id] = []

        self.save_data(WARNINGS_FILE, warnings)
        await ctx.send(f"🗑️ Tous les avertissements de {member.mention} ont été supprimés.")


async def setup(bot):
    await bot.add_cog(Warnings(bot))
