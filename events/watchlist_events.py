import discord
from discord.ext import commands
import json
import os


WATCHLIST_FILE = "data/watchlist.json"


class WatchlistEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def load_watchlist(self):
        """Charge la watchlist depuis le fichier JSON."""
        if os.path.exists(WATCHLIST_FILE):
            with open(WATCHLIST_FILE, "r") as f:
                return json.load(f)
        return {}

    @commands.Cog.listener()
    async def on_message(self, message):
        """Log tous les messages envoyés par un utilisateur surveillé."""
        if message.author.bot:
            return

        watchlist = self.load_watchlist()
        guild_id = str(message.guild.id)
        user_id = str(message.author.id)

        if guild_id in watchlist and user_id in watchlist[guild_id]:
            channel_id = watchlist[guild_id][user_id]["channel_id"]
            watch_channel = self.bot.get_channel(channel_id)

            if watch_channel:
                embed = discord.Embed(
                    title="📩 Message envoyé",
                    description=f"**{message.author}** a envoyé un message dans {message.channel.mention}",
                    color=discord.Color.orange()
                )
                embed.add_field(
                    name="💬 Contenu", value=message.content or "*Aucun texte*", inline=False)
                embed.set_footer(
                    text=f"🕒 {discord.utils.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")

                if message.attachments:
                    embed.add_field(
                        name="📷 Pièces jointes",
                        value="\n".join(
                            [att.url for att in message.attachments]),
                        inline=False
                    )

                await watch_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        """Log les connexions et déconnexions des salons vocaux."""
        watchlist = self.load_watchlist()
        guild_id = str(member.guild.id)
        user_id = str(member.id)

        if guild_id in watchlist and user_id in watchlist[guild_id]:
            channel_id = watchlist[guild_id][user_id]["channel_id"]
            watch_channel = self.bot.get_channel(channel_id)

            if watch_channel:
                embed = discord.Embed(color=discord.Color.blue())
                embed.set_footer(
                    text=f"🕒 {discord.utils.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")

                if before.channel is None and after.channel is not None:

                    embed.title = "🔊 Connexion vocale"
                    embed.description = f"**{member}** a rejoint le salon vocal `{after.channel.name}`."

                elif before.channel is not None and after.channel is None:
                    embed.title = "🔇 Déconnexion vocale"
                    embed.description = f"**{member}** a quitté le salon vocal `{before.channel.name}`."

                elif before.channel != after.channel:
                    embed.title = "🔁 Changement de salon vocal"
                    embed.description = f"**{member}** est passé de `{before.channel.name}` à `{after.channel.name}`."
                else:
                    return
                await watch_channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(WatchlistEvents(bot))
