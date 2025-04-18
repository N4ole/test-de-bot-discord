from discord.ext import commands
from utils.logger import load_log_config
import discord


def setup(bot):
    @bot.command(name="logstatus")
    @commands.has_permissions(administrator=True)
    async def log_status(ctx):
        guild_id = str(ctx.guild.id)
        config = load_log_config()

        log_entry = config.get(guild_id)

        if not log_entry:
            await ctx.send("⚠️ Aucun salon de log n’est configuré pour ce serveur.")
            return

        # Support ancien format (juste l’ID)
        if isinstance(log_entry, str):
            channel_id = int(log_entry)
            channel = bot.get_channel(channel_id)
            embed = discord.Embed(
                title="📝 Log configuré",
                description=f"Ancien format détecté (ID uniquement).\nSalon ID : `{channel_id}`",
                color=discord.Color.orange()
            )
        else:
            channel_id = int(log_entry["channel_id"])
            channel_name = log_entry.get("channel_name", "❓ Inconnu")
            embed = discord.Embed(
                title="📝 Log configuré",
                color=discord.Color.green()
            )
            embed.add_field(
                name="Salon", value=f"<#{channel_id}>", inline=True)
            embed.add_field(name="Nom", value=channel_name, inline=True)
            embed.add_field(name="ID", value=channel_id, inline=True)

        if not bot.get_channel(channel_id):
            embed.color = discord.Color.red()
            embed.set_footer(
                text="⚠️ Attention : le salon n'existe plus ou est inaccessible.")

        await ctx.send(embed=embed)
