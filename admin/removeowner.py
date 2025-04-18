from discord.ext import commands
from utils.security import is_owner, remove_owner, PROTECTED_OWNER_ID
from utils.time import get_french_datetime as get_french_time

import discord


def setup(bot):
    @bot.command(name="removeowner")
    async def remove_owner_cmd(ctx, user: commands.MemberConverter):
        if not is_owner(ctx.author.id):
            await ctx.send("🚫 Tu ne peux pas modifier la liste des owners.")
            return

        if user.id == PROTECTED_OWNER_ID:
            await ctx.send("🚫 Impossible de supprimer le boss suprême !")

            # 📨 Envoie un MP à l'owner protégé
            try:
                owner_user = await bot.fetch_user(PROTECTED_OWNER_ID)
                attempt_time = get_french_time()

                embed = discord.Embed(
                    title="⚠️ Tentative de suppression détectée",
                    description=(
                        f"Quelqu’un a tenté de te retirer de la liste des owners.\n\n"
                        f"**Auteur :** {ctx.author} (`{ctx.author.id}`)\n"
                        f"**Commande :** `!removeowner {user}`\n"
                        f"**Quand :** `{attempt_time}`\n"
                        f"**Serveur :** {ctx.guild.name} (`{ctx.guild.id}`)"
                    ),
                    color=discord.Color.red()
                )
                await owner_user.send(embed=embed)
            except Exception as e:
                print(f"[❌] Impossible d’envoyer le MP de protection : {e}")

            return

        if remove_owner(user.id):
            await ctx.send(f"✅ `{user.name}` a été retiré des owners.")
        else:
            await ctx.send(f"ℹ️ `{user.name}` n'était pas dans la liste.")
