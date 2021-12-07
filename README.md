# Chargemaster Data Aggregator & Analysis

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

## Modules Overview:
 * __scraper.py__         :  Webscraper to gather CDM files from Washington Hospitals.
 * __file_delete.py__        :  Sorts scraped files, and retains .csv and .xlsx data files.
 * __file_rename.py__      :  Renames and numbers scraped data files by hospital.
 * __file_formatting.py__  : Not yet developed - pulls relevant columns from individual datasets and merges into master dataset for analysis.
 * __dashboard.ipynb__   :  Dashboard to visualize hospital prices by Diagnosis-related Group (DRG) code.


