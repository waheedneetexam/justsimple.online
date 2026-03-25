const pool = require('./db');

const sites = [
  {
    name:        'BTCPay Server',
    url:         'https://btcpayserver.org',
    description: 'Open-source Bitcoin payment processor. Accept crypto with 0% fees, no middleman, fully self-hosted.',
    tags:        ['Bitcoin', 'Payments', 'Open Source', 'Crypto', 'Self-hosted', 'Invoice'],
    folder_path: '/btcpayserver.org/',
  },
  {
    name:        'Phoenix Wallet',
    url:         'https://phoenix.acinq.co',
    description: 'Self-custodial Lightning Network Bitcoin wallet by ACINQ. Send Bitcoin instantly with auto channel management.',
    tags:        ['Lightning', 'Bitcoin', 'Mobile Wallet', 'ACINQ', 'Self-custodial', 'Lightning Network'],
    folder_path: '/phoenix.acinq.co/',
  },
  {
    name:        'Amazon',
    url:         'https://www.amazon.com',
    description: 'World\'s largest online retailer and cloud computing provider. 315M+ customers, AWS, Prime, Alexa, and more.',
    tags:        ['E-Commerce', 'Cloud', 'AWS', 'Prime', 'Shopping', 'Streaming', 'Marketplace'],
    folder_path: '/amazon.com/',
  },
  {
    name:        'Yahoo',
    url:         'https://www.yahoo.com',
    description: 'Pioneer web portal with 1B+ users. Yahoo Mail, News, Finance, Sports — all in one place since 1994.',
    tags:        ['Web Portal', 'Email', 'News', 'Finance', 'Search', 'Yahoo Mail'],
    folder_path: '/yahoo.com/',
  },
  {
    name:        'TikTok',
    url:         'https://www.tiktok.com',
    description: 'Short-form video platform by ByteDance with 1.6B users. AI-powered For You feed and $23B revenue in 2024.',
    tags:        ['Video', 'Social Media', 'Entertainment', 'ByteDance', 'Short-form', 'Algorithm'],
    folder_path: '/tiktok.com/',
  },
  {
    name:        'Bing',
    url:         'https://www.bing.com',
    description: 'Microsoft\'s AI-powered search engine with Copilot. 3.36B monthly visits and 11.78% desktop market share.',
    tags:        ['Search', 'AI', 'Microsoft', 'Copilot', 'ChatGPT', 'Web Search'],
    folder_path: '/bing.com/',
  },
  {
    name:        'Yahoo Japan',
    url:         'https://www.yahoo.co.jp',
    description: 'Japan\'s #1 web portal with 83M+ monthly users. News, shopping, auctions, PayPay payments and 100+ services.',
    tags:        ['Japan', 'Web Portal', 'PayPay', 'Shopping', 'News', 'Auctions', 'Japanese'],
    folder_path: '/yahoo.co.jp/',
  },
  {
    name:        'DuckDuckGo',
    url:         'https://www.duckduckgo.com',
    description: 'Privacy-first search engine that never tracks you. 71.9B searches in 2024, #2 mobile search in 20+ countries.',
    tags:        ['Privacy', 'Search', 'No Tracking', 'Anonymous', 'Security', 'Private Browser'],
    folder_path: '/duckduckgo.com/',
  },
  {
    name:        'Temu',
    url:         'https://www.temu.com',
    description: 'Gamified ultra-discount shopping from PDD Holdings. 1B+ downloads, 180+ countries, direct from manufacturers.',
    tags:        ['E-Commerce', 'Shopping', 'Deals', 'Discounts', 'Gamified', 'China', 'PDD Holdings'],
    folder_path: '/temu.com/',
  },
  {
    name:        'Weather.com',
    url:         'https://www.weather.com',
    description: 'IBM\'s global weather platform since 1988. Powers 95% of weather apps worldwide with 100M+ monthly users.',
    tags:        ['Weather', 'Forecast', 'IBM', 'Climate', 'Radar', 'Weather API', 'Meteorology'],
    folder_path: '/weather.com/',
  },
  {
    name:        'Netflix',
    url:         'https://www.netflix.com',
    description: 'World\'s leading streaming service with 230M+ subscribers. $17B content spend, originals in 190 countries.',
    tags:        ['Streaming', 'Entertainment', 'Movies', 'TV Shows', 'Originals', 'Subscription', 'Video'],
    folder_path: '/netflix.com/',
  },
];

async function seed() {
  for (const s of sites) {
    await pool.query(
      `INSERT INTO sites (name, url, description, tags, folder_path)
       VALUES ($1, $2, $3, $4, $5)
       ON CONFLICT (url) DO UPDATE SET
         name        = EXCLUDED.name,
         description = EXCLUDED.description,
         tags        = EXCLUDED.tags,
         folder_path = EXCLUDED.folder_path`,
      [s.name, s.url, s.description, s.tags, s.folder_path]
    );
    console.log(`✓ Seeded: ${s.name}`);
  }
  await pool.end();
  console.log('Seed complete.');
}

seed().catch(err => { console.error(err); process.exit(1); });
