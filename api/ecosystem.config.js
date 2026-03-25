module.exports = {
  apps: [{
    name:        'justsimple-api',
    script:      '/home/waheed/WebCrawl/api/server.js',
    cwd:         '/home/waheed/WebCrawl/api',
    instances:   1,
    exec_mode:   'fork',
    autorestart: true,
    watch:       false,
    max_memory_restart: '150M',
    env: {
      NODE_ENV:    'production',
      DB_PASSWORD: 'js@p1_s3cur3!',
    },
    error_file: '/home/waheed/.pm2/logs/jsapi-error.log',
    out_file:   '/home/waheed/.pm2/logs/jsapi-out.log',
    log_date_format: 'YYYY-MM-DD HH:mm:ss',
  }],
};
