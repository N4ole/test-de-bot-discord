import discord
from discord.ext import commands
import json
import os
from datetime import datetime

MODLOGS_FILE = "modlogs.json"


class ModLogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logs = self.load_logs()

    # ✅ Charger les logs depuis le fichier JSON
    def load_logs(self):
        if os.path.exists(MODLOGS_FILE):
            with open(MODLOGS_FILE, "r") as f:
                return json.load(f)
        return {}

    # ✅ Sauvegarder les logs
    def save_logs(self):
        with open(MODLOGS_FILE, "w") as f:
            json.dump(self.logs, f, indent=4)

    # ✅ Ajouter un log pour un utilisateur
    def add_log(self, user_id, action, moderator, reason="Aucune raison spécifiée"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if str(user_id) not in self.logs:
            self.logs[str(user_id)] = []

        self.logs[str(user_id)].append({
            "action": action,
            "moderator": moderator,
            "reason": reason,
            "timestamp": timestamp
        })

        self.save_logs()

    # ✅ Commande pour afficher les logs d'un utilisateur
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def modlogs(self, ctx, member: discord.Member):
        """Affiche l'historique des actions modératrices sur un utilisateur."""
        user_id = str(member.id)

        if user_id not in self.logs or len(self.logs[user_id]) == 0:
            await ctx.send(f"📜 **Aucun historique de modération pour {member.mention}.**")
            return

        embed = discord.Embed(
            title=f"📜 Historique de Modération - {member.display_name}",
            color=discord.Color.red()
        )

        for log in self.logs[user_id]:
            embed.add_field(
                name=f"🔹 {log['action']} - {log['timestamp']}",
                value=f"👤 **Modérateur:** {log['moderator']}\n📄 **Raison:** {log['reason']}",
                inline=False
            )

        await ctx.send(embed=embed)

# ✅ Fonction pour charger le cog


async def setup(bot):
    await bot.add_cog(ModLogs(bot))
