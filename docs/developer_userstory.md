## Developer User Story
The developer will run the scraper program to generate individual hospital
data files, will run the program to clean and merge the individual hospital
files into a single database, and will ensure that the visualization program
is able to access the appropriate variables in the database to generate 
visualizations and analysis. 

## Developer Use Cases

* Run the scraper program
* Check that Individual Hospital data files have been downloaded
* Check list of hospitals in which no chargemaster was found
* Run the data cleaning and merge program
* Check that all hospitals are included merged database
* Link database to visualization program

## Component Specification
*Webscraper* 
1. Scraper inputs list of hospital URLs (WA Hospital URLs generated from 
Washington State Hospital Association list)
2. Scraper outputs individual hospital chargemaster files & list of 
hospitals where no file was found.
3. Data cleaning and merging program pulls variables from individual
hospital data files, cleans and standardizes data and adds to database. 
4. Visualization program links to database and references variables as
necessary to generate analysis.
