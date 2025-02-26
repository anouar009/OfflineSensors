import pandas as pd
import os
from datetime import datetime

# Chemins des fichiers et dossiers
machines_file = 'machines.csv'
extracts_folder = 'extracts_folder'
results_file = 'results.csv'

# 1. Lire les Machines
print("Lecture des machines à partir de machines.csv...")
machines_df = pd.read_csv(machines_file)
machines = machines_df['Machine name'].tolist()
print(f"{len(machines)} machines lues.")

# 3. Préparer le dictionnaire des résultats
results_dict = {machine: {} for machine in machines}

# 4. Comparaison des Statuts
# Lister les Fichiers d'Extraction à chaque itération pour s'assurer qu'ils sont à jour
extract_files = [f for f in os.listdir(extracts_folder) if f.endswith('.csv')]
dates = []
for file in extract_files:
    date_str = file.split('_')[-1].split('.')[0]  # MM-DD-YYYY
    try:
        date = datetime.strptime(date_str, '%m-%d-%Y').date()
        dates.append(date.strftime('%m-%d-%Y'))  # Conserver le format MM-DD-YYYY
    except ValueError:
        continue  # Ignore les fichiers qui ne correspondent pas au format

print(f"{len(dates)} fichiers d'extraction trouvés.")

for date in sorted(dates):
    date_str = date
    file_path = os.path.join(extracts_folder, f'EDR_Silent_Sensors_Report_{date_str}.csv')
    
    print(f"Traitement de la date: {date_str}...")

    if os.path.exists(file_path):
        print(f"Lecture du fichier: {file_path}...")
        try:
            extract_df = pd.read_csv(file_path)
            # Parcourir les machines
            for machine in machines:
                if machine in extract_df['Machinename'].values:
                    status = extract_df.loc[extract_df['Machinename'] == machine, 'Current Status'].values[0]
                else:
                    status = 'NotFound'
                results_dict[machine][date_str] = status
        except Exception as e:
            print(f"Erreur lors de la lecture de {file_path}: {e}")
            continue
    else:
        for machine in machines:
            results_dict[machine][date_str] = 'FileAbsent'

print("Analyse terminée.")

# 5. Génération des Résultats
results_df = pd.DataFrame.from_dict(results_dict, orient='index').reset_index()
results_df.columns = ['Machine name'] + dates  # Renommer les colonnes
results_df.to_csv(results_file, index=False)

print(f"Les résultats ont été enregistrés dans {results_file}.")
