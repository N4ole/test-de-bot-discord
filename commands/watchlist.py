import discord
from discord.ext import commands
import json
import os

WATCHLIST_FILE = "data/watchlist.json"


class Watchlist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.load_watchlist()

    def load_watchlist(self):
        """Charge la watchlist depuis le fichier JSON."""
        if not os.path.exists(WATCHLIST_FILE):
            with open(WATCHLIST_FILE, "w") as f:
                json.dump({}, f, indent=4)

        with open(WATCHLIST_FILE, "r") as f:
            self.watchlist = json.load(f)

    def save_watchlist(self):
        """Sauvegarde la watchlist dans le fichier JSON."""
        with open(WATCHLIST_FILE, "w") as f:
            json.dump(self.watchlist, f, indent=4)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def watchlist(self, ctx, member: discord.Member):
        """Ajoute un utilisateur à la watchlist et crée un salon privé."""
        guild_id = str(ctx.guild.id)
        user_id = str(member.id)

        if guild_id not in self.watchlist:
            self.watchlist[guild_id] = {}

        if user_id in self.watchlist[guild_id]:
            await ctx.send(f"⚠️ {member.mention} est déjà sur la watchlist.")
            return

        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            ctx.guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True),
        }

        for role in ctx.guild.roles:
            if role.permissions.administrator:
                overwrites[role] = discord.PermissionOverwrite(
                    view_channel=True)

        category = discord.utils.get(ctx.guild.categories, name="📌 Watchlist")
        if category is None:
            category = await ctx.guild.create_category("📌 Watchlist")

        watch_channel = await ctx.guild.create_text_channel(
            name=f"watch-{member.name}",
            category=category,
            overwrites=overwrites
        )

        self.watchlist[guild_id][user_id] = {
            "username": str(member),
            "channel_id": watch_channel.id
        }

        self.save_watchlist()
        await ctx.send(f"✅ {member.mention} a été ajouté à la watchlist et son activité sera enregistrée dans {watch_channel.mention}. 🔍")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unwatch(self, ctx, member: discord.Member):
        """Retire un utilisateur de la watchlist et supprime le salon associé."""
        guild_id = str(ctx.guild.id)
        user_id = str(member.id)

        if guild_id not in self.watchlist or user_id not in self.watchlist[guild_id]:
            await ctx.send(f"⚠️ {member.mention} n'est pas dans la watchlist.")
            return

        channel_id = self.watchlist[guild_id][user_id]["channel_id"]
        watch_channel = self.bot.get_channel(channel_id)
        if watch_channel:
            await watch_channel.delete()

        del self.watchlist[guild_id][user_id]
        self.save_watchlist()

        await ctx.send(f"❌ {member.mention} a été retiré de la watchlist et son salon de surveillance a été supprimé.")


async def setup(bot):
    await bot.add_cog(Watchlist(bot))
