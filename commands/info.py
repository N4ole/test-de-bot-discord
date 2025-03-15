from discord.ext import commands
import discord
import datetime
import platform


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def userinfo(self, ctx, member: discord.Member = None):
        """Affiche des informations détaillées sur un membre"""
        member = member or ctx.author

        embed = discord.Embed(
            title=f"📌 Informations sur {member}",
            color=discord.Color.blue(),
            timestamp=datetime.datetime.utcnow()
        )
        embed.set_thumbnail(url=member.avatar.url)
        embed.add_field(name="🆔 ID", value=member.id, inline=True)
        embed.add_field(name="📛 Nom d'utilisateur",
                        value=member.name, inline=True)
        embed.add_field(name="🏷️ Pseudo",
                        value=member.display_name, inline=True)
        embed.add_field(name="📅 Compte créé le", value=member.created_at.strftime(
            "%d/%m/%Y"), inline=True)
        embed.add_field(name="📆 A rejoint le serveur",
                        value=member.joined_at.strftime("%d/%m/%Y"), inline=True)
        embed.add_field(name="🎭 Rôles", value=", ".join(
            [role.mention for role in member.roles if role != ctx.guild.default_role]) or "Aucun", inline=False)

        # Ajoute des statistiques (nécessite un tracking des logs/messages/vocaux)
        embed.add_field(name="💬 Messages envoyés",
                        value="🔄 Tracking nécessaire", inline=True)
        embed.add_field(name="🎙️ Temps en vocal",
                        value="🔄 Tracking nécessaire", inline=True)

        embed.set_footer(
            text=f"Demandé par {ctx.author.name}", icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @commands.command()
    async def serverinfo(self, ctx):
        """Affiche les informations du serveur"""
        guild = ctx.guild

        embed = discord.Embed(
            title=f"🌍 Informations du serveur : {guild.name}",
            color=discord.Color.green(),
            timestamp=datetime.datetime.utcnow()
        )
        embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
        embed.add_field(name="🆔 ID", value=guild.id, inline=True)
        embed.add_field(name="👑 Propriétaire", value=guild.owner, inline=True)
        embed.add_field(name="📅 Créé le", value=guild.created_at.strftime(
            "%d/%m/%Y"), inline=True)
        embed.add_field(name="👥 Nombre de membres",
                        value=guild.member_count, inline=True)
        embed.add_field(name="💬 Nombre de salons", value=len(
            guild.text_channels), inline=True)
        embed.add_field(name="🔊 Nombre de salons vocaux",
                        value=len(guild.voice_channels), inline=True)
        embed.add_field(name="📜 Nombre de rôles",
                        value=len(guild.roles), inline=True)

        embed.set_footer(
            text=f"Demandé par {ctx.author.name}", icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @commands.command()
    async def avatar(self, ctx, member: discord.Member = None):
        """Affiche l'avatar d'un membre"""
        member = member or ctx.author

        embed = discord.Embed(
            title=f"🖼️ Avatar de {member}",
            color=discord.Color.purple()
        )
        embed.set_image(url=member.avatar.url)
        embed.set_footer(
            text=f"Demandé par {ctx.author.name}", icon_url=ctx.author.avatar.url)

        await ctx.send(embed=embed)

    @commands.command()
    async def botinfo(self, ctx):
        """Affiche les informations du bot"""
        bot_user = self.bot.user
        embed = discord.Embed(
            title="🤖 Informations du Bot",
            color=discord.Color.gold(),
            timestamp=datetime.datetime.utcnow()
        )
        if bot_user.avatar:
            embed.set_thumbnail(url=bot_user.avatar.url)

        embed.add_field(name="📛 Nom", value=bot_user.name, inline=True)
        embed.add_field(name="🆔 ID", value=bot_user.id, inline=True)
        embed.add_field(name="📅 Créé le", value=bot_user.created_at.strftime(
            "%d/%m/%Y"), inline=True)
        embed.add_field(
            name="🌐 Serveurs", value=f"Présent sur {len(self.bot.guilds)} serveurs", inline=True)
        embed.add_field(name="👥 Utilisateurs suivis", value=sum(
            g.member_count for g in self.bot.guilds), inline=True)
        embed.add_field(name="💾 Python",
                        value=platform.python_version(), inline=True)
        embed.add_field(name="🖥️ discord.py",
                        value=discord.__version__, inline=True)

        embed.set_footer(
            text=f"Demandé par {ctx.author.name}",
            icon_url=ctx.author.avatar.url if ctx.author.avatar else None
        )

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Info(bot))
