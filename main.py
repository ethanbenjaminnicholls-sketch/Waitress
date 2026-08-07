import discord
import asyncio
import os
from aiohttp import web

WELCOME_CHANNEL_ID = 1534907292720435401

def ordinal(n):
    if 10 <= n % 100 <= 20:
        return f"{n}th"
    return f"{n}{['th','st','nd','rd'][n%10] if n%10 <= 3 else 'th'}"

class WelcomeBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        super().__init__(intents=intents)

    async def on_ready(self):
        print(f"Online: {self.user}")

    async def on_member_join(self, member):
        print(f"Joined: {member}")
        try:
            channel = member.guild.get_channel(WELCOME_CHANNEL_ID) \
                      or await member.guild.fetch_channel(WELCOME_CHANNEL_ID)
            await channel.send(
                f"👋 Hi {member.mention}, welcome to **One More Day**!\n\n"
                f"You are our **{ordinal(member.guild.member_count)}** member. 🎉"
            )
        except Exception as e:
            print(f"Error: {e}")

async def run_web():
    async def handle(request):
        return web.Response(text="alive")
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", int(os.environ.get("PORT", 3000)))
    await site.start()
    print(f"Web server on port {os.environ.get('PORT', 3000)}")

async def main():
    token = os.environ.get("DISCORD_BOT_TOKEN")
    if not token:
        raise ValueError("DISCORD_BOT_TOKEN not set")
    bot = WelcomeBot()
    await run_web()
    await bot.start(token)

asyncio.run(main())
