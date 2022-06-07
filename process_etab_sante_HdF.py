# imports
import asyncio
from datetime import datetime
import pandas as pd
import requests

# Liste des deps HdF
dep_HdF = ['02','59','60','62','80']
# API to get lat/long
url = "https://api-adresse.data.gouv.fr/search/?q="


# read csv file set column 13 as string
df = pd.read_csv('data\\etalab-cs1100507-stock-20220314-0411.csv',sep=';', skiprows=1, encoding='latin-1', header=None, dtype=str)

# Choisir les departements des HdF (colonne 13)
df_HdF = df[df[13].isin(dep_HdF)]
print(df_HdF.info())

df_HdF.fillna('', inplace=True)

# concat adresse
df_HdF['full_address'] = df_HdF[7] + ' ' + df_HdF[8] + ' ' + df_HdF[9] + ' ' + df_HdF[15]
df_HdF['lat'] = 0
df_HdF['long'] = 0
"""
# loop on address and get lat/long
for i in range(100):
    address = df_HdF.full_address.iloc[i]
    response = requests.get(url + address).json()
    if response['features'] != []:
        df_HdF['lat'].iloc[i] = response['features'][0]['geometry']['coordinates'][1]
        df_HdF['long'].iloc[i] = response['features'][0]['geometry']['coordinates'][0]
    else:
        df_HdF['lat'].iloc[i] = ''
        df_HdF['long'].iloc[i] = ''

print(lat,long, len(lat))
"""
lat = []
long = []
async def get_lat_long(address):
    # get lat/long from API
    try :
        response = requests.get(url + address).json()
        if response['features'] != []:
            lat.append(response['features'][0]['geometry']['coordinates'][1])
            long.append(response['features'][0]['geometry']['coordinates'][0])  
        else:
            lat.append('')
            long.append('')  
    except:
        lat.append('')
        long.append('')
st = datetime.now()
# async loop
async def main():
    task = [asyncio.create_task(get_lat_long(address)) for address in df_HdF['full_address']]
    await asyncio.gather(*task)
    return task

asyncio.run(main())
print(datetime.now() - st)    
df_HdF['lat'] = lat
df_HdF['long'] = long
df_HdF.to_csv('etab_sante_HdF_gps.csv',index=False, encoding='latin-1', sep=';')
# Etablissements avec adresses manquantes (colonnes : 7,8,9)
df_HdF_sans_adresse = df_HdF[(df_HdF[7] == '') & (df_HdF[8] == '') & (df_HdF[9] == '')]
# A supprimer
print(df_HdF_sans_adresse.info())