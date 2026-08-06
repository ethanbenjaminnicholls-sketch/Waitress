# Onemoreday Welcome Bot 🎉

A Discord welcome bot that greets new members with their member number (e.g. "You are our 26th member!").

---

## Features
- Mentions the new member by name
- Shows which numbered member they are (1st, 2nd, 3rd… 26th, etc.)
- Sends a rich embed to your `#welcome` channel (or system channel as fallback)
- Built-in keep-alive HTTP server so it stays running on Railway.app

---

## Setup

### 1. Create a Discord Bot
1. Go to [discord.com/developers/applications](https://discord.com/developers/applications)
2. Click **New Application** → give it a name → go to **Bot**
3. Click **Reset Token** and copy your token
4. Under **Privileged Gateway Intents**, enable **Server Members Intent**
5. Go to **OAuth2 → URL Generator**, select scopes: `bot`  
   Permissions: `Send Messages`, `Embed Links`, `View Channels`
6. Open the generated URL and invite the bot to your server

### 2. Deploy to Railway.app

**Via GitHub (recommended):**
1. Push this project to a GitHub repo
2. Go to [railway.app](https://railway.app) → **New Project** → **Deploy from GitHub repo**
3. Select your repo
4. Go to **Variables** and add:
   ```
   DISCORD_TOKEN = your_token_here
   ```
5. Railway will auto-deploy. Your bot is live! ✅

**Environment Variables needed on Railway:**
| Variable | Description |
|---|---|
| `DISCORD_TOKEN` | Your Discord bot token (keep this secret!) |
| `WELCOME_CHANNEL_ID` | The channel to post welcome messages in (default: `1534907292720435401`) |

---

## How it works

When a member joins your Discord server, the bot sends a message like:

> 👋 **Welcome to Onemoreday!**  
> Hey @Username, welcome to **Onemoreday**!  
> You are our **26th member** 🎉  
> We're glad to have you here. Enjoy your stay!

The bot posts to a channel named `#welcome` if it exists, otherwise falls back to the server's system channel.
