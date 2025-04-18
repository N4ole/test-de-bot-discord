from discord.ext import commands


def setup(bot):
    @bot.command(name='help')
    async def help_command(ctx):
        help_text = """
📘 **Commandes disponibles :**

👤 **Utilitaires**
- `!hello` – Te salue
- `!ping` – Teste la latence du bot
- `!status` – Infos sur le bot (version, uptime, debug...)
- `!uptime` – Depuis combien de temps le bot tourne

🧹 **Modération**
- `!clear <nombre>` – Supprime des messages *(admin)*
- `!kick @user [raison]` – Expulse un membre *(admin)*
- `!ban @user [raison]` – Bannit un membre *(admin)*
- `!mute @user [raison]` – Empêche un membre de parler *(admin)*
- `!unmute @user` – Rétablit les permissions *(admin)*

🛡️ **Logs & sécurité**
- `!setlog #salon` – Définit le salon pour les logs *(admin)*

🧪 **Admin avancé** *(owner uniquement)*
- `!reload [commande]` – Recharge une commande
- `!debug [on/off]` – Active/désactive le mode debug
- `!listowners` – Liste les owners
- `!addowner @user` – Ajoute un owner
- `!removeowner @user` – Supprime un owner

💡 Tape une commande sans argument pour plus de détails.
"""
        await ctx.send(help_text)
