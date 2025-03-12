import dotenv
import os
from datetime import datetime
import json
import asyncio
import discord
from discord.ext import commands
import logging


dotenv.load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")


logging.basicConfig(level=logging.INFO)
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


def log_message(username, user_id, content, timestamp):
    log_entry = {
        "username": username,
        "user_id": user_id,
        "content": content,
        "timestamp": timestamp
    }

    if not os.path.exists("logs.json"):
        with open("logs.json", "w") as f:
            json.dump([], f, indent=4)

    with open("logs.json", "r") as f:
        logs = json.load(f)

    logs.append(log_entry)

    with open("logs.json", "w") as f:
        json.dump(logs, f, indent=4)


@bot.event
async def on_command(ctx):
    logging.info(
        f"🔹 Command Executed: {ctx.command} by {ctx.author} in #{ctx.channel}")


@bot.event
async def on_command_error(ctx, error):
    logging.error(f"❌ Error in command '{ctx.command}': {error}")
    await ctx.send(f"⚠️ Error: {error}")


async def load_cogs():
    for filename in os.listdir("./commands"):
        if filename.endswith(".py"):
            try:
                await bot.load_extension(f"commands.{filename[:-3]}")
                logging.info(f"✅ Loaded cog: {filename}")
            except Exception as e:
                logging.error(f"❌ Failed to load {filename}: {e}")


@bot.event
async def on_ready():
    logging.info(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")
    logging.info(f"📌 Bot is in {len(bot.guilds)} servers.")

    commands_list = [command.name for command in bot.commands]
    if not commands_list:
        logging.error("❌ No commands were loaded. Check your commands folder!")
    else:
        logging.info(f"📝 Loaded Commands: {commands_list}")

    print(f"\n✅ Bot is online as {bot.user}!\n")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    log_message(
        username=str(message.author),
        user_id=str(message.author.id),
        content=message.content,
        timestamp=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    )

    print(f"📩 Logged: {message.author} - {message.content}")

    await bot.process_commands(message)


async def main():
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)


asyncio.run(main())
