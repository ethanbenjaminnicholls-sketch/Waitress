const http = require('http');

const PORT = process.env.PORT || 3000;

// ── HTTP server — keeps Railway happy by holding an open port ───────────────
const server = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/plain' });
  res.end('Bot is alive!');
});

server.listen(PORT, () => {
  console.log(`[Keep-Alive] Server running on port ${PORT}`);
  startSelfPing();
});

// ── Self-ping — hits our own server every 4 minutes to stay awake ───────────
function startSelfPing() {
  const PING_INTERVAL_MS = 4 * 60 * 1000; // every 4 minutes

  setInterval(() => {
    const options = {
      hostname: 'localhost',
      port: PORT,
      path: '/',
      method: 'GET',
    };

    const req = http.request(options, (res) => {
      console.log(`[Keep-Alive] Self-ping OK — status ${res.statusCode}`);
    });

    req.on('error', (err) => {
      console.warn('[Keep-Alive] Self-ping failed:', err.message);
    });

    req.end();
  }, PING_INTERVAL_MS);

  console.log('[Keep-Alive] Self-ping scheduled every 4 minutes.');
}

module.exports = server;
