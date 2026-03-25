SEO Improvement Plan for JustSimple.Online HTML Pages

Current status:
- The site is crawlable at a basic level.
- Most pages have valid HTML structure, `lang`, `charset`, `viewport`, a single `<title>`, a single `<h1>`, and sensible heading hierarchy.
- Several pages already include a useful meta description.
- The site is not yet fully SEO-optimized.

Main gaps found:
- Many pages are missing `<meta name="description">`
- No canonical tags were found
- No Open Graph tags were found
- No Twitter card tags were found
- No JSON-LD structured data was found
- Some page titles are too generic and should be made more search-specific

Pages that need meta descriptions:
- /home/waheed/WebCrawl/index.html
- /home/waheed/WebCrawl/amazon.com/index.html
- /home/waheed/WebCrawl/bing.com/index.html
- /home/waheed/WebCrawl/btcpayserver.org/index.html
- /home/waheed/WebCrawl/duckduckgo.com/index.html
- /home/waheed/WebCrawl/phoenix.acinq.co/index.html
- /home/waheed/WebCrawl/tiktok.com/index.html
- /home/waheed/WebCrawl/yahoo.com/index.html
- /home/waheed/WebCrawl/yahoo.co.jp/index.html

Recommended fixes:
1. Add unique meta descriptions to every HTML page
2. Add a canonical tag to every page
3. Add Open Graph tags:
   - `og:title`
   - `og:description`
   - `og:type`
   - `og:url`
   - `og:site_name`
4. Add Twitter card tags:
   - `twitter:card`
   - `twitter:title`
   - `twitter:description`
5. Add JSON-LD structured data:
   - `WebSite` for homepage
   - `Article` or `WebPage` for analysis pages
6. Improve weak page titles so they better match search intent
7. Keep one clear `<h1>` per page and preserve clean heading order
8. Ensure internal linking from the homepage remains strong

Suggested title pattern:
- `<Brand/Topic> Analysis — JustSimple.Online`
- or
- `How <Brand/Topic> Works — JustSimple.Online`

Suggested meta description pattern:
- `Independent analysis of <brand/topic>: how it works, what it offers, its business model, history, and why it matters.`

Suggested structured data approach:
- Homepage:
  - `WebSite`
- Individual analysis pages:
  - `Article` or `WebPage`
  - include title, description, URL, publisher, and main entity

Implementation order:
1. Patch homepage metadata
2. Patch missing meta descriptions on all content pages
3. Add canonical tags everywhere
4. Add Open Graph and Twitter tags everywhere
5. Add JSON-LD structured data
6. Review titles for search quality
7. Re-scan all pages for consistency

Verification checklist:
- Every page has one `<title>`
- Every page has one meta description
- Every page has one canonical tag
- Every page has Open Graph tags
- Every page has Twitter card tags
- Every page has one `<h1>`
- Structured data exists where appropriate
- No duplicate metadata blocks

Expected result:
- Better search result snippets
- Cleaner indexing signals
- Improved social sharing previews
- Stronger consistency across all analysis pages
