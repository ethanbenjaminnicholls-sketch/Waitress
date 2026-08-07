import discord
import asyncio
import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from discord.ext import commands

# Keep-alive server so Railway stays online 24/7
class KeepAliveHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive!")
    def log_message(self, format, *args):
        pass

def start_keep_alive():
    port = int(os.environ.get("PORT", 3000))
    server = HTTPServer(("0.0.0.0", port), KeepAliveHandler)
    print(f"Keep-alive running on port {port}")
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

# Bot setup
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

client = commands.Bot(command_prefix="!", intents=intents)

WELCOME_CHANNEL_ID = 1534907292720435401

def ordinal(n):
    if 10 <= n % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.command()
async def test(ctx):
    await ctx.send("Bot is online!")

@client.event
async def on_member_join(member):
    print(f"{member} joined {member.guild.name}")
    try:
        guild = member.guild
        channel = guild.get_channel(WELCOME_CHANNEL_ID) or await guild.fetch_channel(WELCOME_CHANNEL_ID)
        member_count = guild.member_count
        await channel.send(
            f"👋 Hi {member.mention}, welcome to **One More Day**!\n\n"
            f"You are our **{ordinal(member_count)}** member. 🎉"
        )
        print(f"Welcomed {member} as the {ordinal(member_count)} member.")
    except Exception as e:
        print(f"Error welcoming {member}: {e}")

async def main():
    token = os.environ.get("DISCORD_BOT_TOKEN")
    if not token:
        raise ValueError("DISCORD_BOT_TOKEN is not set!")
    start_keep_alive()
    while True:
        try:
            async with client:
                await client.start(token)
        except discord.errors.LoginFailure:
            print("Invalid token — check DISCORD_BOT_TOKEN.")
            break
        except Exception as e:
            print(f"Crashed: {e} — reconnecting in 5 seconds...")
            await asyncio.sleep(5)

asyncio.run(main())
