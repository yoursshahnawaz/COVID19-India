import folium as flm
from folium import plugins
import ipywidgets
import geocoder
import geopy
import numpy as np
import pandas as pd
import json
import requests
from itertools import chain

# load geo_json
with open(r'Data/Indian_States.json') as f:
    geojson_counties = json.load(f)

for i in geojson_counties['features']:
    i['id'] = i['properties']['NAME_1']

# Loading Real-time data via API
res = requests.get('https://api.covid19india.org/data.json')
covid_current = res.json()
df = []

# To skip few entries (index 0 and index 15)
concatenated_range = chain(range(1, 11), range(12, 36))

# Filtering only required information
for j in concatenated_range:
    df.append([covid_current['statewise'][j]['state'],
               covid_current['statewise'][j]['confirmed']])
    df_covid = pd.DataFrame(df, columns=['State', 'Total Case'])

# Converting data to CSV 
df_covid.to_csv('Data/TotalCase.csv')

# Reading CSV Data
pop_df = pd.read_csv('Data/TotalCase.csv')

map1 = flm.Map(location=[20.5937,78.9629], zoom_start=4)

flm.Choropleth(
    geo_data=geojson_counties,
    name='Total Case',
    data=pop_df,
    columns=['State', 'Total Case'],
    key_on='feature.id',
    fill_color='YlGn',
    fill_opacity=0.5,
    line_opacity=0.5).add_to(map1)

# layer control to turn choropleth on or off
flm.LayerControl().add_to(map1)

# display map
map1.save('IndianMap.html')