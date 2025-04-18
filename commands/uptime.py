from discord.ext import commands
from utils.time import get_french_datetime
from engine import startup_time


def setup(bot):
    @bot.command(name='uptime')
    async def uptime(ctx):
        now = get_french_datetime()
        delta = now - startup_time

        days = delta.days
        hours, remainder = divmod(delta.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        parts = []
        if days:
            parts.append(f"{days} jour{'s' if days > 1 else ''}")
        if hours:
            parts.append(f"{hours} heure{'s' if hours > 1 else ''}")
        if minutes:
            parts.append(f"{minutes} minute{'s' if minutes > 1 else ''}")
        if not parts:
            parts.append("moins d'une minute")

        await ctx.send(f"🟢 Je suis en ligne depuis : **{' et '.join(parts)}**.")
