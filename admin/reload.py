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

        folders = ["commands", "admin", "logs"]
        reloaded = 0
        failed = []

        # 🔁 Reload ALL
        if command is None:
            for folder in folders:
                folder_path = os.path.join(
                    os.path.dirname(__file__), f"../{folder}")
                for filename in os.listdir(folder_path):
                    if filename.endswith(".py") and filename != "__init__.py":
                        module_name = f"{folder}.{filename[:-3]}"
                        try:
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

        # 🔁 Reload spécifique
        else:
            found = False
            for folder in folders:
                module_name = f"{folder}.{command}"
                try:
                    for cmd in list(bot.commands):
                        if cmd.callback.__module__ == module_name:
                            bot.remove_command(cmd.name)

                    if module_name in sys.modules:
                        del sys.modules[module_name]

                    module = importlib.import_module(module_name)
                    if hasattr(module, "setup"):
                        module.setup(bot)

                    found = True
                    await ctx.send(f"✅ Commande `{command}` rechargée depuis `{folder}/`.")
                    print(f"[🔁] Reload {command}.py effectué par {ctx.author}")

                    await send_log(
                        bot,
                        ctx.guild.id,
                        title=f"🔁 Rechargement : `{command}`",
                        description=f"**Par :** {ctx.author.mention}\n**Commande :** `{folder}/{command}.py`",
                        color=discord.Color.orange()
                    )
                    break

                except Exception as e:
                    traceback.print_exc()
                    failed.append((module_name, str(e)))

            if not found:
                await ctx.send(f"❌ Erreur lors du rechargement de `{command}`.")
                print(f"[❌] Échec reload {command}.py")
                await send_log(
                    bot,
                    ctx.guild.id,
                    title=f"❌ Erreur reload : `{command}`",
                    description=f"**Par :** {ctx.author.mention}\n```{failed[-1][1]}```",
                    color=discord.Color.red()
                )
