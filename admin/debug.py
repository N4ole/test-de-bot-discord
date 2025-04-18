from discord.ext import commands
from utils.config import get_debug_mode, set_debug_mode
from utils.security import is_owner


def setup(bot):
    @bot.command(name="debug")
    async def toggle_debug(ctx, state: str = None):
        if not is_owner(ctx.author.id):
            await ctx.send("🚫 Tu n'es pas autorisé à utiliser cette commande.")
            return

        if state not in ["on", "off"]:
            await ctx.send(f"🐞 Debug actuel : {'Activé' if get_debug_mode() else 'Désactivé'}\nUtilise `!debug on` ou `!debug off`")
            return

        set_debug_mode(state == "on")
        await ctx.send(f"✅ Debug {'activé' if state == 'on' else 'désactivé'} !")
