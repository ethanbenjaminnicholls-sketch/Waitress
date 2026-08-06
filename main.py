import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

import discord
from discord.ext import commands

# ==============================
# Keep Alive Server
# ==============================

class KeepAliveHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive!")

    def log_message(self, format, *args):
        return


def keep_alive():
    port = int(os.getenv("PORT", 3000))
    server = HTTPServer(("0.0.0.0", port), KeepAliveHandler)

    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    print(f"✅ Keep-alive running on port {port}")


# ==============================
# Bot Setup
# ==============================

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

WELCOME_CHANNEL_ID = 1534907292720435401


# ==============================
# Helper
# ==============================

def ordinal(n):
    if 10 <= (n % 100) <= 20:
        return f"{n}th"
    return f"{n}{ {1:'st',2:'nd',3:'rd'}.get(n % 10,'th') }"


async def send_welcome(member):
    guild = member.guild

    channel = guild.get_channel(WELCOME_CHANNEL_ID)

    if channel is None:
        try:
            channel = await guild.fetch_channel(WELCOME_CHANNEL_ID)
        except Exception:
            channel = guild.system_channel

    if channel is None:
        print("❌ No valid welcome channel found.")
        return

    await channel.send(
        f"👋 Welcome {member.mention} to **One More Day**!\n\n"
        f"You are our **{ordinal(guild.member_count)}** member! 🎉"
    )


# ==============================
# Events
# ==============================

@bot.event
async def on_ready():
    print("-" * 40)
    print(f"Logged in as {bot.user}")
    print(f"ID: {bot.user.id}")
    print(f"Discord.py: {discord.__version__}")
    print("-" * 40)

    for guild in bot.guilds:
        print(f"Connected to: {guild.name} ({guild.id})")


@bot.event
async def on_member_join(member):
    print(f"{member} joined {member.guild.name}")

    try:
        await send_welcome(member)
        print(f"Welcome sent to {member}")
    except Exception as e:
        print(f"Welcome error: {e}")


# ==============================
# Commands
# ==============================

@bot.command()
async def test(ctx):
    await ctx.send("✅ Bot is online!")


@bot.command()
async def welcome(ctx):
    try:
        await send_welcome(ctx.author)
        await ctx.send("✅ Welcome message sent.")
    except discord.Forbidden:
        await ctx.send("❌ I don't have permission to send messages there.")
    except discord.NotFound:
        await ctx.send("❌ Welcome channel not found.")
    except Exception as e:
        await ctx.send(f"❌ {e}")


@bot.command()
@commands.has_permissions(administrator=True)
async def ping(ctx):
    await ctx.send(f"🏓 Pong! `{round(bot.latency * 1000)}ms`")


# ==============================
# Main
# ==============================

def main():
    token = os.getenv("DISCORD_BOT_TOKEN")

    if token is None:
        raise RuntimeError("DISCORD_BOT_TOKEN environment variable is missing.")

    keep_alive()
    bot.run(token)


if __name__ == "__main__":
    main()
