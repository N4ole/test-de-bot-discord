from discord.ext import commands
from utils.security import is_owner, add_owner, PROTECTED_OWNER_ID
from utils.time import get_french_datetime as get_french_time
import discord


def setup(bot):
    @bot.command(name="addowner")
    async def add_owner_cmd(ctx, user: commands.MemberConverter):
        if not is_owner(ctx.author.id):
            await ctx.send("🚫 Tu ne peux pas modifier la liste des owners.")
            return

        if user.bot:
            await ctx.send("🚫 Impossible d’ajouter un **bot** comme owner !")
            return

        if add_owner(user.id, user.name, user.bot):
            await ctx.send(f"✅ `{user.name}` a été ajouté comme owner.")

            # 📨 MP au boss
            try:
                boss = await bot.fetch_user(PROTECTED_OWNER_ID)
                embed = discord.Embed(
                    title="👤 Nouveau owner ajouté",
                    description=(
                        f"Un utilisateur a été ajouté à la liste des owners.\n\n"
                        f"**Ajouté par :** {ctx.author} (`{ctx.author.id}`)\n"
                        f"**Nouveau owner :** {user} (`{user.id}`)\n"
                        f"**Serveur :** {ctx.guild.name} (`{ctx.guild.id}`)\n"
                        f"**Quand :** `{get_french_time()}`"
                    ),
                    color=discord.Color.green()
                )
                await boss.send(embed=embed)
            except Exception as e:
                print(f"[❌] Erreur lors de l’envoi du MP owner ajouté : {e}")

        else:
            await ctx.send(f"ℹ️ `{user.name}` est déjà owner ou action interdite.")
