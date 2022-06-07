# imports
from bs4 import BeautifulSoup
import pandas as pd
import requests


# url to scrap
target_url = "https://ansm.sante.fr/disponibilites-des-produits-de-sante/medicaments"


# extract the table from url
def extract_table(url):
    # get the html from url
    html = requests.get(url).text
    # create a BeautifulSoup object
    soup = BeautifulSoup(html, 'html.parser')
    # find the table
    table = soup.find('table', attrs={'class': 'table table-products sortable searchable'})
    # return the table
    return table


# convert the table to a dataframe
def table_to_df(table):
    df = pd.read_html(str(table))[0]
    return df


df_stat_med = table_to_df(extract_table(target_url))

# print df.head
print(df_stat_med.head())

# save df to csv using utf-16 encoding
df_stat_med.to_csv('statut_medicaments.csv',index=False, encoding='utf-16')