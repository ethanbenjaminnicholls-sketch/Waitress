import discord
import asyncio
import os
from discord.ext import commands

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
    print(f"{client.user} is now online!")


@client.event
async def on_member_join(member):
    channel = client.get_channel(WELCOME_CHANNEL_ID)

    if channel:
        member_count = member.guild.member_count

        await channel.send(
            f"👋 Hi {member.mention}, welcome to **One More Day**!\n\n"
            f"You are our **{ordinal(member_count)}** member. 🎉"
        )


async def main():
    token = os.environ.get("DISCORD_BOT_TOKEN")
    if not token:
        raise ValueError("DISCORD_BOT_TOKEN secret is not set!")
    async with client:
        await client.start(token)


asyncio.run(main())
