import discord
from discord.ext import commands
from utils.logger import load_log_config, save_log_config
import os

CONFIG_PATH = os.path.join(os.path.dirname(
    __file__), "../data/log_config.json")


def setup(bot):
    @bot.command(name="logsetdefault")
    @commands.has_permissions(administrator=True)
    async def set_default_log(ctx):
        guild = ctx.guild
        guild_id = str(guild.id)
        config = load_log_config()

        # Vérifie si le salon existe déjà
        existing = discord.utils.get(guild.text_channels, name="logs-bot")
        if not existing:
            try:
                overwrites = {
                    guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    guild.me: discord.PermissionOverwrite(read_messages=True)
                }
                channel = await guild.create_text_channel("logs-bot", overwrites=overwrites)
                await ctx.send(f"✅ Salon `#logs-bot` créé et défini comme salon de log.")
            except Exception as e:
                await ctx.send(f"❌ Erreur lors de la création du salon : {e}")
                return
        else:
            channel = existing
            await ctx.send(f"📌 Le salon `#logs-bot` existe déjà. Il a été défini comme salon de log.")

        # Met à jour log_config.json
        config[guild_id] = {
            "channel_id": str(channel.id),
            "guild_name": guild.name,
            "channel_name": channel.name
        }
        save_log_config(config)

    @bot.command(name="logtest")
    @commands.has_permissions(administrator=True)
    async def log_test(ctx):
        from utils.logger import send_log

        await send_log(
            bot,
            ctx.guild.id,
            title="📋 Test du système de logs",
            description="Ceci est un message de test du système de logs.\nSi tu vois ce message, tout fonctionne correctement ✅",
            color=discord.Color.blurple()
        )

        await ctx.send("✅ Message de test envoyé au salon de logs.")
