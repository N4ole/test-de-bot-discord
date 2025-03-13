import discord
from discord.ext import commands
import os
import dotenv


class LogsConfig(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ✅ Commande pour changer les salons logs
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setlog(self, ctx, log_type: str = None, channel: discord.TextChannel = None):
        """
        Change le salon log pour `sent`, `deleted` ou `edited`.
        Usage : !setlog sent #log-salon
        """
        log_types = {
            "sent": "LOGS_SENT_CHANNEL_ID",
            "deleted": "LOGS_DELETED_CHANNEL_ID",
            "edited": "LOGS_EDITED_CHANNEL_ID"
        }

        # Vérification des arguments
        if log_type not in log_types:
            await ctx.send("❌ Usage: `!setlog [sent/deleted/edited] #salon`")
            return

        if channel is None:
            await ctx.send("❌ Veuillez mentionner un salon valide. Exemple: `!setlog sent #logs-envoyés`")
            return

        # Modifier la valeur dans .env
        env_file = ".env"
        lines = []
        if os.path.exists(env_file):
            with open(env_file, "r") as f:
                lines = f.readlines()

        with open(env_file, "w") as f:
            found = False
            for line in lines:
                if line.startswith(log_types[log_type]):
                    f.write(f"{log_types[log_type]}={channel.id}\n")
                    found = True
                else:
                    f.write(line)
            if not found:
                f.write(f"{log_types[log_type]}={channel.id}\n")

        # ✅ Recharger les variables d'environnement après modification
        dotenv.load_dotenv()

        # ✅ Mise à jour des variables dans `os.environ`
        os.environ[log_types[log_type]] = str(channel.id)

        await ctx.send(f"✅ Le salon des logs `{log_type}` a été changé en {channel.mention}")

    # ✅ Commande pour effacer les logs
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def clearlogs(self, ctx, log_type: str = None):
        """
        Supprime les logs de `sent`, `deleted` ou `edited`.
        Usage : !clearlogs sent
        """
        log_files = {
            "sent": "logs_sent.json",
            "deleted": "logs_deleted.json",
            "edited": "logs_edited.json"
        }

        if log_type not in log_files:
            await ctx.send("❌ Usage: `!clearlogs [sent/deleted/edited]`")
            return

        file_path = log_files[log_type]

        # Vérifier si le fichier existe
        if os.path.exists(file_path):
            with open(file_path, "w") as f:
                f.write("[]")  # Écrire un fichier JSON vide
            await ctx.send(f"🗑️ Les logs `{log_type}` ont été supprimés.")
        else:
            await ctx.send(f"⚠️ Aucun fichier de logs `{log_type}` trouvé.")


# ✅ Fonction pour charger le cog
async def setup(bot):
    await bot.add_cog(LogsConfig(bot))
