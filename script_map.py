import folium as flm
from folium import plugins
import ipywidgets
import geocoder
import geopy
import numpy as np
import pandas as pd
import json

# load geo_json
# shapefiles can be converted to geojson with QGIS
with open(r'Data/Indian_States.json') as f:
    geojson_counties = json.load(f)

for i in geojson_counties['features']:
    i['id'] = i['properties']['NAME_1']
    
# load data associated with geo_json
pop_df = pd.read_excel(r'Data/data_excel.xlsx')
pop_df.head()

map1 = flm.Map(location=[20.5937,78.9629], zoom_start=4)

flm.Choropleth(
    geo_data=geojson_counties,
    name='choropleth',
    data=pop_df,
    columns=['Name of State / UT', 'Total Confirmed cases'],
    # see folium.Choropleth? for details on key_on
    key_on='feature.id',
    fill_color='YlGn',
    fill_opacity=0.5,
    line_opacity=0.5).add_to(map1)

# layer control to turn choropleth on or off
flm.LayerControl().add_to(map1)

# display map
map1.save('IndianMap.html')