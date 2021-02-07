# author: Sasha Babicki, Ifeanyi Anene, and Cal Schafer 
# date: 2021-01-22

"""
Generate crime statistics dashboard with 2 tabs
Usage: python src/app.py
Source for code to create tabs: https://dash.plotly.com/dash-core-components/tabs
Source for choropleth map boundaries: https://exploratory.io/map 
Tutorial used for Leaflet: https://dash-leaflet.herokuapp.com/#geojson 
"""

import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import dash_leaflet as dl
from dash_extensions.javascript import Namespace, arrow_function

import altair as alt
import pandas as pd
import json
import numpy as np
import matplotlib
from matplotlib import cm

import tab1
import tab2


app = dash.Dash(__name__,  external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
app.title = 'Canadian Crime Dashboard'
server = app.server

app.layout = html.Div([
    dbc.Row(
        [
            html.H2("Criminality in Canada: Fighting Anecdotes with Data",
            style = {                    
                    'padding':5
                    }
            )
        ],
        style={'backgroundColor': '#e6e6e6',
                'border-radius': 5,
                'margin':10,
        }

    ),
    dbc.Tabs(
        [
            dbc.Tab(label='Geographic Crime Comparisons', tab_id='tab-1', label_style={'font-weight':'bold'}),
            dbc.Tab(label='Crime Trends', tab_id='tab-2', label_style={'font-weight':'bold'})
        ],
        id='crime-dashboard-tabs',
        active_tab='tab-1'
    ),
    html.Div(id='crime-dashboard-content')
])


@app.callback(
    Output('crime-dashboard-content', 'children'),
    Input('crime-dashboard-tabs', 'active_tab'))
def render_content(tab):
    """Renders the selected tab
   
   Parameters
   -------
   String
       The name of the tab selected
   
   Returns
   -------
   html
       The page to render
    """
    data = import_data()
    if tab == 'tab-1':
        return html.Div([
            tab1.generate_layout()
        ])
    elif tab == 'tab-2':
        return html.Div([
            tab2.generate_layout()
        ])

# Pull initial data for plots
def import_data():
    """Import data from file
    Returns
    -------
    pd.Dataframe
        dataframe containing all data from the processed import file
    """
    
    # Disable max rows for data sent to altair plots
    alt.data_transformers.disable_max_rows()
    
    path = "data/processed/DSCI532-CDN-CRIME-DATA.tsv"
    data = pd.read_csv(path, sep="\t", encoding="ISO-8859-1")
    
    ### Data Wrangling 
    data = data.dropna()
    data.replace(" \[.*\]", "", regex=True, inplace=True)
    data.loc[data["Geography"] == "Prince Edward Island", "Geo_Level"] = data["Geo_Level"].replace("CMA", "PROVINCE")
    data['Geography'].replace("\?", "e", regex=True, inplace=True)
    
    # Remove total col
    data = data[data['Level1 Violation Flag'] != "Total, all violations"]
    
    # Change subcategory name to All for totals 
    for name in data['Level1 Violation Flag'].unique():
        data['Violation Description'].replace(name, "All", inplace=True)
    
    # Separate 'Geography' into Province and CMA
    data[['CMA','Province']]=data['Geography'].str.extract(r'(?P<CMA>^.*)\,(?P<Province>.*$)')
    data.loc[(data["Geo_Level"] == "PROVINCE"),'Province'] = data.loc[(data["Geo_Level"] == "PROVINCE"),'Geography']


    return data
    
DATA = import_data()

def import_map():
    """Import map data from file
    Returns
    -------
    json
        geojson for provinces
    """
    
    with open("data/processed/provinces.geojson") as f:
        geojson = json.load(f)
    return geojson

PROVINCES = import_map()

# CMA plot, tab1
@app.callback(
   Output('cma_barplot', 'srcDoc'),
   Input('metric_select', 'value'), 
   Input('violation_select', 'value'),
   Input('subviolation_select', 'value'),
   Input('year_select', 'value'), 
   Input('highlight', 'value'))
def generate_cma_barplot(metric, violation, subcategory, year, highlight):
    """Updates the CMA barplot on tab 1 when triggered
    
    Parameters
    -------
    String
        The name of the metric selected from the dropdown
    String
        The violation selected from the dropdown
    String
        The subcategory selected from the dropdown
    Int
        The year selected from the slider
    
    Returns
    -------
    html
        An altair plot in html format
    """

    df = DATA[
        (DATA["Metric"] == metric) & 
        (DATA["Level1 Violation Flag"] == violation) &
        (DATA["Violation Description"] == subcategory) &
        (DATA["Year"] == year) &
        (DATA["Geo_Level"] == "CMA")
    ]
    
    df["highlight"] = df["Geography"].str.contains(highlight or "")
   
    plot = alt.Chart(df, width=250).mark_bar().encode(
        x=alt.X('Value', axis=alt.Axis(title = metric)),
        y=alt.Y('Geography', axis=alt.Axis(title = 'Census Metropolitan Area (CMA)'), sort = '-x'), 
        color="highlight",
        tooltip='Value'
    ).properties(
        title=violation
    ).to_html()
    return plot


# Canadian provinces map from: https://exploratory.io/map 
# Tutorial used: https://dash-leaflet.herokuapp.com/#geojson 
@app.callback(
   Output('choropleth', 'children'),
   Input('metric_select', 'value'), 
   Input('violation_select', 'value'),
   Input('subviolation_select', 'value'),
   Input('year_select', 'value'))
def generate_choropleth(metric, violation, subcategory, year):     
    """Updates the choropleth map on tab 1 when triggered
    
    Parameters
    -------
    String
        The name of the metric selected from the dropdown
    String
        The violation selected from the dropdown
    String
        The subcategory selected from the dropdown
    Int
        The year selected from the slider
    
    Returns
    -------
    html
        A leaflet choropleth map
    """
    
    geojson = PROVINCES
    df = DATA [
        (DATA["Metric"] == metric) & 
        (DATA["Level1 Violation Flag"] == violation) &
        (DATA["Violation Description"] == subcategory) &
        (DATA["Year"] == year) &
        (DATA['Geo_Level'] == "PROVINCE")
    ]
    
    data_dict = dict(zip(df['Geography'], df['Value']))
    
    for location in geojson['features']:
        try:
            lookup_val = data_dict[location['properties']['PRENAME']]
        except:
            lookup_val = None
        location['properties']['Value'] = lookup_val
        
    num = 13 # number of provinces and territories in Canada
    vals = pd.Series(data_dict.values())
    classes = list(np.linspace(int(vals.min())-0.01, int(vals.max())+0.01, num = num))
    mm =  dict(min = vals.min(), max = vals.max()) 
    
    viridis = cm.get_cmap('viridis', num)
    colorscale = []
    for i in range(viridis.N):
        rgba = viridis(i)
        colorscale.append(matplotlib.colors.rgb2hex(rgba))
    
    style = dict(weight=1, color='black', fillOpacity=0.7)
    hover_style = dict(weight=5, color='orange', dashArray='')
    ns = Namespace("dlx", "choropleth")  
    
    return [ 
        dl.TileLayer(),
        dl.GeoJSON(data=geojson, id="provinces", 
        options=dict(style=ns("style")),
        hideout=dict(colorscale = colorscale[::-1], classes = classes, style = style, colorProp = "Value"),
        hoverStyle=arrow_function(hover_style)),
        dl.Colorbar(colorscale = colorscale[::-1], id = "colorbar", width = 20, height = 150, **mm, position = "bottomleft")
    ]


# Effect of hovering over province. Alternative: click_feature
@app.callback(
    Output("province_info", "children"), 
    Output('highlight', 'value'),
    Input("provinces", "hover_feature"))
def province_hover(feature):
    """Displays information about the map area hovered over
    
    Parameters
    -------
    geojson feature
        The geojson feature being hovered over
    
    Returns
    -------
    html, String
         Html to display on in the info box on the map and the name of the province to hightlight
    """
    intro_message = [
        html.H5("Hover over a Province"), 
        "Hovering over a province will allow you to view details", 
        html.Br(), 
        "and highlight related entries in the CMA plot to the right"
    ]
    
    if feature is not None:
        return [[html.H5(feature['properties']['PRENAME']),  feature['properties']['Value']], feature['properties']['PRENAME']]
    else:
        return [intro_message, None]


# Crime trends plots, tab2
@app.callback(
    Output('crime_trends_plot', 'srcDoc'),
    Input('geo_multi_select', 'value'),
    Input('geo_radio_button', 'value'))
def generate_time_plots(geo_list, geo_level):
    """Updates the time series plots on tab 2 when triggered
    
    Parameters
    -------
    [String]
        List of strings of selected locations
    String
        Radio button selection, CMA or PROVINCE
    
    Returns
    -------
    html
        A 2 by 2 plot 
    """
    metric = "Violations per 100k"
    metric_name = "Violations per 100k"
    
    df = DATA[
        (DATA['Metric'] == 'Rate per 100,000 population') &
        (DATA["Geo_Level"] == geo_level) 
    ]
    df = df[df["Geography"].isin(geo_list)]
    df['Year'] = pd.to_datetime(df['Year'], format='%Y')
    
    category_dict = {
        'Violent Crimes' : 'Total violent Criminal Code violations',
        'Property Crimes' : 'Total property crime violations',
        'Drug Crimes' : 'Total drug violations',
        'Other Criminal Code Violations' : 'Total other Criminal Code violations'
    }
    
    plot_list = []

    for title, description in category_dict.items():
        plot_list.append(
            alt.Chart(df[df['Level1 Violation Flag'] == description], title = title).mark_line().encode(
                x = alt.X('Year'),
                y = alt.Y('Value', type='quantitative', aggregate='sum', title = metric_name),
                tooltip = alt.Tooltip('Value', type='quantitative', aggregate='sum'),
                color = 'Geography').properties(height = 200, width = 300)
        )

    chart = (plot_list[0] | plot_list[2]) & (plot_list[1] | plot_list[3])

    return chart.to_html()


def get_dropdown_values(col, filter=False):
    """Helper function for extracting dropdown option list from given column
    
    Parameters
    -------
    String
        The column to get dropdown options / value for
    
    Returns
    -------
    [[String], String]
        List with two elements, options list and default value based on data
    """
    if filter:
        df = DATA[DATA[filter[0]].isin(filter[1])][col].unique()
    else:
        df = DATA[col].unique()
    return [[{"label": x, "value": x} for x in df], df[0]]
 

@app.callback(
    Output('metric_select', 'options'),
    Output('metric_select', 'value'),
    Output('violation_select', 'options'),
    Output('violation_select', 'value'),
    Input('crime-dashboard-tabs', 'active_tab'))
def set_dropdown_values(__):
    """Set dropdown options for metrics, returns options list and default value for each output
    
    Parameters
    -------
    String
        Tab value provided by trigger, not used
    
    Returns
    -------
    [[String], String]
        List with two elements, options list and default value based on data
    """
    dropdowns = ["Metric", "Level1 Violation Flag"]
    output = []
    for i in dropdowns:
        output += get_dropdown_values(i)
    return output


@app.callback(
    Output('subviolation_select', 'options'),
    Output('subviolation_select', 'value'),
    Input('violation_select', 'value'))
def set_dropdown_values(violation_values):
    """Set dropdown options for violation subcategory, returns options list and default value for each output
    
    Parameters
    -------
    String
        Value from `violation_select` dropdown element (i.e., the selected primariy violation category)
    
    Returns
    -------
    [String], String
        Two elements, options list and default value based on data
    """
    output = get_dropdown_values("Violation Description", filter = ["Level1 Violation Flag", [violation_values]])
    return output

@app.callback(
    Output('geo_multi_select', 'options'),
    Output('geo_multi_select', 'value'),
    Input('crime-dashboard-tabs', 'active_tab'),    
    Input('geo_radio_button', 'value'))
def set_multi_dropdown_values(__, geo_level):
    """Set dropdown options for metrics, returns options list  for each output
    
    Parameters
    -------
    String
        Tab value provided by trigger, not used
    String
        Province level selection of radiobutton, PROVINCE or CMA
    
    Returns
    -------
    [[String], String]
    List with two elements, options list and default value based on data
    """
    
    df = DATA[DATA["Geo_Level"] == geo_level]
    df = df["Geography"].unique()
    df2 = np.sort(df)   # can't call it df without map error
    selected = ['Alberta', 'British Columbia', 'Ontario'] if geo_level == 'PROVINCE' else ['Edmonton, Alberta', 'Vancouver, British Columbia', 'Toronto, Ontario']

    return [{'label': city, 'value': city} for city in df2], selected


if __name__ == '__main__':
    
    # Disable max rows for data sent to altair plots
    alt.data_transformers.disable_max_rows()
    
    app.run_server(debug=True)