import dash
from dash.dependencies import Input, Output, State

import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
import dash_bootstrap_components as dbc
import dash_table

import numpy as np
import pandas as pd
import json


app = dash.Dash(__name__, title="Dash Project - Ignacio Medina & María Cristina Sánchez")

df_url_rocks = 'https://query.data.world/s/xzozlqhuagxyazzgc3avtgcaw2yqxk'
df_rocks = pd.read_csv(df_url_rocks)

app.layout= html.Div([
    html.Div([html.H1(app.title, className="app-header--title")],
        className= "app-header",
    ),
    html.Div([  
        dcc.Tabs(id="tabs", value='tab-fifa', children=[
            dcc.Tab(label='FIFA', value='tab-fifa'),
            dcc.Tab(label='Rocks', value='tab-rocks'),
        ]),
        html.Div(id='tabs-content')
    ],
    className= "app-body")
])

fifa_tab=html.Div([
    html.Div([  
        dcc.Tabs(id="tabs_sub_fifa", value='tab-stats', children=[
            dcc.Tab(label='Stats', value='tab-stats'),
            dcc.Tab(label='Top Players', value='tab-top'),
            dcc.Tab(label='Price Calculator', value='tab-price'),
        ]),
        html.Div(id='fifa-content')
    ],
    className= "app-body")
])

rocks_tab=html.Div([
    html.Div([  
        dcc.Tabs(id="tabs_sub_rocks", value='tab-char', children=[
            dcc.Tab(label='Characteristics per core', value='tab-char'),
            dcc.Tab(label='Composition per depth', value='tab-comp'),
            dcc.Tab(label='Materials abundance', value='tab-mat'),
        ]),
        html.Div(id='rocks-content')
    ],
    className= "app-body")
])

@app.callback(Output('tabs-content', 'children'),
              Input('tabs', 'value'))
def render_content(tab):
    if tab == 'tab-fifa':
        return fifa_tab
    elif tab == 'tab-rocks':
        return rocks_tab