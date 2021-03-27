import dash
import dash_html_components as html
import dash_core_components as dcc

import pandas as pd


app = dash.Dash(__name__, title="Dash Project - Ignacio Medina & María Cristina Sánchez")

df_url_rocks = 'https://query.data.world/s/xzozlqhuagxyazzgc3avtgcaw2yqxk'
df_rocks = pd.read_csv(df_url_rocks)

df_url_fifa = 'https://query.data.world/s/457fikckeqdoemry75fqfhjoqwtrxv'
df_fifa = pd.read_csv(df_url_fifa)

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



