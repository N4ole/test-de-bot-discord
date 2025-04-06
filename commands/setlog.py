from discord.ext import commands
from utils.logger import load_log_config, save_log_config


def setup(bot):
    @bot.command(name='setlog')
    @commands.has_permissions(administrator=True)
    async def setlog(ctx, channel: commands.TextChannelConverter):
        config = load_log_config()
        config[str(ctx.guild.id)] = str(channel.id)
        save_log_config(config)
        await ctx.send(f"📋 Salon de log défini sur {channel.mention}")
