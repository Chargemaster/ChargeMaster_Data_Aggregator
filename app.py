''' layout and callbacks for chargemaster interactive dashboard

'''
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State

# read in data files
hospital_fee = pd.read_csv('./data/all_hospital_fee_combined.csv')
hospital_address = pd.read_csv('./data/hospital_address.csv')
hospital_all = hospital_fee.merge(hospital_address, on = 'hospital', how = 'left')

# text that will show when hover
hospital_all['text'] = hospital_all['hospital'] + ' Size: ' + hospital_all['hospital_size'] + ' Address: ' + hospital_all['address'].astype(str)

# Plot out 4 graphs
app = dash.Dash(__name__)
server = app.server # for starting heroku
app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="🏥", style={'fontSize': "30px",'textAlign': 'center'}, className="header-emoji"),
                html.H1(children="Chargemaster Dashboard",style={'textAlign': 'center'}, className="header-title"),
                html.H2(children="Comparing prices from hospitals", style={'textAlign': 'center'}, className="header-description"),
            ],
            className="header",style={'backgroundColor':'#F5F5F5'},
        ),

        html.Div(
            children=[
                html.Div(children = 'DRG Code', style={'fontSize': "24px"},className = 'menu-title'),
                dcc.Dropdown(
                    id = 'drg-filter',
                    options = [
                        {'label': Code, 'value': Code}
                        for Code in hospital_all.drg_code.unique()
                    ],
                    value = [3, 4, 5],
                    clearable = False,
                    searchable = True,
                    multi = True,
                    className = 'dropdown',
                    style={'fontSize': "24px",'textAlign': 'center'},
                ),
            ],
           className = 'menu',
        ), #the drg_code dropdown filter
        
        html.Div(
            children=[
                html.Div(children = 'County', style={'fontSize': "24px"},className = 'menu-title'),
                dcc.Dropdown(
                    id = 'county-filter',
                    #'County' is the filter
                    options = [
                        {'label': County, 'value': County}
                        for County in hospital_all.county.unique()
                    ],
                    value = ['King'],
                    clearable = False,
                    searchable = True,
                    multi = True,
                    className = 'dropdown',
                    style={'fontSize': "24px",'textAlign': 'center'},
                ),
            ],
            className = 'menu',
        ), #the county dropdown filter

        html.Div(
            children=[
                html.Div(children = 'Hospital Size', style={'fontSize': "24px"},className = 'menu-title'),
                dcc.Dropdown(
                    id = 'size-filter',
                    options = [
                        {'label': Size, 'value': Size}
                        for Size in hospital_all.hospital_size.unique()
                    ], #'Size' is the filter
                    value = ['Large', 'Medium', 'Small'],
                    clearable = False,
                    searchable = True,
                    multi = True,
                    className = 'dropdown',
                    style={'fontSize': "24px",'textAlign': 'center'},
                ),
            ],
            className = 'menu',
        ), #the hospital_size dropdown filter

        html.Div(
            children=[
                html.Div(
                children = dcc.Graph(
                    id = 'geoscatter',
                    figure = fig_1,
                ),
                style={'width': '50%', 'display': 'inline-block'},
            ),

                html.Div(
                children = dcc.Graph(
                    id = 'histogram',
                    figure = fig_2,
                    config={"displayModeBar": False},
                ),
                style={'width': '50%', 'display': 'inline-block'},
            ),

                html.Div(
                children = dcc.Graph(
                    id = 'bar',
                    figure = fig_3,
                    config={"displayModeBar": False},
                ),
                style={'width': '50%', 'display': 'inline-block'},
            ),

                html.Div(
                children = dcc.Graph(
                    id = 'table',
                    figure = fig_4,
                    config={"displayModeBar": False},
                ),
                style={'width': '50%', 'display': 'inline-block'},
            ),

        ],
        className = 'double-graph',
        ),
    ]
)

