# author: Steffen Pentelow and Sasha Babicki
# date: 2021-01-22
"""
Module to generate tab 1: Geographic Crime Comparisons
"""

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash_leaflet as dl

# links to add later


def generate_layout():
    """Generate tab 1 layout

    Returns
    -------
    dbc.Container
        Container with the html content of the page
    """
    
    dropdown_height = 70
    start_year = 1998
    end_year = 2019
    year_range = list(range(start_year, end_year+1,3))
    slider_marks = dict(zip(
        year_range,
        [str(x) for x in year_range]
         ))
    years = [{"label": x, "value": x} for x in range(start_year, end_year)]
    
    return dbc.Container(
        [
            dbc.Row(
                [
                    # Column 1
                    dbc.Col(
                        [
                            dbc.Row(
                                [
                                    html.Div(
                                        [
                                            "Select Crime Measurement",
                                            dcc.Dropdown(
                                                id="metric_select",
                                                optionHeight=dropdown_height,
                                                clearable=False
                                            ),
                                        ],
                                        style={"width": "100%"},
                                    ),
                                ]
                            ),
                            html.Br(),
                            dbc.Row(
                                [
                                    html.Div(
                                        [
                                            "Select Crime Grouping",
                                            dcc.Dropdown(
                                                id="violation_select",
                                                optionHeight=dropdown_height,
                                                clearable=False
                                            ),
                                        ],
                                        style={"width": "100%"},
                                    ),
                                ]
                            ),
                            html.Br(),
                            dbc.Row(
                                [
                                    html.Div(
                                        [
                                            "Select Violation Subcategory",
                                            dcc.Dropdown(
                                                id="subviolation_select",
                                                optionHeight=dropdown_height,
                                                clearable=False
                                            ),
                                        ],
                                        style={"width": "100%"},
                                    ),
                                ]
                            ),
                            html.Br(),
                            dbc.Row(
                                [
                                    html.Div(
                                        [
                                            "Select Year of Interest",
                                            dcc.Slider(
                                                id="year_select",
                                                min = start_year, 
                                                max = end_year,
                                                step = 1,
                                                value =2019, 
                                                dots = True,
                                                included=False,
                                                tooltip = {"placement": "top"},
                                                marks = slider_marks
                                                )
                                        ], 
                                        style = {"width": "100%"},
                                    ),
                                ]
                            ),
                            html.Br(),
                            dbc.Row(
                                [
                                     dbc.Col(
                                        [
                                            html.H5("About this Dashboard"),
                                            dcc.Markdown(['''This Dashboard has been designed to give Canadians 
                                            easy access to police-reported crime statistics so they can better understand 
                                            the state of public safety in their community and across the country. 
                                            Data visualizations have been organized to let users compare a multitude of crime 
                                            types across Census Metropolitian Areas (CMAs), provinces, and across time.
                                            '''],
        
                                            style = {'color': 'grey',
                                                     'font-size': '12px'}),
                                            
                                            html.Br(),
                                            dcc.Markdown(['''All data shown on this dashboard is sourced from Statistics Canada, 
                                            specifically [table 35-10-0177-01](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=3510017701).
                                            Data is subject to the Uniform-Crime-Reporting (UCR2) standard, insuring that data is collected 
                                            and reported reliably and consistently by Canada's various police agencies.
                                            All data and coding for this project is publicly available at this 
                                            [Github repository](https://github.com/UBC-MDS/532_Group_22).
                                            '''],
        
                                            style = {'color': 'grey',
                                                     'font-size': '12px'}),        

                                        ],
                                        style = {'background-color': '#e6e6e6',
                                                'padding': 15,
                                                'border-radius': 3}
                                    )
                                ]
                            ),
                        ],

                        style={'padding-left': '2%'}                    
                    ),
                    
                    # Column 2
                    dbc.Col(
                        dbc.Row(
                            [
                                html.Div(html.H5("Violation Subcategory by Province")),
                                html.Div(
                                    [
                                        #dcc.Graph(id="choropleth"),
                                        dl.Map(id="choropleth", 
                                        center=[62, -98],
                                        zoom=3,
                                        style={'width': '550px', 'height': '600px'}),
                                        html.Div(#[dcc.Dropdown(id = "year_select", options = years)],
                                            id="province_info",className="info",
                                            style={"position": "absolute", 
                                                "top": "40px", 
                                                "right": "2%", 
                                                "z-index": "1000"}
                                        ),
                                        html.Div(id="highlight")
                                                
                                    ]
                                ),
                            ]
                        ),
                        style={'padding-left': '2%'}
                    ),
                    
                    # Column 3
                    dbc.Col(
                        dbc.Row(
                            [
                                html.Div(html.H5("Violation Subcategory by CMA")),
                                html.Iframe(
                                    id='cma_barplot',
                                    style={'border-width': '0', 'width': '100%', 'height': '800px'}
                                )
                            ]
                        ),
                        width="auto",
                        style={'padding-left': '2%', 'padding-right': '2%'}
                    ),
                ]
            )
        ], 
        fluid=True
    )