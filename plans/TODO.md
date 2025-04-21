## TODO

 
- ~make parent git to host both spring project and scraper in one repo, currently some weird thing where one is inside the other but they are still pushing separately~ 

- dockerise python part

- build out backend endpoints/set it up as an API
- something about city/location
- tests
- type hints/return values and documentation comments
- Deal with collisions in db?




### things that need fixing
- currently i am scraping just links with daily in the title as i thought that was the ones that were relevant. now i see that there are posession orders in other ones, also some with funky formatting likely to need custom scraping logic. what a pain. Gonna try with jsut the daily selector and see how it goes?

- different courts et updated at different times, I dont know when to do the scheduled scrape. Is there a time by which all will be updated for the following day? maybe at midnight? otherwise do i need custom scrape logic that will check whether the date is for tomorrow before scraping it and have it run periodically over the day? <br>
**Dates can be like up to four days into the future so i need to get the date from the page not from the current date!!!** may as well not do daily whilst in there.
- also therefore need to do checks to not insert duplicate data, as there will be some courts that are in multiple days scrapes.

- need to do testing. If you are relying on this to tell you whether or not you might be getting evicted you want it to be robust.

- there is definitely at least one other semi common html structure for court pages that should be conditionally scraped/parsed

- Newport IOW will need extra logic

- Need better regex for cases like this: M00KH164 Matthew James (Joint LPA Receivers) -v- Persons Unknown, the v messing it up?

- Clerkenwell and shoreditch not showing up

- stratford needs to be included separately to clerkenwell and shoreditch

- Central london is a different format, slough also, maybe distinguishable from: "Civil and Family Daily Cause List"

- Not all of east london are coming through?

- Maybe create a debug statement so that I can see how many courts are found per location? to compare with website to see if any are being missed.

- may as well take all data whilst im here. new fields for cases without claimant/defendant structures.

- DO PERSIST RAW CASE DETAILS STRING
