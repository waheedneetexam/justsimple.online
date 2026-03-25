AI Agent Compatibility Plan

Objective:
- Make the site easy for AI agents to discover, parse, query, and use safely
- Keep the site human-friendly while adding structured, machine-readable access

Definition of "AI-agent compatible":
- machine-readable page metadata
- structured content blocks
- stable URLs and canonical IDs
- API access for search and page retrieval
- clear usage and policy boundaries for agents
- predictable internal linking and schemas

Plan:

1. Define the compatibility target
- Decide exactly what AI agents should be able to do
- Focus on:
  - discovering pages
  - reading structured summaries
  - retrieving full page metadata
  - navigating related content
  - using stable URLs and identifiers

2. Audit the current site
- Review existing HTML structure
- Review current API implementation
- Review search flow
- Review metadata consistency
- Confirm how the database fits into the system

3. Add machine-readable metadata to every page
- Standardize:
  - JSON-LD
  - page type
  - topic or entity name
  - summary
  - tags and categories
  - publication/update timestamps
  - canonical URL
  - stable internal page ID

4. Make content structure predictable
- Ensure every analysis page follows a standard section layout:
  - overview
  - what it is
  - how it works
  - business model
  - key metrics
  - history
  - comparisons
  - summary
- Use semantic HTML and clear section markers so agents can extract reliably

5. Build a dedicated agent-friendly API
- Add or standardize endpoints such as:
  - `/api/search?q=...`
  - `/api/pages`
  - `/api/page/:slug`
  - `/api/featured`
  - `/api/sitemap`
  - `/api/entities/:name`
- Return clean JSON optimized for machine consumption

6. Add an agent guidance document
- Create a public machine-oriented guidance file or page
- Include:
  - supported endpoints
  - allowed usage
  - attribution expectations
  - crawl guidance
  - rate-limit expectations
  - contact and policy information

7. Add discovery files
- Generate:
  - XML sitemap
  - structured internal content index
  - category and tag listings
  - updated robots guidance if needed

8. Use the database as the source of truth where possible
- Ensure the database can provide:
  - slugs
  - titles
  - summaries
  - tags
  - content sections
  - related pages
  - last-updated timestamps
- Make HTML pages and API output derive from the same core data

9. Normalize content for machine use
- Standardize:
  - slugs
  - titles
  - tag vocabulary
  - date formats
  - entity naming
  - footer and nav structure
  - related page links

10. Add agent-oriented QA
- Verify:
  - every page has valid structured data
  - every page is reachable through API and sitemap
  - section extraction is consistent
  - JSON responses are stable
  - canonical URLs are correct
  - duplicate entity identities do not exist

11. Document the system
- Write internal documentation for:
  - agent-facing architecture
  - API contracts
  - content schema
  - publishing workflow
  - future extension points

Deliverables:
- upgraded HTML pages
- agent-facing JSON API
- structured metadata across pages
- sitemap and discovery layer
- agent guidance document
- documentation for maintenance

Expected result:
- The site remains readable for people
- The site becomes easier for AI agents to use as a structured knowledge source
- Content can be discovered, queried, and interpreted more reliably
