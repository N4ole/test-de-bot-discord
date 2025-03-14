import discord
from discord.ext import commands
import asyncio


class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help_command(self, ctx, command_name: str = None):
        """Affiche l'aide générale ou les détails d'une commande spécifique."""

        if command_name:
            command = self.bot.get_command(command_name)
            if command:
                embed = discord.Embed(
                    title=f"📖 Détails de `!{command.name}`",
                    description=command.help or "Aucune description disponible.",
                    color=discord.Color.green()
                )
                await ctx.send(embed=embed)
            else:
                await ctx.send("❌ Commande introuvable. Utilisez `!help` pour voir la liste des commandes.")
            return

        # ✅ Générer les pages d'aide
        pages = []
        for cog_name, cog in self.bot.cogs.items():
            commands_list = [
                f"**`!{command.name}`** - {command.help or 'Pas de description'}"
                for command in cog.get_commands()
            ]
            if commands_list:
                embed = discord.Embed(
                    title=f"📜 Aide - {cog_name}",
                    description="\n".join(commands_list),
                    color=discord.Color.blue()
                )
                pages.append(embed)

        if not pages:
            await ctx.send("❌ Aucune commande disponible.")
            return

        # ✅ Gérer la pagination
        current_page = 0
        total_pages = len(pages)

        # Ajout de l'indicateur de page X / Y
        def update_footer():
            pages[current_page].set_footer(
                text=f"Page {current_page + 1} / {total_pages} • Utilisez ◀️ et ▶️ pour naviguer")

        update_footer()  # Initialisation
        message = await ctx.send(embed=pages[current_page])

        # Ajouter les réactions
        await message.add_reaction("◀️")
        await message.add_reaction("▶️")

        def check(reaction, user):
            return user == ctx.author and reaction.message.id == message.id and reaction.emoji in ["◀️", "▶️"]

        while True:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=60.0, check=check)
                if reaction.emoji == "▶️" and current_page < total_pages - 1:
                    current_page += 1
                    update_footer()
                    await message.edit(embed=pages[current_page])
                elif reaction.emoji == "◀️" and current_page > 0:
                    current_page -= 1
                    update_footer()
                    await message.edit(embed=pages[current_page])

                await message.remove_reaction(reaction, user)

            except asyncio.TimeoutError:
                await message.clear_reactions()
                break


async def setup(bot):
    await bot.add_cog(HelpCommand(bot))
