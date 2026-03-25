const express = require('express');
const router = express.Router();
const db = require('../db');

// GET /api/sites
router.get('/', async (req, res) => {
  try {
    const { rows } = await db.query(
      `SELECT name, url, description, tags, folder_path
       FROM sites
       ORDER BY name ASC`
    );

    res.json({
      sites: rows,
      count: rows.length,
    });
  } catch (err) {
    console.error('[sites] error:', err.message);
    res.status(500).json({ error: 'failed to load sites' });
  }
});

module.exports = router;
