from discord.ext import commands
from utils.security import is_owner, get_owners


def setup(bot):
    @bot.command(name="listowners")
    async def list_owners(ctx):
        if not is_owner(ctx.author.id):
            await ctx.send("🚫 Tu n'as pas accès à cette commande.")
            return

        owners = get_owners()
        if not owners:
            await ctx.send("👥 Aucun owner enregistré.")
            return

        msg = "👥 Owners actuels :\n" + "\n".join(
            f"- {o['name']} ({o['id']})" for o in owners
        )
        await ctx.send(msg)
