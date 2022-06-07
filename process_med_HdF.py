# imports
import pandas as pd

# Liste des deps HdF
dep_HdF = ['02', '59', '60', '62', '80']


df = pd.read_csv('data\\medecins.csv', sep=';', encoding='utf-8',header=0)

# 1\ Filtre les medecins en reg HdF (code INSEE : 32)
df_reg_HdF = df[df['Code INSEE Région'] == 32]
print(df_reg_HdF.info())

# 2\ Extraction CP regex sur les adresses des medecins
df_reg_HdF['Code Postal'] = df_reg_HdF.concat.str.extract(r'(?s:.*)\b(\d{5})\b', expand=False)

# 3\ Filtre les CP hors HdF (False positif)
df_reg_HdF_false = df_reg_HdF[~df_reg_HdF['Code Postal'].str[:2].isin(dep_HdF)]

print(df_reg_HdF_false.info())