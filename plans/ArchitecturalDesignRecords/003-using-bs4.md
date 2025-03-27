# Using bs4 and requests for scraping 
---

### Context
I need to scrape this data from the court pages, and as such need some scraping/parsing library. The court website seems to be statically generated php.

### Decision
Using scrapy with requests to navigate and parse the data

### Alternatives Considered
using selenium/playwright for navigation (needed for high js sites), using scrapy (asynchronous, faster for more scraping)

### Consequences
should be fine and simple enough to start with

### Status
- Accepted
