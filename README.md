# Chargemaster Data Aggregator & Analysis

<p align="left"><img src="https://github.com/Chargemaster/ChargeMaster_Data_Aggregator/blob/3ba46778eb2950c838ad184406542957a1ed75a7/docs/Screen%20Shot%202021-12-06%20at%209.08.21%20PM.png" width=250 alt="chargemaster logo"/></p>



Hospitals must have transparency in releasing hospital charges for services that they provide. A "Charge Master Description" (CDM) is a file, usually in CSV or Excel format, that lists prices for each service. Since there is no regulation on how hospitals need to format this data, each hospital's CDM varies greatly from another which makes cost breakdown and analysis very difficult for anyone who is trying to compare costs between hospitals for specific services, procedures, and labor. 

## Purpose
This project is part of a school project with the University of Washington's CSE 583 course. We are aiming to compile the CDMs of hospitals listed by the Washington State Hospital Association which can be found [here](https://www.wsha.org/our-members/member-listing/#non-hospital-member-list). 

Additionally, we are aiming to do cost analysis on groups of services and/or goods and see what we may find. This project will be a work in progress during and most likely past the course itself.

## Requirements

Chargemaster has the following dependencies: 
1. Python = 3.9

## Usage

Chargemaster can be used to scrape CDM files from Washington State Hospital webpages. The downloaded data files are then organized, cleaned, and reformated for analysis and visualization in a dashboard.

## Modules Overview

 * __scraper.py__         :  Webscraper to gather CDM files from Washington Hospitals.
 * __file_delete.py__        :  Sorts scraped files, and retains .csv and .xlsx data files.
 * __file_rename.py__      :  Renames and numbers scraped data files by hospital.
 * __file_formatting.py__  : Not yet developed - pulls relevant columns from individual datasets and merges into master dataset for analysis.
 * __app.py__   :  Dashboard to visualize hospital prices by Diagnosis-related Group (DRG) code.

## Use Case

A prospective patient needing non-immediate medical attention may be more focused on balancing care with financial burden.

This could be calculating the cost of a one-time procedure along with consistent medical attention needed like refilling prescriptions, check-ups every X months, along with hospital size and location (E.g. They probably don't want to drive hours to a hospital they have to go to somewhat regualrly). The user can look at the dashboard, filter by type of service, hospital size, and county in Washington state. They can then see the hospitals fitting the criteria, their locations, price distribution, and compare their costs side to side for the specific services and/or medical goods/attention they may need.

## Workflow
<p align="center"><img src="https://github.com/Chargemaster/ChargeMaster_Data_Aggregator/blob/b60b93df42b42aedea64e2d7741cc2796efa25c6/docs/Chargemaster%20Workflow-4.png" width=1000 alt="chargemaster logo"/></p>

## Dashboard Design

Dashboard link: https://cse583-chargemaster.herokuapp.com/

<p align="center"><img src="https://github.com/Chargemaster/ChargeMaster_Data_Aggregator/blob/8e29861c98726901aded30bfcbd1a23ec29e1566/docs/dashboard.png" width=1000 alt="dashboard"/></p>

We decided to include four visualizations and 3 filters in our dashboard for users to view hospitals and procedure prices based on their needs. 

### Filters

 * DRG Code  :  Diagnosis-related group (DRG) is a system which classifies hospital cases according to certain groups, also referred to as DRGs, which are expected to have similar hospital resource use (cost). They have been used in the United States since 1983. Users can select DRG codes from this filter to narrow down the data and focus on specific diagnosis, treatment and length of hospital stay they are looking for.
 * County   :  Users can select from counties in the Washington state that are closer to where they live.
 * Hospital Size   :  Users can select whether they want to search for small, medium, or large hospitals that provide they procedure they are looking for.


### Visualizations

#### Geo Map

The geo map uses latitude and longitude to plot the location of hospitals in WA. We put this on the top left because users can have an overview of the locations and see whether there are hospitals that provide procedures in the county they selected. Users can also view basic information such as address and hospital size by hovering their curser on the dot. 

#### Price Distribution

After selecting the DRG code(s), the second chart will show the price distribution of the procedures and the average price. Users can get a better understanding of the price of the selected code to make estimation.

#### Price Comparison

The third chart allows users to make comparison of the prices among hospitals in different counties and size. They can compare the prices of the same procedure from small, medium, and large hospitals in the same county, or compare the prices of the same procedures among same-size hospitals in different counties. This chart helps patients find the hospital with the lowest price under the selected filters.

#### Detailed Information

After having a better understanding of from a bigger scope, some patients might still want to look at detailed information of the hospital, procedure, and the price, so we put a table that shows text of the search result.
