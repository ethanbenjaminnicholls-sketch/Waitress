const { Client, GatewayIntentBits, EmbedBuilder } = require('discord.js');

// ── Keep-alive server + self-ping (keeps bot online 24/7 on Railway) ────────
require('./keep_alive');

// ── Global crash guards ─────────────────────────────────────────────────────
process.on('unhandledRejection', (err) => {
  console.error('Unhandled promise rejection:', err);
});
process.on('uncaughtException', (err) => {
  console.error('Uncaught exception:', err);
});

// ── Discord client ──────────────────────────────────────────────────────────
const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMembers,
  ],
});

// ── Ordinal helper: 1 → "1st", 2 → "2nd", 26 → "26th" ─────────────────────
function ordinal(n) {
  const s = ['th', 'st', 'nd', 'rd'];
  const v = n % 100;
  return n + (s[(v - 20) % 10] || s[v] || s[0]);
}

// ── Welcome event ───────────────────────────────────────────────────────────
client.on('guildMemberAdd', async (member) => {
  try {
    const memberCount = member.guild.memberCount;
    const WELCOME_CHANNEL_ID = process.env.WELCOME_CHANNEL_ID || '1534907292720435401';

    // Fetch the channel directly (more reliable than cache.get)
    const welcomeChannel = await client.channels.fetch(WELCOME_CHANNEL_ID).catch(() => null);

    if (!welcomeChannel) {
      console.warn(`Welcome channel ${WELCOME_CHANNEL_ID} not found.`);
      return;
    }

    // Get avatar URL — discord.js v14 syntax
    const avatarURL = member.user.displayAvatarURL({ size: 256 });

    const embed = new EmbedBuilder()
      .setColor(0x5865f2)
      .setTitle('👋 Welcome to Onemoreday!')
      .setDescription(
        `Hey ${member}, welcome to **Onemoreday**!\n` +
        `You are our **${ordinal(memberCount)} member** 🎉\n\n` +
        `We're glad to have you here. Enjoy your stay!`
      )
      .setThumbnail(avatarURL)
      .setFooter({ text: 'Onemoreday • Welcome System' })
      .setTimestamp();

    await welcomeChannel.send({ embeds: [embed] });
    console.log(`Welcomed ${member.user.tag} as the ${ordinal(memberCount)} member.`);

  } catch (err) {
    console.error('Error in guildMemberAdd:', err);
  }
});

// ── Ready ───────────────────────────────────────────────────────────────────
client.once('ready', () => {
  console.log(`✅ Logged in as ${client.user.tag}`);
  console.log(`Watching for new members...`);
});

// ── Login ───────────────────────────────────────────────────────────────────
const token = process.env.DISCORD_TOKEN;
if (!token) {
  console.error('ERROR: DISCORD_TOKEN environment variable is not set.');
  process.exit(1);
}

client.login(token).catch((err) => {
  console.error('Failed to log in:', err.message);
  process.exit(1);
});
