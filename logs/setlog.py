import discord
from discord.ext import commands
import json
import os

CONFIG_PATH = os.path.join(os.path.dirname(
    __file__), "../data/log_config.json")


def setup(bot):
    @bot.command(name="setlog")
    @commands.has_permissions(administrator=True)
    async def setlog(ctx, channel: discord.TextChannel):
        guild_id = str(ctx.guild.id)
        log_entry = {
            "channel_id": str(channel.id),
            "guild_name": ctx.guild.name,
            "channel_name": channel.name
        }

        # Charger la config existante
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, "r") as f:
                config = json.load(f)
        else:
            config = {}

        config[guild_id] = log_entry

        with open(CONFIG_PATH, "w") as f:
            json.dump(config, f, indent=2)

        await ctx.send(f"✅ Salon de log défini sur {channel.mention} pour ce serveur.")
