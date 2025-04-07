## TODO

- use spring jpa/hibernate to create tables in db
- Scraper should scrape and add all the data to the db separately
    - use pandas to get all table data
    - 
- ~make parent git to host both spring project and scraper in one repo~ 



### Scraper
- find all links
- iterate through and find all urls
- iterate through and send requests getting new response to make soup with
- parse the data in this new soup and add to the 

maybe make tables for regions and citys independently rather than trying to scrape it so you can just scrape the court name and data from each page and link it with foreign keys etc..

### things that need fixing
- currently i am scraping just links with daily in the title as i thought that was the ones that were relevant. now i see that there are posession orders in other ones, also some with funky formatting likely to need custom scraping logic. what a pain. Gonna try with jsut the daily selector and see how it goes?