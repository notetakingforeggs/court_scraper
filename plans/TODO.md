## TODO

 
- ~make parent git to host both spring project and scraper in one repo, currently some weird thing where one is inside the other but they are still pushing separately~ 

- dockerise python part

- build out backend endpoints/set it up as an API
- something about city/location
- tests
- type hints/return values and documentation comments
- Deal with collisions in db?




### things that need fixing
- ~~ currently i am scraping just links with daily in the title as i thought that was the ones that were relevant. now i see that there are posession orders in other ones, also some with funky formatting likely to need custom scraping logic. what a pain. Gonna try with jsut the daily selector and see how it goes?~~

- different courts et updated at different times, I dont know when to do the scheduled scrape. Is there a time by which all will be updated for the following day? maybe at midnight? otherwise do i need custom scrape logic that will check whether the date is for tomorrow before scraping it and have it run periodically over the day? <br>

times that courtserve has refreshed:
- 12:23
- 21:37
- 00:31
- 00:30
- 10:03

I'm thinking to scrape at 01:00 for the next day?

**Dates can be like up to four days into the future so i need to get the date from the page not from the current date!!!** may as well not do daily whilst in there.
- ~~also therefore need to do checks to not insert duplicate data, as there will be some courts that are in multiple days scrapes.~~

- need to do __more__ testing. If you are relying on this to tell you whether or not you might be getting evicted you want it to be robust.

- ~~there is definitely at least one other semi common html structure for court pages that should be conditionally scraped/parsed~~

- ~~Newport IOW will need extra logic deprioritised~~

- ~~Need better regex for cases like this: M00KH164 Matthew James (Joint LPA Receivers) -v- Persons Unknown, the v messing it up?~~

- ~~Clerkenwell and shoreditch not showing up~~

- ~~stratford needs to be included separately to clerkenwell and shoreditch~~

- Central london is a different format, slough also, maybe distinguishable from: "Civil and Family Daily Cause List"

- Not all of east london are coming through?

- ~~may as well take all data whilst im here. new fields for cases without claimant/defendant structures.~~

- ~~DO PERSIST RAW CASE DETAILS STRING, good for reference and when parsing breaks~~

- ~~clean up duration strings, maybe also clean into minutes?~~

- need to tighten up regex for v, as some are splitting on v within words. need to exclude v when it is part of like receivers 
## GDPR concerns

- A lot of these entries have full names of individuals in... personal data persistence == gdpr concerns

- "Legitimate Interests" are needed to justify persisting of data. this project should be valid in that it serves a real purpose and needs the names of people accessible to allow for people to search by their name to check if they have court date that they are not aware of.

- Will have to do some sort of ID verification / email verification enough? to verify users. Or.... maybe you can put a name in and it will just say like yes or no and then point you to the relevant courtserve page?

- but then do i have legitimate interests to persist into the future. Interested in exploring patterns that may emerege, and wouldn't want to cut out the possibility of deanonymisation if it could become vital in the future.

steps now though...

1. ~~fix current tests~~
2. ~~clean up duration strings~~
3. ~~consider refactoring any sprawling methods into smaller subunits~~
4. ~~build out test suite for scraping including full page scrape for normal case~~
5. ~~implement conditional scraping for non normal court pages - here use polymorphism? and create different scraper classes?~~

bugs to iron out: 

1.~~ brighton style page~~
2. over 8 but common case (disregard trailing empty spans)
3. single empty leading span resulting in duration parsing error

_There will be more bugs and I haven't got every different page shape accounted for, but i think i need to move on as I am getting restless_


## Atypical daily cause strcutres:

__ There are approx 37 courts I know are failing__
 I should use logging to keep track of this, adding the court name/url to a log upon failure.


## now doing some dev ops stuff? 
- dockerise scraper 
- hook up scraper to psql db via compose?
- crontab automate scraping daily at 7
- just run it on my laptop for now
- host on either old thinkpad (noisy?) or vps (oracle)

so then i have this scraper running and populating this database, with data that i will anonymise. GDPR etc.. maybe purge it every three days to avoid storing personal data until i have the encrpytion and hashing implemented. 

then i set up the backend rest endpoints to allow searching for cases by name of defendant/claimant... also by type?