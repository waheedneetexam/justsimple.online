const { Pool } = require('pg');

const pool = new Pool({
  host:             'localhost',
  port:             5432,
  database:         'justsimple',
  user:             'jsapi',
  password:         process.env.DB_PASSWORD || 'js@p1_s3cur3!',
  max:              10,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 5000,
});

pool.on('error', (err) => {
  console.error('Unexpected DB error:', err.message);
});

module.exports = pool;
