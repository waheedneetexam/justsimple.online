const express = require('express');
const router  = express.Router();
const pool    = require('../db');

// GET /api/search?q=bitcoin
router.get('/', async (req, res) => {
  const q = (req.query.q || '').trim();

  if (!q || q.length < 2) {
    return res.json({ results: [] });
  }

  try {
    const { rows } = await pool.query(`
      SELECT
        id,
        name,
        url,
        description,
        tags,
        folder_path,
        ts_rank(search_vector, plainto_tsquery('english', $1)) AS rank
      FROM sites
      WHERE
        search_vector @@ plainto_tsquery('english', $1)
        OR name ILIKE $2
        OR description ILIKE $2
      ORDER BY rank DESC, name
      LIMIT 10
    `, [q, `%${q}%`]);

    res.json({ results: rows });
  } catch (err) {
    console.error('Search error:', err.message);
    res.status(500).json({ error: 'Search failed' });
  }
});

module.exports = router;
