import discord
from discord.ext import commands
from utils.time import get_french_datetime, get_french_time_str
from engine import startup_time, BOT_VERSION, DEBUG_MODE


def setup(bot):
    @bot.command(name="status")
    async def status(ctx):
        now = get_french_datetime()
        delta = now - startup_time

        days = delta.days
        hours, remainder = divmod(delta.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        uptime_str = f"{days}j {hours}h {minutes}min" if days else f"{hours}h {minutes}min"

        ping_ms = round(bot.latency * 1000)

        total_members = sum(guild.member_count for guild in bot.guilds)

        embed = discord.Embed(
            title="📊 Statut du bot",
            color=discord.Color.green()
        )

        embed.add_field(name="🟢 Uptime", value=uptime_str, inline=True)
        embed.add_field(name="📶 Ping", value=f"{ping_ms} ms", inline=True)
        embed.add_field(name="🏠 Serveurs",
                        value=f"{len(bot.guilds)}", inline=True)
        embed.add_field(name="👥 Utilisateurs",
                        value=f"{total_members}", inline=True)
        embed.add_field(name="🕒 Heure actuelle",
                        value=get_french_time_str(), inline=False)
        embed.add_field(name="🧩 Version", value=BOT_VERSION, inline=True)
        embed.add_field(name="📅 Date de démarrage",
                        value=startup_time.strftime("%d/%m/%Y %H:%M:%S"), inline=False)
        embed.set_footer(
            text=f"Requête par : {ctx.author}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)

        if DEBUG_MODE:
            embed.add_field(
                name="🐞 Mode debug", value="Activé" if DEBUG_MODE else "Désactivé", inline=True)

        await ctx.send(embed=embed)
