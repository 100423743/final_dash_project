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

df_rocks = pd.read_csv('https://query.data.world/s/5iexdkk6ujdrzsih3s3cbymh6pfaeq')
df_fifa = pd.read_csv('https://query.data.world/s/ygkyyhzm7i5umjqdznkigwmtg525ou')


# ROCKS PREPROCESSING

for i in range(3,15):
    df_rocks.columns.values[i]=df_rocks.iloc[0,i]

df_rocks = df_rocks.drop([0], axis=0)

ncol=len(df_rocks.columns)
nrow=df_rocks.shape[0]
null_columns=[]
for i in range(0, ncol):
    if (df_rocks.isnull().sum(axis=0)[i]/nrow)>=0.9:
        null_columns.append(i)

df_rocks = df_rocks.drop(df_rocks.columns.values[null_columns], axis=1)

null_rows=[]
for i in range(0, nrow):
      if (df_rocks.isnull().sum(axis=1)[i+1]/ncol)>=0.5:
          null_rows.append(i+1)
      elif df_rocks.isnull().iloc[i,0]==1:
          df_rocks.iloc[i,0]=df_rocks.iloc[i-1,0]
   
df_rocks = df_rocks.drop(null_rows, axis=0)  

df_rocks = df_rocks.replace(np.nan, "-")
df_rocks = df_rocks.replace("?", "-")
df_rocks = df_rocks.replace("silt v.f. sand", "silt-v.f. sand")
df_rocks =df_rocks.rename(columns={"Grain Size": "grain"})
df_rocks[['grain1','grain2']] = df_rocks.grain.str.split("-",expand=True,)

df_rocks = df_rocks.replace("v.f. sand", "v.f.sand")
df_rocks = df_rocks.replace("v.f sand", "v.f.sand")
df_rocks = df_rocks.replace("f. sand", "f.sand")

df_rocks_long=pd.melt(df_rocks, id_vars=['Core #','Smear Slide #','Depth (cm)','grain1','grain2'],
value_vars=['Quartz','Feldspar', 'Dark Lithics', 'Manganese', 'Forams', 'Sponge Spicules',
       'Carbonate Fragments', 'Pteropods'], var_name='material', value_name='proportion')

# FIFA PREPROCESSING

columns_remove_array=np.concatenate([(0,), (2,), (3,), (7,), (10,),
  np.arange(13,20,1),(21,), np.arange(23,30,1),np.arange(42,92,1)])
   
columns_remove=columns_remove_array.tolist()
   
df_fifa = df_fifa.drop(df_fifa.columns.values[columns_remove], axis=1)

df_fifa = df_fifa.replace("GK", "GOALKEEPER")
df_fifa = df_fifa.replace("LCB", "DEFENDER")
df_fifa = df_fifa.replace("RCB", "DEFENDER")
df_fifa = df_fifa.replace("LB", "DEFENDER")
df_fifa = df_fifa.replace("RB", "DEFENDER")
df_fifa = df_fifa.replace("CB", "DEFENDER")
df_fifa = df_fifa.replace("LWB", "DEFENDER")
df_fifa = df_fifa.replace("RWB", "DEFENDER")
df_fifa = df_fifa.replace("RW", "MIDFIELDER")
df_fifa = df_fifa.replace("LCM", "MIDFIELDER")
df_fifa = df_fifa.replace("CDM", "MIDFIELDER")
df_fifa = df_fifa.replace("LDM", "MIDFIELDER")
df_fifa = df_fifa.replace("CAM", "MIDFIELDER")
df_fifa = df_fifa.replace("RAM", "MIDFIELDER")
df_fifa = df_fifa.replace("LW", "MIDFIELDER")
df_fifa = df_fifa.replace("LAM", "MIDFIELDER")
df_fifa = df_fifa.replace("CM", "MIDFIELDER")
df_fifa = df_fifa.replace("RM", "MIDFIELDER")
df_fifa = df_fifa.replace("LM", "MIDFIELDER")
df_fifa = df_fifa.replace("RDM", "MIDFIELDER")
df_fifa = df_fifa.replace("RCM", "MIDFIELDER")
df_fifa = df_fifa.replace("LS", "STRIKER")
df_fifa = df_fifa.replace("ST", "STRIKER")
df_fifa = df_fifa.replace("RS", "STRIKER")
df_fifa = df_fifa.replace("LF", "STRIKER")
df_fifa = df_fifa.replace("RF", "STRIKER")
df_fifa = df_fifa.replace("CF", "STRIKER")

df_fifa=df_fifa[(df_fifa['club_position']=="GOALKEEPER")|(df_fifa['club_position']=="DEFENDER")|
        (df_fifa['club_position']=="MIDFIELDER")|(df_fifa['club_position']=="STRIKER")]

df_fifa=df_fifa.dropna()

df_fifa=df_fifa.rename(columns={"name": "Name", "age": "Age", "height_cm": "Height",
"weight_kgs": "Weight", "nationality": "Nationality",
"overall_rating": "Overall", "value_euro": "Price", "wage_euro": "Wage",
"club_team": "Team", "club_position": "Position",
"crossing": "Crossing", "finishing":"Finishing", "heading_accuracy":"Heading",
"short_passing":"ShortPassing", "volleys":"Volleys",
"dribbling":"Dribbling", "curve":"Curve", "freekick_accuracy":"Freekick",
"long_passing":"LongPassing", "ball_control":"Control",
"acceleration":"Acceleration", "sprint_speed":"Speed"})
   
