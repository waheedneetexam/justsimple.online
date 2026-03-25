const express = require('express');
const cors    = require('cors');
const search  = require('./routes/search');

const app  = express();
const PORT = 3011;

app.use(cors({ origin: ['https://justsimple.online', 'https://www.justsimple.online'] }));
app.use(express.json());

app.use('/api/search', search);

app.get('/api/health', (req, res) => res.json({ ok: true, ts: new Date() }));

app.listen(PORT, '127.0.0.1', () => {
  console.log(`[justsimple-api] listening on 127.0.0.1:${PORT}`);
});
