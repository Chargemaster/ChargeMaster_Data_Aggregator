This file provides patients a walk through of how to use our dashboard to compare prices among hospitals and make decisions on which hospital they should select.

## Getting Started

Our dashboard has 3 filters and 4 charts.

### How to Select Filters

<p align="center"><img src="https://github.com/Chargemaster/ChargeMaster_Data_Aggregator/blob/8e29861c98726901aded30bfcbd1a23ec29e1566/docs/dashboard_filter.png" width=1000 alt="dashboard_filter"/></p>

 * DRG Code  :  Diagnosis-related group (DRG) is a system which classifies hospital cases according to certain groups, also referred to as DRGs, which are expected to have similar hospital resource use (cost). They have been used in the United States since 1983. Users can select DRG codes from this filter to narrow down the data and focus on specific diagnosis, treatment and length of hospital stay they are looking for. 
 * County   :  Users can select from counties in the Washington state that are closer to where they live.
 * Hospital Size   :  Users can select whether they want to search for small, medium, or large hospitals that provide they procedure they are looking for.

### How to Interpret Data from the Visualizations

<p align="center"><img src="https://github.com/Chargemaster/ChargeMaster_Data_Aggregator/blob/8e29861c98726901aded30bfcbd1a23ec29e1566/docs/dashboard_visualizations.png" width=1000 alt="dashboard_chart"/></p>

#### Geo Map

Users can have an overview of the locations and see which hospitals provide procedures for their cases. Users can also view basic information such as address and hospital size by hovering their curser on the dot. They can then determine whether there are hospitals close to them that provide the procedure they want, or they need to adjust the filter and search for hospitals in other counties.

#### Price Distribution

After selecting the DRG code(s) and county, the second chart will show the price distribution of the procedures and the average price. Users can get a better understanding of the price of the selected code to make estimation. They can also refer to the yellow line, which is the average price of the selected DRG code in the filtered hospitals.

#### Price Comparison

The third chart allows users to make comparison of the prices among hospitals in different counties and size. They can compare the prices of the same procedure from small, medium, and large hospitals in the same county, or compare the prices of the same procedures among same-size hospitals in different counties. This chart helps patients find the hospital with the lowest price under the selected filters. For example, if a patient found that the average price in King County is much higher, they might want to travel a bit and go to a hospital in Snohomish county.

#### Detailed Information

After having a better understanding of from a bigger scope, some patients might still want to look at detailed information of the hospital, procedure, and the price, so we put a table that shows text of the search result.