import geopandas as gpd
import pandas as pd
import os
import folium

files = os.listdir("/")
gdfIsocTot = gpd.GeoDataFrame()
# Read geojson files generated from gen_etab_isochron_CH.py
for file in files:
    gdftransition = gpd.read_file('/'+file)
    gdfIsocTot = pd.concat([gdfIsocTot,gdftransition],ignore_index = True)

gdfIsocTot = gdfIsocTot[gdfIsocTot["value"]==900.0]
gdfIsocTot.reset_index(inplace=True)
gdfIsocTot.explore()
polytot = gdfIsocTot["geometry"][0]
for i in range(1,len(gdfIsocTot)):
    polytot = polytot.union(gdfIsocTot["geometry"][i])

map_osm = folium.Map(location=[49.883113804902585,2.320625169796018])
sim_geo = gpd.GeoSeries(polytot).simplify(tolerance=0.001)
geo_j = sim_geo.to_json()
style_function=lambda x: {'fillColor': '#048b9a'}
geo_j = folium.GeoJson(data=geo_j,
                       style_function=style_function)
#folium.Popup(r['total_pop']).add_to(geo_j)
geo_j.add_to(map_osm)

map_osm