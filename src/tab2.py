# author: Ifeanyi Anene and Cal Schafer 
# date: 2021-01-22
"""
Module to generate tab 1: Geographic Crime Comparisons
"""

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import numpy as np
import pandas as pd
import altair as alt
import datetime
import dash_bootstrap_components as dbc

def generate_layout():
    """Generate tab 2 layout

    Returns
    -------
    dbc.Container
        Container with the html content of the page
    """
    
    return dbc.Container([

        ### 1st Row 
        dbc.Row([
            ### 1st column
            dbc.Col([
                dbc.Row(
                    [
                        html.Div(
                            [
                                "Select Province or CMA",
                                dcc.RadioItems(
                                    id='geo_radio_button',
                                    options=[
                                        {'label': 'Province', 'value': 'PROVINCE'},
                                        {'label': 'CMA', 'value': 'CMA'},
                                    ],
                                    value='PROVINCE', 
                                    labelStyle={'margin-left': '10px', 'margin-right': '10px'}
                                )
                            ],
                            style={"width": "100%"},
                        )
                        
                    ],
                ),
                dbc.Row(
                    [
                        html.Div(
                            [
                                "Select Locations to Display",
                                dcc.Dropdown(
                                    id = 'geo_multi_select',
                                    multi = True
                                ),
                            ],
                            style={"width": "100%"},
                        )
                    ]
                ),
                html.Br(),
                # NEW
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
                                    'border-radius': 3,
                                    'padding-left': '2%'}
                        )
                    ]
                )
## END


              ],
              style={'padding-left': '2%'},
              width=3
              ),



              
              
              
              dbc.Col([
                html.Iframe(
                    id = 'crime_trends_plot',
                    style = {'border-width': '0', 'width': '100%', 'height': '800px'}
                )
            ], 
            style={'padding-left': '2%'},
            )
        ])
    ],
    fluid=True)