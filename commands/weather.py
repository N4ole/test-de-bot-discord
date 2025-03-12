from discord.ext import commands
import requests
import os

API_KEY = "YOUR_OPENWEATHER_API_KEY"


class Weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def weather(self, ctx, *, city: str):
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url).json()

        if response["cod"] != 200:
            await ctx.send("❌ City not found!")
            return

        weather = response["weather"][0]["description"].capitalize()
        temp = response["main"]["temp"]
        await ctx.send(f"🌍 Weather in {city}: {weather}, 🌡 {temp}°C")


async def setup(bot):
    await bot.add_cog(Weather(bot))
