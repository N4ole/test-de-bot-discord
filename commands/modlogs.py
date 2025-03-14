import discord
from discord.ext import commands
import json
import os
from datetime import datetime

MODLOGS_FILE = "modlogs.json"


class ModLogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def load_logs(self):
        """Charge les logs en s'assurant qu'ils sont bien au format dictionnaire"""
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
    @commands.has_permissions(administrator=True)
    async def modlogs(self, ctx, member: discord.Member):
        """Affiche l'historique des actions de modération sur un utilisateur"""
        logs = self.load_logs()
        user_id = str(member.id)

        if user_id not in logs or len(logs[user_id]) == 0:
            await ctx.send(f"📜 **Aucun historique de modération pour {member.mention}.**")
            return

        embed = discord.Embed(
            title=f"📜 Historique de Modération - {member.display_name}",
            color=discord.Color.red()
        )

        for log in logs[user_id]:
            embed.add_field(
                name=f"🔹 {log['action']} - {log['timestamp']}",
                value=f"👮 **Modérateur :** {log['moderator']}\n📄 **Raison :** {log['reason']}",
                inline=False
            )

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(ModLogs(bot))
