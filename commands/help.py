from discord.ext import commands


def setup(bot):
    @bot.command(name='help')
    async def help_command(ctx):
        help_text = """
📘 **Commandes disponibles** :

👋 `!hello` – Te salue
🏓 `!ping` – Teste la latence du bot

🧼 `!clear <nombre>` – Supprime des messages *(admin)*
👢 `!kick @user [raison]` – Kick un membre *(admin)*
🔨 `!ban @user [raison]` – Ban un membre *(admin)*
🔇 `!mute @user [raison]` – Empêche un membre d’écrire *(admin)*
🔊 `!unmute @user` – Rétablit les permissions *(admin)*
"""
        await ctx.send(help_text)
