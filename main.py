import discord
import asyncio
import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from discord.ext import commands

# ── Keep-alive server ──────────────────────────────────────────────────────
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
    print(f"[Keep-Alive] Running on port {port}")
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

# ── Bot ────────────────────────────────────────────────────────────────────
intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix="!", intents=intents)

WELCOME_CHANNEL_ID = 1529217305756827649

def ordinal(n):
    if 10 <= n % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"

@client.event
async def on_ready():
    print(f"✅ {client.user} is now online!")

@client.event
async def on_member_join(member):
    try:
        # fetch_channel works even if not cached
        channel = await client.fetch_channel(WELCOME_CHANNEL_ID)
        member_count = member.guild.member_count
        await channel.send(
            f"👋 Hi {member.mention}, welcome to One More Day!\n\n and welcome to the team"
            f"You are our **{ordinal(member_count)}** member. 🎉"
        )
        print(f"Welcomed {member} as the {ordinal(member_count)} member.")
    except Exception as e:
        print(f"Error sending welcome: {e}")

# ── Run ────────────────────────────────────────────────────────────────────
async def main():
    token = os.environ.get("DISCORD_BOT_TOKEN")
    if not token:
        raise ValueError("DISCORD_BOT_TOKEN is not set!")
    start_keep_alive()
