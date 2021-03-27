import dash
import dash_html_components as html
import dash_core_components as dcc

import pandas as pd

df_url_rocks = 'https://query.data.world/s/xzozlqhuagxyazzgc3avtgcaw2yqxk'
df_rocks = pd.read_csv(df_url_rocks)