df_fifa_long=pd.melt(df_fifa, id_vars=["Name", "Age", "Height", "Weight", "Nationality",
"Overall", "Team", "Position"],
value_vars=["Price", "Wage", "Crossing", "Finishing", "Heading", "ShortPassing", "Volleys",
"Dribbling", "Curve", "Freekick", "LongPassing", "Control", "Acceleration", "Speed"],
            var_name='Stat', value_name='stat_value')


# DASH APP

app.layout= html.Div([
    html.Div([html.H1(app.title, className="app-header--title")],
        className= "app-header",
    ),
    html.Div([  
        dcc.Tabs(id="tabs", value='tab-fifa', 
#        style={
#        'width': '90%',
#        'font-size': '120%',
#        'height': '3vh',
#        'borderBottom': '1px solid #d6d6d6',
#        'padding': '20px',
#        'fontWeight': 'bold',
#        'textAlign': 'center'
#        },
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
#        style={
#        'width': '100%',
#        'font-size': '80%',
#        'height': '3vh',
#        'borderBottom': '1px solid #d6d6d6',
#        'padding': '6px',
#        'fontWeight': 'bold'
#        },
        children=[
            dcc.Tab(label='Stats', value='tab-stats'),
            dcc.Tab(label='Top Players', value='tab-top'),
            dcc.Tab(label='Price Calculator', value='tab-price'),
        ]),
        html.Div(id='fifa-content')
    ],
    className= "app-body")
])

# STATS SELECTOR       
## opt_stat=df_fifa_long['Stat'].sort_values().unique()
# Discrete Colors in Python
# https://plotly.com/python/discrete-color/
### col_stat = {x: px.colors.qualitative.G10[i] for i,x in enumerate(df_stat)}


#### SUBTABS 1 ####

# PLOTS
stats_tab=html.Div([
    html.Div([  
###        html.Label(["Select player stat:", 
###                    dcc.Dropdown('my-dropdown', options= opt_stat, value= [opt_stat[0]['value']], multi=False)
###                ]),
###        html.Div(id='sel_stats', style={'display': 'none'}), # ?????????????????????????????????????
        dcc.Tabs(id="tabs_stats", value='tab-gen', children=[
            dcc.Tab(label='General Rating', value='tab-gen'),
            dcc.Tab(label='Rating per Position', value='tab-pos'),
        ]),
#        html.Div(id='stats-content')
    ],
    className= "app-body")
])


opt_nat=df_fifa['Nationality'].sort_values().unique()
opt_team=df_fifa['Team'].sort_values().unique()

# TABLA
top_tab=html.Div([
    html.Div([
        html.Label(["Select nationality:", 
                    dcc.Dropdown('my-drop-nat', options= opt_nat, value= [opt_nat[0]['value']], multi=False) # TRUE¿?
                ]),
        html.Label(["Select team:", 
                    dcc.Dropdown('my-drop-team', options= opt_team, value= [opt_team[0]['value']], multi=False) # TRUE¿?
                ]),
        html.Div( 
        dash_table.DataTable(
                id='my-table',
                columns=[{"name": i, "id": i} for i in df_fifa.columns],
                data=df_fifa.to_dict("records")
            )
        )
#        html.Div(id='top-content')
    ],
    className= "app-body")
])

# LINEAR MODEL
price_tab=html.Div([
    html.Div([  
        
#        html.Div(id='price-content')
    ],
    className= "app-body")
])


#### SUBTABS 2 ####
gen_tab=html.Div([
    html.Div([  
        

    ],
    className= "app-body")
])


pos_tab=html.Div([
    html.Div([  
        

    ],
    className= "app-body")
])


rocks_tab=html.Div([
    html.Div([  
        dcc.Tabs(id="tabs_sub_rocks", value='tab-char', 
 #       style={
 #       'width': '100%',
 #       'font-size': '80%',
 #       'height': '3vh',
 #       'borderBottom': '1px solid #d6d6d6',
 #       'padding': '6px',
 #       'fontWeight': 'bold'
 #       },
        children=[
            dcc.Tab(label='Characteristics per core', value='tab-char'),
            dcc.Tab(label='Composition per depth', value='tab-comp'),
            dcc.Tab(label='Materials abundance', value='tab-mat'),
        ]),
        html.Div(id='rocks-content')
    ],
    className= "app-body")
])


# CALLBACKS
@app.callback(Output('tabs-content', 'children'),
              Input('tabs', 'value'))
def render_content(tab):
    if tab == 'tab-fifa':
        return fifa_tab
    elif tab == 'tab-rocks':
        return rocks_tab

# CALLBACKS FIFA
@app.callback(Output('fifa-content', 'children'),
              Input('tabs_sub_fifa', 'value'))
def render_content1(tab):
    if tab == 'tab-stats':
        return stats_tab
    elif tab == 'tab-top':
        return top_tab # Tabla filtrada por: Nacionalidad + Stat????????????????
    elif tab == 'tab-price':
        return price_tab # LM MODEL???????????????????


@app.callback(
     Output('my-table', 'data'),
     Input('my-dropdown', 'value'))
def update_data(value):
    filter = df['quality'] == value
    return df[filter].to_dict("records")



@app.callback(Output('stats-content', 'children'),
              Input('tabs_stats', 'value'))
def render_content2(tab):
    if tab == 'tab-gen':
        return gen_tab
    elif tab == 'tab-pos':
        return pos_tab


# CALLBACKS ROCKS




#@app.callback(Output('sel_stats', 'children'), 
#    Input('my-dropdown', 'value'))
#def filter(values):
#     filter = df['Stat'].isin(values) # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#    return df[filter].to_json(date_format='iso', orient='split')

if __name__ == '__main__':
    app.server.run(debug=True)
