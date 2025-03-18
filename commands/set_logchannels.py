import discord
from discord.ext import commands
from config import save_log_channel


async def setup(bot):
    @commands.has_permissions(administrator=True)
    @bot.command(name='setlog')
    async def set_log(ctx, log_type: str, channel: discord.TextChannel):
        log_type = log_type.lower()
        valid_types = ['message', 'edit', 'delete', 'voice']

        if log_type not in valid_types:
            await ctx.send(f"❌ Type invalide. Types valides : {', '.join(valid_types)}")
            return

        save_log_channel(log_type, channel.id)
        await ctx.send(f"✅ Log type **{log_type}** sera envoyé dans {channel.mention}")
