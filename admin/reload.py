import os
import sys
import importlib
import traceback
import discord
from discord.ext import commands
from utils.logger import send_log
from utils.security import is_owner


def setup(bot):
    @bot.command(name='reload')
    async def reload(ctx, command: str = None):
        if not is_owner(ctx.author.id):
            await ctx.send("🚫 Tu n'es pas autorisé à utiliser cette commande.")
            return

        base_path = os.path.join(os.path.dirname(__file__), "../commands")
        base_import = "commands"

        if command is None:
            reloaded = 0
            failed = []

            for filename in os.listdir(base_path):
                if filename.endswith(".py") and filename != "__init__.py":
                    cmd_name = filename[:-3]
                    module_name = f"{base_import}.{cmd_name}"
                    try:
                        # Supprime toutes les commandes de ce module
                        for cmd in list(bot.commands):
                            if cmd.callback.__module__ == module_name:
                                bot.remove_command(cmd.name)

                        if module_name in sys.modules:
                            del sys.modules[module_name]

                        module = importlib.import_module(module_name)
                        if hasattr(module, "setup"):
                            module.setup(bot)
                        reloaded += 1

                    except Exception as e:
                        traceback.print_exc()
                        failed.append((module_name, str(e)))

            await ctx.send(f"🔁 {reloaded} commandes rechargées.")
            print(
                f"[🔁] Reload global par {ctx.author} ({reloaded} OK, {len(failed)} erreurs)")

            desc = f"**Par :** {ctx.author.mention}\n**Commandes OK :** {reloaded}"
            if failed:
                desc += f"\n**Erreurs :** {len(failed)}\n```" + "\n".join(
                    [f"{name}: {err}" for name, err in failed]) + "```"

            await send_log(
                bot,
                ctx.guild.id,
                title="🔁 Rechargement des commandes",
                description=desc,
                color=discord.Color.orange()
            )

        else:
            module_name = f"{base_import}.{command}"
            try:
                # Supprime les commandes du module ciblé
                for cmd in list(bot.commands):
                    if cmd.callback.__module__ == module_name:
                        bot.remove_command(cmd.name)

                if module_name in sys.modules:
                    del sys.modules[module_name]

                module = importlib.import_module(module_name)
                if hasattr(module, "setup"):
                    module.setup(bot)

                await ctx.send(f"✅ Commande `{command}` rechargée.")
                print(f"[🔁] Reload {command}.py effectué par {ctx.author}")

                await send_log(
                    bot,
                    ctx.guild.id,
                    title=f"🔁 Rechargement : `{command}`",
                    description=f"**Par :** {ctx.author.mention}\n**Commande :** `{command}.py`",
                    color=discord.Color.orange()
                )

            except Exception as e:
                traceback.print_exc()
                await ctx.send(f"❌ Erreur lors du rechargement de `{command}`.")
                print(f"[❌] Échec reload {command}.py : {e}")

                await send_log(
                    bot,
                    ctx.guild.id,
                    title=f"❌ Erreur reload : `{command}`",
                    description=f"**Par :** {ctx.author.mention}\n```{e}```",
                    color=discord.Color.red()
                )
