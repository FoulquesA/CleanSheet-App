# 📑 CleanSheet - Outil de Nettoyage de Données

**Application web interactive pour nettoyer, transformer et analyser vos données facilement.**

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

> 🇬🇧 **[English version available below](#-cleansheet---data-cleaning-tool)** | 🇫🇷 Version française

---

##  Fonctionnalités

###  Profiling & Analyse
- Aperçu complet des données (lignes, colonnes, types, mémoire)
- Détection automatique des valeurs manquantes avec statistiques détaillées
- Analyse des types de données et suggestions de conversion
- Détection d'anomalies (valeurs aberrantes, formats incohérents)
- Visualisations interactives (heatmaps, distributions, boxplots)
- Identification des doublons avec aperçu

###  Transformations Avancées

**Gestion des valeurs manquantes :**
- Remplacement par médiane, moyenne, mode ou valeur fixe
- Propagation avant/arrière (ffill/bfill)
- Suppression intelligente des lignes

**Conversion de types :**
- Numérique (int, float)
- Texte (string)
- Date/Heure (datetime)
- Booléen

**Manipulation texte :**
- Nettoyage (trim, casse, caractères spéciaux)
- Extraction de patterns (emails, téléphones, codes postaux, regex personnalisés)
- Split de colonnes (séparateur, position, regex)
- Find & Replace avancé (texte exact, regex, remplacements multiples)

**Filtrage multi-critères :**
- Filtres numériques (égal, différent, >, <, entre)
- Filtres dates (avant, après, entre)
- Filtres texte (contient, commence par, finit par)
- Combinaison de filtres (opérateur ET)

**Autres :**
- Suppression de doublons (première, dernière, aucune occurrence)
- Formatage décimales par colonne

###  Export & Réutilisabilité

- Export CSV, Excel, JSON
- **Génération automatique de code Python reproductible**
- Templates réutilisables (sauvegarde/chargement de workflows)
- Historique des transformations avec Undo
- Reset complet vers données originales

---

##  Installation

### Prérequis
- Python 3.8 ou supérieur
- pip

### Installation des dépendances
```bash
# Cloner le repository
git clone https://github.com/votre-username/cleansheet.git
cd cleansheet

# Installer les dépendances
pip install -r requirements.txt
```

### Lancement de l'application
```bash
streamlit run app.py
```

L'application s'ouvrira automatiquement dans votre navigateur à `http://localhost:8501`

---

##  Guide d'utilisation

### 1️⃣ Upload de fichier
- Formats supportés : CSV, Excel (.xlsx, .xls), JSON
- Taille maximale : 200 MB
- Encodage automatique (UTF-8, latin-1)

### 2️⃣ Profiling
- Consultez l'onglet **Profiling & Analyse**
- Identifiez les problèmes : valeurs manquantes, doublons, anomalies
- Visualisez la distribution de vos données

### 3️⃣ Transformations
- Naviguez entre les 6 catégories de transformations
- Appliquez les modifications une par une
- Utilisez **Undo** si nécessaire

### 4️⃣ Export
- Téléchargez vos données nettoyées (CSV, Excel, JSON)
- Récupérez le code Python généré automatiquement
- Sauvegardez votre workflow en template

---

##  Architecture
```
cleansheet/
├── app.py                      # Interface principale Streamlit
├── utils/
│   ├── data_loader.py          # Chargement et validation fichiers
│   ├── profiling.py            # Analyse et détection anomalies
│   ├── transformations.py      # Replay et génération code Python
│   └── templates_manager.py    # Gestion templates JSON
├── templates/                  # Templates sauvegardés (créé auto)
├── requirements.txt            # Dépendances Python
└── README.md
```

---

##  Technologies

- **Streamlit** - Framework web interactif
- **Pandas** - Manipulation de données
- **NumPy** - Calculs numériques
- **Plotly** - Visualisations interactives
- **Missingno** - Visualisation valeurs manquantes
- **Matplotlib & Seaborn** - Graphiques statistiques

---

## 📝 Exemples d'utilisation

### Nettoyage CRM
```python
# Workflow typique pour des données clients
1. Remplir NaN dans "Email" par valeur fixe "inconnu@example.com"
2. Convertir "Téléphone" en format texte
3. Supprimer doublons (garder première occurrence)
4. Nettoyer "Nom" : trim + title case
5. Extraire code postal de "Adresse"
→ Sauvegarder comme template "Nettoyage CRM"
```

### Nettoyage E-commerce
```python
# Workflow pour transactions
1. Remplir NaN dans "Prix" par médiane
2. Supprimer lignes avec "Commande" vide
3. Convertir "Date" en datetime
4. Filtrer : Prix > 0 ET Date > 2024-01-01
5. Formater "Prix" avec 2 décimales
→ Export Excel + code Python
```

---

##  Contribution

Les contributions sont les bienvenues ! 

1. Fork le projet
2. Créez votre branche (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

---

## 📜 License

Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)

Ce projet est libre d'utilisation à des fins non-commerciales. Voir le fichier [LICENSE] pour plus de détails.

---

## 👤 Auteur

**Foulques** - Data Analyst
- LinkedIn: [https://www.linkedin.com/in/foulques-arbaretier/]
- GitHub: [https://github.com/FoulquesA]

---

**⭐ N'oubliez pas de mettre une étoile si ce projet vous a été utile !**

---
---
---

# 📑 CleanSheet - Data Cleaning Tool

**Interactive web application to clean, transform and analyze your data easily.**

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

> 🇬🇧 English version | 🇫🇷 **[Version française ci-dessus](#-cleansheet---outil-de-nettoyage-de-données)**

---

##  Features

###  Profiling & Analysis
- Complete data overview (rows, columns, types, memory)
- Automatic missing values detection with detailed statistics
- Data types analysis and conversion suggestions
- Anomaly detection (outliers, inconsistent formats)
- Interactive visualizations (heatmaps, distributions, boxplots)
- Duplicate identification with preview

###  Advanced Transformations

**Missing values handling:**
- Replace with median, mean, mode or fixed value
- Forward/backward fill (ffill/bfill)
- Smart row deletion

**Type conversion:**
- Numeric (int, float)
- Text (string)
- Date/Time (datetime)
- Boolean

**Text manipulation:**
- Cleaning (trim, case, special characters)
- Pattern extraction (emails, phone numbers, postal codes, custom regex)
- Column splitting (separator, position, regex)
- Advanced Find & Replace (exact text, regex, multiple replacements)

**Multi-criteria filtering:**
- Numeric filters (equal, different, >, <, between)
- Date filters (before, after, between)
- Text filters (contains, starts with, ends with)
- Filter combination (AND operator)

**Other:**
- Duplicate removal (first, last, no occurrence)
- Decimal formatting per column

###  Export & Reusability

- CSV, Excel, JSON export
- **Automatic reproducible Python code generation**
- Reusable templates (save/load workflows)
- Transformation history with Undo
- Complete reset to original data

---

##  Installation

### Prerequisites
- Python 3.8 or higher
- pip

### Dependencies installation
```bash
# Clone the repository
git clone https://github.com/your-username/cleansheet.git
cd cleansheet

# Install dependencies
pip install -r requirements.txt
```

### Launch the application
```bash
streamlit run app.py
```

The application will automatically open in your browser at `http://localhost:8501`

---

##  User Guide

### 1️⃣ File Upload
- Supported formats: CSV, Excel (.xlsx, .xls), JSON
- Maximum size: 200 MB
- Automatic encoding (UTF-8, latin-1)

### 2️⃣ Profiling
- Check the **Profiling & Analysis** tab
- Identify issues: missing values, duplicates, anomalies
- Visualize your data distribution

### 3️⃣ Transformations
- Navigate through 6 transformation categories
- Apply changes one by one
- Use **Undo** if needed

### 4️⃣ Export
- Download your cleaned data (CSV, Excel, JSON)
- Get automatically generated Python code
- Save your workflow as a template

---

##  Architecture
```
cleansheet/
├── app.py                      # Main Streamlit interface
├── utils/
│   ├── data_loader.py          # File loading and validation
│   ├── profiling.py            # Analysis and anomaly detection
│   ├── transformations.py      # Replay and Python code generation
│   └── templates_manager.py    # JSON templates management
├── templates/                  # Saved templates (auto-created)
├── requirements.txt            # Python dependencies
└── README.md
```

---

##  Technologies

- **Streamlit** - Interactive web framework
- **Pandas** - Data manipulation
- **NumPy** - Numerical computing
- **Plotly** - Interactive visualizations
- **Missingno** - Missing values visualization
- **Matplotlib & Seaborn** - Statistical charts

---

## 📝 Usage Examples

### CRM Cleaning
```python
# Typical workflow for customer data
1. Fill NaN in "Email" with fixed value "unknown@example.com"
2. Convert "Phone" to text format
3. Remove duplicates (keep first occurrence)
4. Clean "Name": trim + title case
5. Extract postal code from "Address"
→ Save as template "CRM Cleaning"
```

### E-commerce Cleaning
```python
# Workflow for transactions
1. Fill NaN in "Price" with median
2. Delete rows with empty "Order"
3. Convert "Date" to datetime
4. Filter: Price > 0 AND Date > 2024-01-01
5. Format "Price" with 2 decimals
→ Export Excel + Python code
```

---

## 📜 License

Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)

This project is free to use for non-commercial purposes. See [LICENSE] file for details.

---

## 👤 Author

**Foulques** - Data Analyst
- LinkedIn: [https://www.linkedin.com/in/foulques-arbaretier/]
- GitHub: [https://github.com/FoulquesA]

---

**⭐ Don't forget to star if this project was useful to you!**