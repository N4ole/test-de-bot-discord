import discord
from discord.ext import commands
import json
import os


class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # Chargement des salons logs depuis .env
        self.logs_sent_channel_id = int(os.getenv("LOGS_SENT_CHANNEL_ID", 0))
        self.logs_deleted_channel_id = int(
            os.getenv("LOGS_DELETED_CHANNEL_ID", 0))
        self.logs_edited_channel_id = int(
            os.getenv("LOGS_EDITED_CHANNEL_ID", 0))

    @commands.command()
    async def logs(self, ctx, log_type: str = None):
        """Affiche les derniers logs. Usage : !logs [sent/deleted/edited]"""

        log_files = {
            "sent": "logs_sent.json",
            "deleted": "logs_deleted.json",
            "edited": "logs_edited.json"
        }

        if log_type not in log_files:
            await ctx.send("❌ Usage: `!logs [sent/deleted/edited]`")
            return

        file_path = log_files[log_type]

        if not os.path.exists(file_path):
            await ctx.send(f"⚠️ Aucun log trouvé pour `{log_type}`.")
            return

        with open(file_path, "r") as f:
            logs = json.load(f)

        if not logs:
            await ctx.send(f"⚠️ Aucun log enregistré pour `{log_type}`.")
            return

        logs = logs[-5:]  # On affiche uniquement les 5 derniers logs

        embed = discord.Embed(
            title=f"📄 Derniers logs `{log_type}`", color=discord.Color.blue())
        for log in logs:
            msg = f"📜 **{log['timestamp']}**\n"
            msg += f"👤 **Utilisateur:** {log['username']} ({log['user_id']})\n"
            msg += f"📍 **Salon:** {log['channel']}\n"

            if log_type == "sent" or log_type == "deleted":
                msg += f"💬 **Message:** {log.get('content', 'Inconnu')}\n"
            elif log_type == "edited":
                msg += f"✏️ **Avant:** {log.get('before', 'Inconnu')}\n"
                msg += f"🔄 **Après:** {log.get('after', 'Inconnu')}\n"

            embed.add_field(name="📝 Log", value=msg, inline=False)

        await ctx.send(embed=embed)

    async def send_log_to_channel(self, event, log_entry):
        """Envoie un log dans le salon Discord correspondant"""

        log_channels = {
            "message_sent": self.logs_sent_channel_id,
            "message_deleted": self.logs_deleted_channel_id,
            "message_edited": self.logs_edited_channel_id
        }

        channel_id = log_channels.get(event)
        if not channel_id or channel_id == 0:
            return

        channel = self.bot.get_channel(channel_id)
        if not channel:
            print(
                f"❌ Impossible de trouver le salon pour {event}. Vérifiez l'ID.")
            return

        embed = discord.Embed(
            title=f"📌 Log: {event.replace('_', ' ').title()}", color=discord.Color.blue())
        embed.add_field(name="👤 Utilisateur",
                        value=f"{log_entry['username']} ({log_entry['user_id']})", inline=False)
        embed.add_field(
            name="📍 Salon", value=log_entry["channel"], inline=False)
        embed.add_field(
            name="🕒 Date", value=log_entry["timestamp"], inline=False)

        if event == "message_sent" or event == "message_deleted":
            embed.add_field(name="💬 Message", value=log_entry.get(
                "content", "Inconnu"), inline=False)
        elif event == "message_edited":
            embed.add_field(name="✏️ Avant", value=log_entry.get(
                "before", "Inconnu"), inline=False)
            embed.add_field(name="🔄 Après", value=log_entry.get(
                "after", "Inconnu"), inline=False)

        await channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Logs(bot))
