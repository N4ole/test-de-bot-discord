import discord
from discord.ext import commands
import json
import os

WATCHLIST_FILE = "watchlist.json"


class Watchlist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.watchlist = self.load_watchlist()

    def load_watchlist(self):
        if os.path.exists(WATCHLIST_FILE):
            with open(WATCHLIST_FILE, "r") as f:
                return json.load(f)
        return []

    def save_watchlist(self):
        with open(WATCHLIST_FILE, "w") as f:
            json.dump(self.watchlist, f, indent=4)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def watchlist(self, ctx, action: str, member: discord.Member = None):
        """Ajoute, retire ou affiche la liste des utilisateurs surveillés."""

        if action.lower() == "add":
            if not member:
                await ctx.send("❌ Spécifiez un utilisateur à surveiller.")
                return
            if member.id in self.watchlist:
                await ctx.send(f"⚠️ {member.mention} est **déjà** surveillé.")
                return

            self.watchlist.append(member.id)
            self.save_watchlist()
            await ctx.send(f"👀 {member.mention} a été **ajouté** à la watchlist.")

        elif action.lower() == "remove":
            if not member:
                await ctx.send("❌ Spécifiez un utilisateur à retirer de la watchlist.")
                return
            if member.id not in self.watchlist:
                await ctx.send(f"⚠️ {member.mention} **n'est pas** sur la watchlist.")
                return

            self.watchlist.remove(member.id)
            self.save_watchlist()
            await ctx.send(f"✅ {member.mention} a été **retiré** de la watchlist.")

        elif action.lower() == "list":
            if not self.watchlist:
                await ctx.send("📜 La watchlist est **vide**.")
                return

            user_list = [f"<@{user_id}>" for user_id in self.watchlist]
            await ctx.send(f"👀 **Utilisateurs surveillés :**\n" + "\n".join(user_list))

        else:
            await ctx.send("❌ Commande invalide. Utilisez : `!watchlist add @user`, `!watchlist remove @user` ou `!watchlist list`.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return  # Ignore les bots

        if message.author.id in self.watchlist:
            log_channel = discord.utils.get(
                message.guild.text_channels, name="watchlist-logs")

            if log_channel:
                embed = discord.Embed(
                    title="👀 Message Surveillé",
                    description=f"**Auteur :** {message.author.mention}\n**Salon :** {message.channel.mention}",
                    color=discord.Color.red()
                )
                embed.add_field(name="💬 Message :",
                                value=message.content, inline=False)
                embed.set_footer(text=f"ID : {message.author.id}")

                await log_channel.send(embed=embed)
            else:
                print(
                    f"⚠️ Aucun salon `watchlist-logs` trouvé pour surveiller {message.author}.")


async def setup(bot):
    await bot.add_cog(Watchlist(bot))
