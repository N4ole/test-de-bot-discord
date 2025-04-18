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
            current = "Activé ✅" if get_debug_mode() else "Désactivé ❌"
            await ctx.send(f"🐞 Debug actuel : {current}\nUtilise `!debug on` ou `!debug off`")
            return

        new_state = (state == "on")
        set_debug_mode(new_state)
        await ctx.send(f"✅ Mode debug {'activé ✅' if new_state else 'désactivé ❌'}")

        # 🖥️ Log en console
        print(
            f"[🐞 DEBUG] Mode debug {'activé' if new_state else 'désactivé'} par {ctx.author} ({ctx.author.id})")
