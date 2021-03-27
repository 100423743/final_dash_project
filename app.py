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

# df_url_rocks = 'https://query.data.world/s/xzozlqhuagxyazzgc3avtgcaw2yqxk'
# df_rocks = pd.read_csv(df_url_rocks)




df_url_fifa = "https://query.data.world/s/ygkyyhzm7i5umjqdznkigwmtg525ou"
df_fifa = pd.read_csv(df_url_fifa)






app.layout= html.Div([
    html.Div([html.H1(app.title, className="app-header--title")],
        className= "app-header",
    ),
    html.Div([  
        dcc.Tabs(id="tabs", value='tab-fifa', 
        style={
        'width': '90%',
        'font-size': '120%',
        'height': '3vh',
        'borderBottom': '1px solid #d6d6d6',
        'padding': '20px',
        'fontWeight': 'bold',
        'textAlign': 'center'
        },
        children=[
            dcc.Tab(label='FIFA', value='tab-fifa'),
            dcc.Tab(label='Rocks', value='tab-rocks'),
        ]),
        html.Div(id='tabs-content')
    ],
    className= "app-body")
])

fifa_tab=html.Div([
    html.Div([  
        dcc.Tabs(id="tabs_sub_fifa", value='tab-stats', 
        style={
        'width': '100%',
        'font-size': '80%',
        'height': '3vh',
        'borderBottom': '1px solid #d6d6d6',
        'padding': '6px',
        'fontWeight': 'bold'
        },
        children=[
            dcc.Tab(label='Stats', value='tab-stats'),
            dcc.Tab(label='Top Players', value='tab-top'),
            dcc.Tab(label='Price Calculator', value='tab-price'),
        ]),
        html.Div(id='fifa-content')
    ],
    className= "app-body")
])

## STATS SELECTOR
        html.Label(["Select player stat:", 
                    dcc.Dropdown('my-dropdown', options= opt_stat, value= [opt_stat[0]['value']], multi=False)
                ]),

        df_stat = df_fifa['Stat'].sort_values().unique()
        opt_stat = [{'label': x + 'Stat', 'value': x} for x in df_stat]
        # Discrete Colors in Python
        # https://plotly.com/python/discrete-color/
        col_stat = {x: px.colors.qualitative.G10[i] for i,x in enumerate(df_stat)}


rocks_tab=html.Div([
    html.Div([  
        dcc.Tabs(id="tabs_sub_rocks", value='tab-char', 
        style={
        'width': '100%',
        'font-size': '80%',
        'height': '3vh',
        'borderBottom': '1px solid #d6d6d6',
        'padding': '6px',
        'fontWeight': 'bold'
        },
        children=[
            dcc.Tab(label='Characteristics per core', value='tab-char'),
            dcc.Tab(label='Composition per depth', value='tab-comp'),
            dcc.Tab(label='Materials abundance', value='tab-mat'),
        ]),
        html.Div(id='rocks-content')
    ],
    className= "app-body")
])

# table_tab = dash_table.DataTable(
#                id='my-table',
#                columns=[{"name": i, "id": i} for i in df_fifa.columns]
#            )

@app.callback(Output('tabs-content', 'children'),
              Input('tabs', 'value'))
def render_content(tab):
    if tab == 'tab-fifa':
        return fifa_tab
    elif tab == 'tab-rocks':
        return rocks_tab

if __name__ == '__main__':
    app.server.run(debug=True)