# callbacks
# geomap
@app.callback(
    Output("geoscatter", "figure"),
    [Input("drg-filter", "value"),
    Input("county-filter", "value"),
    Input("size-filter", "value")
    ],
)
def update_charts(Code, County, Size):
    if len(Code) == 0 or len(County) == 0 or len(Size) == 0:
        return dash.no_update
    else:
        filtered_data = hospital_all[hospital_all["drg_code"].isin(Code)&\
                                     hospital_all["county"].isin(County)&\
                                     hospital_all["hospital_size"].isin(Size)]

        figure = go.Figure(data = go.Scattergeo(
                        lon = filtered_data['longtitude'],
                        lat = filtered_data['latitude'],
                        text = filtered_data['text'],
                        mode = 'markers',
                        marker_color = filtered_data['price'],
                        ))

        figure.update_geos(
                        center = dict(lon = -120.31634289576678, lat = 47.42494286618738),
                        lataxis_range = [45.5,49], lonaxis_range = [-124, -116],
                        showcountries = True, countrycolor = "lightslategrey",
                        showsubunits = True, subunitcolor = "Goldenrod"
                        )

        figure.update_layout(
                        title = 'Hospital Location',
                        geo_scope='usa',
                        )
        # return geomap
        return figure

# Hist
@app.callback(
    Output("histogram", "figure"),
    [Input("drg-filter", "value"),
    Input("county-filter", "value"),
    Input("size-filter", "value")
    ],
)

def update_charts(Code, County, Size):
    if len(Code) == 0 or len(County) == 0 or len(Size) == 0:
        return dash.no_update
    else:
        filtered_data = hospital_all[hospital_all["drg_code"].isin(Code)&\
                                     hospital_all["county"].isin(County)&\
                                     hospital_all["hospital_size"].isin(Size)]

        figure = px.histogram(filtered_data,
                         x = "price",
                         nbins = 100,
                         color_discrete_sequence = ['lightslategrey'],)

        figure.add_vline(x = np.median(hospital_all.price),
                        line_dash = 'dash',
                        line_color = 'goldenrod')

        return figure

# Bar plot
@app.callback(
    Output("bar", "figure"),
    [Input("drg-filter", "value"),
    Input("county-filter", "value"),
    Input("size-filter", "value")
    ]
)

def update_charts(Code, County, Size):
    if len(Code) == 0 or len(County) == 0 or len(Size) == 0:
        return dash.no_update
    else:    
        filtered_data = hospital_all[hospital_all["drg_code"].isin(Code)&\
                                     hospital_all["county"].isin(County)&\
                                     hospital_all["hospital_size"].isin(Size)]
        
        small = go.Bar(
                      x = filtered_data[filtered_data.hospital_size == 'Small']['county'].unique(),
                      y = filtered_data[filtered_data.hospital_size == 'Small'].groupby(['county'])['price'].mean(),
                      name = 'Small',
                      marker_color = 'lightslategrey',)
        medium = go.Bar(
                      x = filtered_data[filtered_data.hospital_size == 'Medium']['county'].unique(),
                      y = filtered_data[filtered_data.hospital_size == 'Medium'].groupby(['county'])['price'].mean(),
                      name = 'Medium',
                      marker_color = 'darkolivegreen')
        large = go.Bar(
                      x = filtered_data[filtered_data.hospital_size == 'Large']['county'].unique(),
                      y = filtered_data[filtered_data.hospital_size == 'Large'].groupby(['county'])['price'].mean(),
                      name = 'Large',
                      marker_color = 'goldenrod')
    
        figure = go.Figure(data = [small, medium, large])
        figure.update_layout(barmode = 'group',
                           title="Average Treatment Price by County/Hospital Size")
        return figure

# Table (data)   
@app.callback(
    Output("table", "figure"),
    [Input("drg-filter", "value"),
    Input("county-filter", "value"),
    Input("size-filter", "value")
    ]
)

def update_charts(Code, County, Size):
    if len(Code) == 0 or len(County) == 0 or len(Size) == 0:
        return dash.no_update
    else:    
        filtered_data = hospital_all[hospital_all["drg_code"].isin(Code)&\
                                     hospital_all["county"].isin(County)&\
                                     hospital_all["hospital_size"].isin(Size)]
        figure = go.Figure(data = [go.Table(
                    header = dict(values = ['Hospital', 'County', 'Address', 'Size', 'Treatment', 'Price'],
                                  font = dict(color='white'),
                                  fill_color='lightslategrey',
                                  align='left'),
                    cells = dict(values = [filtered_data.hospital, filtered_data.county, filtered_data.address, filtered_data.hospital_size, filtered_data.name, filtered_data.price],
                                  align = 'left'))
            ])
    
        figure.update_layout(title = "Price Information")
        return figure

if __name__ == '__main__':
    app.run_server(debug=True)
