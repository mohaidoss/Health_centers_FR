# Description des fichiers *.py*

### Scripts

- `gen_etab_isochron_CH.py` : Génère des zones isochrones de 5, 15, 30 minutes en utilisant OpenRouteService API autours des Centres Hospitaliers, Centres Hospitaliers Régional et les ex Hopitaux Locaux.
<p align="center">
⚠️ MISSING PERSONAL TOKEN `Authorization: XXXXXXX` ⚠️
</p>

-  `med_dep_HdF.py` : Process le dataset des médecins de l'annuaire santé (Code postaux des départements HdF) pour corriger les colonnes *Commune, code_insee, Code INSEE Département, Code INSEE Région, lat, long* à l'aide de l'API https://adresse.data.gouv.fr/

- `process_etab_sante_HdF.py` : Utilise l'API https://adresse.data.gouv.fr/ pour trouver les coordonnées GPS (*lat, long*) des établissements de santé HdF

- `scrap_med.py` : scraping du dataset des médicaments en rupture de stock ([ANSM](https://ansm.sante.fr/disponibilites-des-produits-de-sante/medicaments))

### Discovery

- `process_med_32.py` : Script pour découvrir le nombre des False Negatif (Médecins qui se trouvent en HdF mais la colonne *Région* n'est pas juste)

- `process_med_HdF.py` : Script pour découvrir le nombre des False Positif (Médecins qui ne se trouvent pas en HdF mais la colonne *Région* dit qu'ils le sont)
