from dotenv import load_dotenv
import os
from engine import run_bot

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

bot = run_bot()
bot.run(TOKEN)
