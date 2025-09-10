import discord
from discord.ext import commands
import aiohttp
import os

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

# HARDCODED cookies and headers (from your curl)
HARDCODED_COOKIE_HEADER = (
    "_SplunkChallenge=MjEwLjIzLjIyNS4yMDI=; "
    "_SplunkChallengeHash=0nq9x3txgcyi; "
    "AUTH_TOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjExMjk2NDcyNTE4MDM4Nzc0OTgiLCJuYW1lIjoiX3g2NGRiZy5leGUiLCJleHAiOjE3NTgxMjAyNzh9.MO4QmEWVY1QZoYB9cbkipAGOpVq66u57Il_MMs5jwf8"
)

HEADERS = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json',
    'cookie': HARDCODED_COOKIE_HEADER,
    'origin': 'https://app.beamers.si',
    'priority': 'u=1, i',
    'referer': 'https://app.beamers.si/dashboard/bypasser',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest'
}


@bot.event
async def on_ready():
    print(f'✅ Logged in as {bot.user}')


@bot.command()
async def refreshcookie(ctx, *, cookie_input: str):
    """Refreshes cookie using hardcoded headers and user input."""
    url = 'https://app.beamers.si/api/bypasser'
    payload = {
        "action": "refresh_cookie",
        "cookie": cookie_input
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, headers=HEADERS, json=payload) as response:
                status = response.status
                text = await response.text()

                if status == 200:
                    await ctx.send(f"✅ Refreshed:\n```{text}```")
                else:
                    await ctx.send(f"❌ Failed (HTTP {status}):\n```{text}```")
        except Exception as e:
            await ctx.send(f"❌ Error:\n```{e}```")


# Run the bot
bot.run(os.getenv("DISCORD_BOT_TOKEN"))
