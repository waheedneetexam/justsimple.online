const express = require('express');
const router  = express.Router();
const db      = require('../db');

const POOL_SIZE    = 20;   // sites fetched from DB each cycle
const TTL_MS       = 60 * 60 * 1000; // 1 hour

let cache = {
  sites:     [],
  expiresAt: 0,
};

async function refreshCache() {
  const result = await db.query(
    `SELECT name, url, description, tags, folder_path
     FROM sites
     ORDER BY RANDOM()
     LIMIT $1`,
    [POOL_SIZE]
  );
  cache.sites     = result.rows;
  cache.expiresAt = Date.now() + TTL_MS;
  console.log(`[featured] cache refreshed — ${cache.sites.length} sites, next refresh in 1h`);
}

// GET /api/featured
router.get('/', async (req, res) => {
  try {
    if (Date.now() > cache.expiresAt || cache.sites.length === 0) {
      await refreshCache();
    }
    res.json({
      sites:      cache.sites,
      expiresAt:  cache.expiresAt,
      poolSize:   cache.sites.length,
    });
  } catch (err) {
    console.error('[featured] error:', err.message);
    res.status(500).json({ error: 'failed to load featured sites' });
  }
});

module.exports = router;
