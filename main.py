import discord
import asyncio
import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from discord.ext import commands, tasks

# ── Keep-alive HTTP server (runs in background thread) ─────────────────────
class KeepAliveHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive!")

    def log_message(self, format, *args):
        pass  # silence HTTP request logs

def run_keep_alive():
    port = int(os.environ.get("PORT", 3000))
    server = HTTPServer(("0.0.0.0", port), KeepAliveHandler)
    print(f"[Keep-Alive] Server running on port {port}")
    server.serve_forever()

def start_keep_alive():
    thread = threading.Thread(target=run_keep_alive, daemon=True)
    thread.start()

# ── Bot setup ───────────────────────────────────────────────────────────────
intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix="!", intents=intents)

WELCOME_CHANNEL_ID = 1529217305756827649

# ── Ordinal helper: 1 → "1st", 26 → "26th" ─────────────────────────────────
def ordinal(n):
    if 10 <= n % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"

# ── Events ───────────────────────────────────────────────────────────────────
@client.event
async def on_ready():
    print(f"✅ {client.user} is now online!")

@client.event
async def on_member_join(member):
    try:
        channel = client.get_channel(WELCOME_CHANNEL_ID)

        if not channel:
            # Try fetching it directly if not in cache
            channel = await client.fetch_channel(WELCOME_CHANNEL_ID)

        if channel:
            member_count = member.guild.member_count
            await channel.send(
                f"👋 Hi {member.mention}, welcome to **One More Day**!\n\n"
                f"You are our **{ordinal(member_count)}** member. 🎉"
            )
            print(f"Welcomed {member} as the {ordinal(member_count)} member.")
    except Exception as e:
        print(f"Error in on_member_join: {e}")

@client.event
async def on_error(event, *args, **kwargs):
    print(f"Error in event {event}: {args}")

# ── Entry point ──────────────────────────────────────────────────────────────
async def main():
    token = os.environ.get("DISCORD_BOT_TOKEN")
    if not token:
        raise ValueError("DISCORD_BOT_TOKEN environment variable is not set!")

    # Start keep-alive server in background
    start_keep_alive()

    # Auto-reconnect loop
    while True:
        try:
            async with client:
                await client.start(token)
        except discord.errors.LoginFailure:
            print("❌ Invalid token — check your DISCORD_BOT_TOKEN variable.")
            break
        except Exception as e:
            print(f"⚠️ Bot crashed: {e} — reconnecting in 5 seconds...")
            await asyncio.sleep(5)

asyncio.run(main())
