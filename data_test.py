import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Génération de données de test pour CleanSheet
np.random.seed(42)

# Nombre de lignes
n_rows = 200

# Création du DataFrame avec tous les problèmes possibles
data = {
    # Colonne ID (propre, sans problème)
    'ID': range(1, n_rows + 1),
    
    # Colonne Nom (avec NaN et doublons)
    'Nom': [f'Client_{i}' for i in range(1, n_rows + 1)],
    
    # Colonne Email (avec formats incohérents et NaN)
    'Email': [
        f'client{i}@example.com' if i % 5 != 0 else None 
        for i in range(1, n_rows + 1)
    ],
    
    # Colonne Age (avec valeurs aberrantes et NaN)
    'Age': [
        np.random.randint(18, 80) if i % 7 != 0 else None 
        for i in range(1, n_rows + 1)
    ],
    
    # Colonne Prix (avec symboles €, virgules, et NaN)
    'Prix': [
        f"{np.random.randint(10, 1000)}€" if i % 3 == 0
        else str(np.random.randint(10, 1000)) if i % 3 == 1
        else None if i % 10 == 0
        else f"{np.random.randint(10, 1000)}.{np.random.randint(10, 99)}"
        for i in range(1, n_rows + 1)
    ],
    
    # Colonne Montant (numérique mais avec NaN et outliers)
    'Montant': [
        np.random.uniform(10, 500) if i % 8 != 0
        else 999999 if i % 50 == 0  # Outlier volontaire
        else None
        for i in range(1, n_rows + 1)
    ],
    
    # Colonne Date (formats multiples et incohérents)
    'Date_Achat': [],
    
    # Colonne Pays (catégorielle avec NaN)
    'Pays': [
        np.random.choice(['France', 'Belgique', 'Suisse', 'Canada', None], p=[0.4, 0.2, 0.2, 0.15, 0.05])
        for _ in range(n_rows)
    ],
    
    # Colonne Statut (catégorielle avec typos)
    'Statut': [
        np.random.choice(['Actif', 'actif', 'ACTIF', 'Inactif', 'inactif', 'En attente', None], 
                         p=[0.3, 0.2, 0.1, 0.15, 0.1, 0.1, 0.05])
        for _ in range(n_rows)
    ],
    
    # Colonne Quantité (devrait être int mais contient des strings)
    'Quantite': [
        str(np.random.randint(1, 100)) if i % 15 != 0
        else f"{np.random.randint(1, 100)} unités" if i % 20 == 0
        else None
        for i in range(1, n_rows + 1)
    ],
}

# Génération des dates avec formats variés
base_date = datetime(2024, 1, 1)
dates = []
for i in range(n_rows):
    if i % 10 == 0:
        dates.append(None)  # NaN
    elif i % 4 == 0:
        dates.append((base_date + timedelta(days=i)).strftime('%d/%m/%Y'))  # Format DD/MM/YYYY
    elif i % 4 == 1:
        dates.append((base_date + timedelta(days=i)).strftime('%Y-%m-%d'))  # Format YYYY-MM-DD
    elif i % 4 == 2:
        dates.append((base_date + timedelta(days=i)).strftime('%m/%d/%Y'))  # Format MM/DD/YYYY
    else:
        dates.append((base_date + timedelta(days=i)).strftime('%d.%m.%Y'))  # Format DD.MM.YYYY

data['Date_Achat'] = dates

# Création du DataFrame
df = pd.DataFrame(data)

# Ajout de doublons volontaires (10% de lignes dupliquées)
duplicates = df.sample(n=20, random_state=42)
df = pd.concat([df, duplicates], ignore_index=True)

# Shuffle pour mélanger les doublons
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# Ajout de quelques outliers supplémentaires dans Age
df.loc[df.sample(5, random_state=42).index, 'Age'] = [150, 5, 200, 0, -10]

# Sauvegarde en CSV
df.to_csv('data/test_data_cleansheet.csv', index=False, encoding='utf-8')

print("✅ Fichier de test généré")