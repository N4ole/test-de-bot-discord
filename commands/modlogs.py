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
        if os.path.exists(MODLOGS_FILE):
            with open(MODLOGS_FILE, "r") as f:
                return json.load(f)
        return {}

    def save_logs(self, logs):
        with open(MODLOGS_FILE, "w") as f:
            json.dump(logs, f, indent=4)

    def add_log(self, user_id, action, moderator_id, reason="Aucune raison spécifiée"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        logs = self.load_logs()
        if str(user_id) not in logs:
            logs[str(user_id)] = []

        logs[str(user_id)].append({
            "action": action,
            "moderator": f"<@{moderator_id}>",
            "reason": reason,
            "timestamp": timestamp
        })

        if str(moderator_id) not in logs:
            logs[str(moderator_id)] = []

        logs[str(moderator_id)].append({
            "action": action,
            "user": f"<@{user_id}>",
            "reason": reason,
            "timestamp": timestamp
        })

        self.save_logs(logs)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def modlogs(self, ctx, member: discord.Member):
        """Affiche l'historique des actions modératrices sur un utilisateur ou les actions d'un modérateur."""
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
            if "user" in log:
                embed.add_field(
                    name=f"🔹 {log['action']} - {log['timestamp']}",
                    value=f"👤 **Utilisateur ciblé :** {log['user']}\n📄 **Raison :** {log['reason']}",
                    inline=False
                )
            else:
                embed.add_field(
                    name=f"🔹 {log['action']} - {log['timestamp']}",
                    value=f"👤 **Modérateur :** {log['moderator']}\n📄 **Raison :** {log['reason']}",
                    inline=False
                )

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(ModLogs(bot))
