# Persisting all court case data in postgres
---

### Context
Need to access the html data on the court website, allowing users to search for particular terms

### Decision
Using PostgreSQL to persist all data, scraping at a schedule, rather than on demand. Using postgres as it is familiar to me. This will also allow the arhiving of data, allowing potential interesting insights to be extracted later also.

### Alternatives Considered
Keeping scraping as an "on the fly" action, using other dbs, not persisting data...

### Consequences
..idk
### Status
- Accepted
