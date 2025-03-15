import discord
from discord.ext import commands
import json
import os
from datetime import datetime

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

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        """Log les événements vocaux (mute, deaf, changement de canal, etc.) pour les utilisateurs surveillés."""
        guild_id = str(member.guild.id)
        user_id = str(member.id)

        if guild_id not in self.watchlist or user_id not in self.watchlist[guild_id]:
            return

        channel_id = self.watchlist[guild_id][user_id]["channel_id"]
        watch_channel = self.bot.get_channel(channel_id)
        if not watch_channel:
            return

        embed = discord.Embed(
            title="🎙️ Surveillance vocale",
            color=discord.Color.purple(),
            timestamp=datetime.utcnow()
        )
        embed.set_author(
            name=member.name, icon_url=member.avatar.url if member.avatar else discord.Embed.Empty)

        # Détection des actions vocales
        if before.channel is None and after.channel is not None:
            embed.description = f"🔊 **{member.mention}** a rejoint **{after.channel.name}**"
        elif before.channel is not None and after.channel is None:
            embed.description = f"🔇 **{member.mention}** a quitté **{before.channel.name}**"
        elif before.channel != after.channel:
            embed.description = f"🔁 **{member.mention}** est passé de **{before.channel.name}** à **{after.channel.name}**"

        # Détection du mute / unmute
        if before.self_mute != after.self_mute:
            if after.self_mute:
                embed.description = f"🔕 **{member.mention}** s'est muté"
            else:
                embed.description = f"🔊 **{member.mention}** s'est démuté"

        # Détection du deaf / undeaf
        if before.self_deaf != after.self_deaf:
            if after.self_deaf:
                embed.description = f"🔇 **{member.mention}** s'est rendu sourd"
            else:
                embed.description = f"🔉 **{member.mention}** a réactivé le son"

        # Détection du mute administrateur
        if before.mute != after.mute:
            if after.mute:
                embed.description = f"⚠️ **{member.mention}** a été muté par un administrateur"
            else:
                embed.description = f"✅ **{member.mention}** a été démuté par un administrateur"

        # Détection du deaf administrateur
        if before.deaf != after.deaf:
            if after.deaf:
                embed.description = f"⚠️ **{member.mention}** a été rendu sourd par un administrateur"
            else:
                embed.description = f"✅ **{member.mention}** a été réactivé par un administrateur"

        # Envoi du log uniquement si une action a été détectée
        if embed.description:
            await watch_channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Watchlist(bot))
