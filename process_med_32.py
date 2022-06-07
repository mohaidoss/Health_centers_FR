# imports
import pandas as pd

# Liste des deps HdF
dep_HdF = ['02', '59', '60', '62', '80']


df = pd.read_csv('data\\medecins.csv', sep=';', encoding='utf-8',header=0)

# 2\ Extraction CP regex sur les adresses des medecins, pick last match
df['Code Postal'] = df.concat.str.extract(r'(?s:.*)\b(\d{5})\b', expand=False)

# 3\ Filtre les CP HdF
df_reg_32 = df[df['Code Postal'].str[:2].isin(dep_HdF)]
print(df_reg_32.info())

# 1\ Filtre les medecins en reg HdF (code INSEE : 32) (False negatif)
df_reg_32_negatif = df_reg_32[df_reg_32['Code INSEE Région'] != 32]

print(df_reg_32_negatif.info())