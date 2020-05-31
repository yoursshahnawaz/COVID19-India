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

# To skip few entries (index 0 and index 9)
concatenated_range = chain(range(1, 9), range(10, 35))

# Filtering only required information
for j in concatenated_range:
    df.append([covid_current['statewise'][j]['state'],
               covid_current['statewise'][j]['confirmed'],
               covid_current['statewise'][j]['active'],
               covid_current['statewise'][j]['deaths'],
               ])
    df_covid = pd.DataFrame(df, columns=['State', 'Total Case', 'Active Case', 'Deaths'])

# Adding missing data
df2 = pd.DataFrame({'State':['Mizoram'],
                  'Total Case':[1],
                  'Active Case':[1],
                  'Deaths':[0]})
df3 = pd.DataFrame({'State':['Sikkim'],
                    'Total Case':[1],
                    'Active Case':[1],
                  'Deaths':[0]})
df_covid = pd.concat([df_covid, df2])
df_covid = pd.concat([df_covid, df3])

# More filtration to match index of both the files
df_covid = df_covid.sort_values('State', axis=0)
df_covid = df_covid.reset_index(drop=True)

# Converting required data to CSV 
df_covid['State'].iloc[7] = 'Dadra and Nagar Haveli'
df_covid.to_csv('Data/TotalCase.csv')

# Reading CSV Data
pop_df = pd.read_csv('Data/TotalCase.csv')

# Adding total_cases, active_cases, and total_deaths to JSON file (Coordinates' file)
for i in range(35):
    if((geojson_counties['features'][i]['properties']['NAME_1']) == (df_covid['State'][i])):
        geojson_counties['features'][i]['properties']['total_case'] = df_covid['Total Case'][i]
        geojson_counties['features'][i]['properties']['active_case'] = df_covid['Active Case'][i]
        geojson_counties['features'][i]['properties']['total_deaths'] = df_covid['Deaths'][i]

# Choropleth map object
map1 = flm.Map(location=[20.5937,78.9629], zoom_start=4)

# Map Tiles (Different types of maps)
tiles = ['stamenwatercolor', 'cartodbpositron', 'openstreetmap', 'stamenterrain']
for tile in tiles:
    flm.TileLayer(tile).add_to(map1)

choropleth = flm.Choropleth(
    geo_data=geojson_counties,
    name='Total Case',
    data=pop_df,
    columns=['State', 'Total Case'],
    key_on='feature.id',
    fill_color='Set2',
    fill_opacity=0.5,
    line_opacity=0.5,
    nan_fill_color='white',
    nan_fill_opacity=1, 
    line_weight=0.8,
    highlight=True,
    legend_name='State-wise COVID-19 Cases in INDIA',
    ).add_to(map1)

# Adding Hover Effect
style_function = "font-size: 12px; font-weight: bold"
choropleth.geojson.add_child(
    flm.features.GeoJsonTooltip(fields=['NAME_1','total_case','active_case','total_deaths',], aliases=['State', 'Total Case', 'Active', 'Deaths'], lables=True, sticky=True, toLocaleString=True, style=style_function))

# layer control to turn choropleth on or off
flm.LayerControl().add_to(map1)

# display map
map1.save('IndianMap.html')