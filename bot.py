import discord
from discord.ext import commands
import aiohttp
import os

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

# Store user cookies (per user ID, optional)
user_cookies = {}

@bot.event
async def on_ready():
    print(f'Bot is online as {bot.user}')

@bot.command()
async def updatecookie(ctx, *, cookie: str):
    user_id = str(ctx.author.id)
    user_cookies[user_id] = cookie
    await ctx.send("✅ Cookie saved successfully.")

@bot.command()
async def refreshcookie(ctx, *, cookie_input: str):
    user_id = str(ctx.author.id)

    if user_id not in user_cookies:
        await ctx.send("⚠️ You haven't set your cookie. Use `!updatecookie <cookie>` first.")
        return

    # Prepare headers and body
    headers = {
        'accept': '*/*',
        'content-type': 'application/json',
        'cookie': user_cookies[user_id],  # full cookie string
        'origin': 'https://app.beamers.si',
        'referer': 'https://app.beamers.si/dashboard/bypasser',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    payload = {
        "action": "refresh_cookie",
        "cookie": cookie_input  # user-provided input
    }

    url = 'https://app.beamers.si/api/bypasser'

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, headers=headers, json=payload) as response:
                status = response.status
                data = await response.text()
                if status == 200:
                    await ctx.send(f"✅ Cookie refresh successful.\nResponse: ```{data}```")
                else:
                    await ctx.send(f"❌ Refresh failed. HTTP Status: {status}\nResponse: ```{data}```")
        except Exception as e:
            await ctx.send(f"❌ Error occurred: {e}")

bot.run(os.getenv("DISCORD_BOT_TOKEN"))
