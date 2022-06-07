# imports
import numpy as np
import pandas as pd
import requests
import time

# Headers
headers = {
    "Accept": "application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8",
    "Authorization": "",
    "Content-Type": "application/json; charset=utf-8"
}

# Json body
body = {
    "range": [300, 900, 1800],
    "attributes": ["area", "reachfactor", "total_pop"],
    "range_type": "time"
}

# Post url
url = "https://api.openrouteservice.org/v2/isochrones/driving-car"


############################################## Locations file ##############################################
# Read etab_sante_HdF.csv
df = pd.read_csv("data/etab_sante_HdF_gps.csv", sep=";", encoding="latin-1", header=0, dtype=str)
# Filtre sur type d'etablissement CH,CHR,ex Hopital local : 355,101,106 
df = df[df['18'].isin(["355","101","106"])][['long','lat']]
# convert df into python matrix
df.dropna(axis=0, inplace=True)
# change column type from string to float
df.astype(np.float64)
# list of lat/long to get isochrone
list_gps_etab = df.to_numpy(dtype=np.float64).tolist()

############################################## Main ##############################################
# 5 locations per request
for i in range((len(list_gps_etab)//5)+1):
    body["locations"] = list_gps_etab[i*5:(i+1)*5]
    call = requests.post(url, json=body, headers=headers)
    with open('data/isoc_' + str(i) + '.geojson','w',encoding='utf-8') as outfile:
        outfile.write(call.text)
    # limit of 20 calls per minute
    time.sleep(3)