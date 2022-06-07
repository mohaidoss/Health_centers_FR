# imports
import pandas as pd

# Liste des deps HdF
dep_HdF = ['02', '59', '60', '62', '80']

# Lecture du fichier complet
df = pd.read_csv('data\\medecins.csv', sep=';', encoding='utf-8',header=0)

# 2\ Extraction Code Postal avec regex sur les adresses des medecins (pick last match)
df['Code Postal'] = df.concat.str.extract(r'(?s:.*)\b(\d{5})\b', expand=False)

# 3\ Selection des medecins en HdF
df_med_32 = df[df['Code Postal'].str[:2].isin(dep_HdF)]
# nb lignes
print(df_med_32.shape[0])

# split colonne coordonnées en 2 colonnes lat et long
df_med_32[['lat','long']] = df_med_32['Coordonnées'].str.split(',', n=1, expand=True)

# Selection des medecins HdF qui ont la mauvaise région (False Negatives)
df_med_32_negatif = df_med_32[df_med_32['Code INSEE Région'] != 32]

print(df_med_32_negatif.head())

###############################################################################
###############################################################################

# Correction des informations en utilisant l'API adresse.gouv
url = "https://api-adresse.data.gouv.fr/search/?q="

import asyncio
from datetime import datetime
import requests

lat_correction = []
long_correction = []
commune_correction = []
codeINSEE_com_correction = []
departement_correction = []
codeINSEE_dep_correction = []

async def get_lat_long(address, code_postal):
    # get lat/long from API
    try :
        response = requests.get(url + address + "&postcode="+code_postal).json()
        if response['features'] != []:
            lat_correction.append(response['features'][0]['geometry']['coordinates'][1])
            long_correction.append(response['features'][0]['geometry']['coordinates'][0])  
            commune_correction.append(response['features'][0]['properties']['city'])
            codeINSEE_com_correction.append(response['features'][0]['properties']['citycode'])
            codeINSEE_dep_correction.append(response['features'][0]['properties']['context'][:2])
        else:
            lat_correction.append('')
            long_correction.append('')
            commune_correction.append('')
            codeINSEE_com_correction.append('')
            codeINSEE_dep_correction.append('')
    except:
        lat_correction.append('')
        long_correction.append('')
        commune_correction.append('')
        codeINSEE_com_correction.append('')
        codeINSEE_dep_correction.append('')

st = datetime.now()

# async loop
async def main():
    task = [asyncio.create_task(get_lat_long(address, code_postal)) for address, code_postal in zip(df_med_32_negatif['Adresse'], df_med_32_negatif['Code Postal'])]
    await asyncio.gather(*task)
    return task

asyncio.run(main())
print(datetime.now() - st)


df_med_32_negatif['lat'] = lat_correction
df_med_32_negatif['long'] = long_correction
df_med_32_negatif['Commune'] = commune_correction
df_med_32_negatif['code_insee'] = codeINSEE_com_correction
df_med_32_negatif['Code INSEE Département'] = codeINSEE_dep_correction
df_med_32_negatif['Code INSEE Région'] = 32
st = datetime.now()
df_med_32.update(df_med_32_negatif)
print(datetime.now() - st)

# Fin et verif
print(df_med_32.shape[0])
df_med_32.to_csv('med_HdF_corrected_gps.csv',index=False, encoding='utf-8', sep=';')

