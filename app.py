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

# df_url_rocks='https://raw.githubusercontent.com/mariacristinasi/class_dash/main/rocks.csv' 
# df_rocks = pd.read_csv(df_url_rocks, error_bad_lines=False)

df_rocks = pd.read_csv('https://query.data.world/s/5iexdkk6ujdrzsih3s3cbymh6pfaeq')


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

# opt_stats=df['stats'].sort_values().unique()

stats_tab=html.Div([
    html.Div([  
        html.Label(["Select types of feeding strategies:", 
            # dcc.Dropdown('my-dropdown', options= opt_stats, value= [opt_stats[0]['value']], multi=True) !!!!!!!!
        ]),
        html.Div(id='sel_stats', style={'display': 'none'}),
        dcc.Tabs(id="tabs_stats", value='tab-gen', children=[
            dcc.Tab(label='General Rating', value='tab-gen'),
            dcc.Tab(label='Rating per Position', value='tab-pos'),
        ]),
        html.Div(id='stats-content')
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
              Input('tabs_sub_fifa', 'value'))
def render_content(tab):
    if tab == 'tab-stats':
        return stats_tab
    elif tab == 'tab-top':
        return top_tab
    elif tab == 'tab-price':
        return price_tab

@app.callback(Output('fifa-content', 'children'),
              Input('tabs_fifa', 'value'))
def render_content(tab):
    if tab == 'tab-fifa':
        return fifa_tab
    elif tab == 'tab-rocks':
        return rocks_tab

#@app.callback(Output('sel_stats', 'children'), 
#    Input('my-dropdown', 'value'))
#def filter(values):
#     filter = df['stats'].isin(values) !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
#    return df[filter].to_json(date_format='iso', orient='split')

if __name__ == '__main__':
    app.server.run(debug=True)
