"""
Module de gestion des transformations.
Gère le replay et la génération de code Python.
"""

import pandas as pd


def replay_transformation(df_copy, transformation):
    """
    Rejoue une transformation sur un DataFrame avec gestion d'erreurs.
    
    Args:
        df_copy: DataFrame sur lequel appliquer la transformation
        transformation: Dict contenant les infos de la transformation
        
    Returns:
        DataFrame transformé ou DataFrame original si erreur
    """
    try:
        trans_type = transformation['type']
        
        # Remplissage valeurs manquantes
        if trans_type in ['fill_na', 'fill_na_numeric', 'fill_na_categorical']:
            col = transformation['column']
            
            # Validation : colonne existe
            if col not in df_copy.columns:
                st.warning(f" Colonne '{col}' introuvable, transformation ignorée")
                return df_copy
            
            strategy = transformation.get('strategy', transformation.get('method', ''))
            
            if strategy in ['supprimer les lignes', 'Supprimer les lignes']:
                df_copy = df_copy.dropna(subset=[col])
            elif strategy in ['valeur fixe', 'Valeur fixe']:
                fill_value = transformation.get('fill_value')
                if fill_value is not None:
                    df_copy[col].fillna(fill_value, inplace=True)
            elif strategy in ['médiane', 'Médiane']:
                if df_copy[col].dtype in ['int64', 'float64']:
                    median_val = df_copy[col].median()
                    if pd.notna(median_val):
                        df_copy[col].fillna(median_val, inplace=True)
                else:
                    st.warning(f" Impossible de calculer la médiane pour '{col}' (type non numérique)")
            elif strategy in ['moyenne', 'Moyenne']:
                if df_copy[col].dtype in ['int64', 'float64']:
                    mean_val = df_copy[col].mean()
                    if pd.notna(mean_val):
                        df_copy[col].fillna(mean_val, inplace=True)
                else:
                    st.warning(f" Impossible de calculer la moyenne pour '{col}' (type non numérique)")
            elif strategy in ['mode (valeur la plus fréquente)', 'Mode (valeur la plus fréquente)']:
                mode_series = df_copy[col].mode()
                if len(mode_series) > 0:
                    df_copy[col].fillna(mode_series[0], inplace=True)
            elif strategy == 'Propagation avant (ffill)':
                df_copy[col].fillna(method='ffill', inplace=True)
            elif strategy == 'Propagation arrière (bfill)':
                df_copy[col].fillna(method='bfill', inplace=True)
        
        # Conversion de types
        elif trans_type == 'convert_type':
            col = transformation['column']
            
            if col not in df_copy.columns:
                st.warning(f" Colonne '{col}' introuvable, transformation ignorée")
                return df_copy
            
            target_type = transformation['target_type']
            
            try:
                if target_type == 'Entier (int)':
                    df_copy[col] = pd.to_numeric(df_copy[col], errors='coerce').fillna(0).astype(int)
                elif target_type == 'Décimal (float)':
                    df_copy[col] = pd.to_numeric(df_copy[col], errors='coerce')
                elif target_type == 'Texte (string)':
                    df_copy[col] = df_copy[col].astype(str)
                elif target_type == 'Date (datetime)':
                    df_copy[col] = pd.to_datetime(df_copy[col], errors='coerce')
                elif target_type == 'Booléen (bool)':
                    df_copy[col] = df_copy[col].astype(bool)
            except Exception as e:
                st.warning(f" Erreur de conversion pour '{col}' : {str(e)}")
        
        # Suppression doublons
        elif trans_type == 'drop_duplicates':
            keep = transformation['keep']
            keep_map = {'première': 'first', 'dernière': 'last', 'aucune': False}
            df_copy = df_copy.drop_duplicates(keep=keep_map[keep])
        
        # Formatage décimales
        elif trans_type == 'format_decimals':
            col = transformation['column']
            
            if col not in df_copy.columns:
                st.warning(f" Colonne '{col}' introuvable, transformation ignorée")
                return df_copy
            
            decimals = transformation['decimals']
            
            if df_copy[col].dtype in ['int64', 'float64']:
                df_copy[col] = df_copy[col].round(decimals)
            else:
                st.warning(f" Colonne '{col}' n'est pas numérique, formatage ignoré")
        
        # Nettoyage texte
        elif trans_type == 'text_cleaning':
            col = transformation['column']
            
            if col not in df_copy.columns:
                st.warning(f" Colonne '{col}' introuvable, transformation ignorée")
                return df_copy
            
            operation = transformation['operation']
            
            if operation == "Supprimer espaces début/fin (trim)":
                df_copy[col] = df_copy[col].str.strip()
            elif operation == "Convertir en minuscules":
                df_copy[col] = df_copy[col].str.lower()
            elif operation == "Convertir en majuscules":
                df_copy[col] = df_copy[col].str.upper()
            elif operation == "Convertir en title case (Première Lettre Majuscule)":
                df_copy[col] = df_copy[col].str.title()
            elif operation == "Remplacer une valeur":
                replace_from = transformation['replace_from']
                replace_to = transformation['replace_to']
                if replace_from and replace_to is not None:
                    df_copy[col] = df_copy[col].str.replace(replace_from, replace_to, regex=False)
            elif operation == "Supprimer caractères spéciaux":
                df_copy[col] = df_copy[col].str.replace(r'[^a-zA-Z0-9\s]', '', regex=True)
        
        # Extraction pattern
        elif trans_type == 'extract_pattern':
            source_col = transformation['source_column']
            new_col = transformation['new_column']
            pattern = transformation['pattern']
            
            if source_col not in df_copy.columns:
                st.warning(f" Colonne '{source_col}' introuvable, transformation ignorée")
                return df_copy
            
            try:
                if '(' in pattern and ')' in pattern:
                    df_copy[new_col] = df_copy[source_col].str.extract(pattern, expand=False)
                else:
                    df_copy[new_col] = df_copy[source_col].str.extract(f'({pattern})', expand=False)
            except Exception as e:
                st.warning(f" Erreur d'extraction regex : {str(e)}")
        
        # Split colonnes
        elif trans_type == 'split_column':
            source_col = transformation['source_column']
            new_cols = transformation['new_columns']
            split_method = transformation['split_method']
            
            if source_col not in df_copy.columns:
                st.warning(f" Colonne '{source_col}' introuvable, transformation ignorée")
                return df_copy
            
            try:
                if split_method == 'separator':
                    separator = transformation['separator']
                    n_splits = transformation['n_splits']
                    split_data = df_copy[source_col].str.split(separator, n=n_splits-1, expand=True)
                    
                    for i, col_name in enumerate(new_cols):
                        if i < split_data.shape[1]:
                            df_copy[col_name] = split_data[i]
                        else:
                            df_copy[col_name] = None
                
                elif split_method == 'position':
                    position = transformation['position']
                    df_copy[new_cols[0]] = df_copy[source_col].str[:position]
                    df_copy[new_cols[1]] = df_copy[source_col].str[position:].str.strip()
                
                elif split_method == 'regex':
                    pattern = transformation['pattern']
                    n_splits = transformation['n_splits']
                    split_data = df_copy[source_col].str.split(pattern, n=n_splits-1, expand=True, regex=True)
                    
                    for i, col_name in enumerate(new_cols):
                        if i < split_data.shape[1]:
                            df_copy[col_name] = split_data[i]
                        else:
                            df_copy[col_name] = None
            except Exception as e:
                st.warning(f" Erreur de split : {str(e)}")
        
        # Find & Replace avancé
        elif trans_type == 'find_replace':
            col = transformation['column']
            
            if col not in df_copy.columns:
                st.warning(f" Colonne '{col}' introuvable, transformation ignorée")
                return df_copy
            
            method = transformation['method']
            
            try:
                if method == 'exact':
                    search = transformation['search']
                    replace = transformation['replace']
                    case_sensitive = transformation.get('case_sensitive', False)
                    df_copy[col] = df_copy[col].str.replace(search, replace, case=case_sensitive, regex=False)
                    
                elif method == 'regex':
                    pattern = transformation['pattern']
                    replace = transformation['replace']
                    df_copy[col] = df_copy[col].str.replace(pattern, replace, regex=True)
                    
                elif method == 'multiple':
                    replacements = transformation['replacements']
                    for r in replacements:
                        df_copy[col] = df_copy[col].str.replace(r['search'], r['replace'], regex=False)
            except Exception as e:
                st.warning(f" Erreur de remplacement : {str(e)}")
        
        # Filtrage de lignes
        elif trans_type == 'filter_rows':
            filters = transformation['filters']
            
            for f in filters:
                col = f['column']
                
                if col not in df_copy.columns:
                    st.warning(f" Colonne '{col}' introuvable dans le filtre, ignorée")
                    continue
                
                operator = f['operator']
                value = f['value']
                category = f['category']
                
                try:
                    # FILTRES NUMÉRIQUES
                    if category == "Numérique":
                        if operator == "Égal à":
                            df_copy = df_copy[df_copy[col] == value]
                        elif operator == "Différent de":
                            df_copy = df_copy[df_copy[col] != value]
                        elif operator == "Supérieur à":
                            df_copy = df_copy[df_copy[col] > value]
                        elif operator == "Inférieur à":
                            df_copy = df_copy[df_copy[col] < value]
                        elif operator == "Entre":
                            df_copy = df_copy[(df_copy[col] >= value[0]) & (df_copy[col] <= value[1])]
                        elif operator == "N'est pas entre":
                            df_copy = df_copy[(df_copy[col] < value[0]) | (df_copy[col] > value[1])]
                    
                    # FILTRES DATES
                    elif category == "Date":
                        if operator == "Avant le":
                            df_copy = df_copy[df_copy[col] < value]
                        elif operator == "Après le":
                            df_copy = df_copy[df_copy[col] > value]
                        elif operator == "Égal à":
                            df_copy = df_copy[df_copy[col].dt.date == value.date()]
                        elif operator == "Entre":
                            df_copy = df_copy[(df_copy[col] >= value[0]) & (df_copy[col] <= value[1])]
                        elif operator == "N'est pas entre":
                            df_copy = df_copy[(df_copy[col] < value[0]) | (df_copy[col] > value[1])]
                    
                    # FILTRES TEXTE
                    else:
                        if operator == "Contient":
                            df_copy = df_copy[df_copy[col].str.contains(str(value), case=False, na=False)]
                        elif operator == "Ne contient pas":
                            df_copy = df_copy[~df_copy[col].str.contains(str(value), case=False, na=False)]
                        elif operator == "Égal à":
                            df_copy = df_copy[df_copy[col] == value]
                        elif operator == "Différent de":
                            df_copy = df_copy[df_copy[col] != value]
                        elif operator == "Commence par":
                            df_copy = df_copy[df_copy[col].str.startswith(str(value), na=False)]
                        elif operator == "Finit par":
                            df_copy = df_copy[df_copy[col].str.endswith(str(value), na=False)]
                except Exception as e:
                    st.warning(f" Erreur lors du filtrage sur '{col}' : {str(e)}")
        
        return df_copy
        
    except Exception as e:
        st.error(f" Erreur lors de la transformation : {str(e)}")
        st.info(" La transformation a été ignorée, données conservées")
        return df_copy


def generate_python_code(transformations, original_filename):
    """
    Génère du code Python reproductible pour les transformations.
    
    Args:
        transformations: Liste des transformations appliquées
        original_filename: Nom du fichier original
        
    Returns:
        Code Python sous forme de string
    """
    code_lines = []
    
    # Imports
    code_lines.append("import pandas as pd")
    code_lines.append("import numpy as np")
    code_lines.append("")
    
    # Chargement fichier
    code_lines.append(f"# Chargement du fichier")
    if original_filename.endswith('.csv'):
        code_lines.append(f"df = pd.read_csv('{original_filename}')")
    elif original_filename.endswith(('.xlsx', '.xls')):
        code_lines.append(f"df = pd.read_excel('{original_filename}')")
    elif original_filename.endswith('.json'):
        code_lines.append(f"df = pd.read_json('{original_filename}')")
    
    code_lines.append("")
    code_lines.append("# Transformations")
    
    # Générer code pour chaque transformation
    for trans in transformations:
        trans_type = trans['type']
        code_lines.append("")
        
        # Remplissage NaN
        if trans_type in ['fill_na', 'fill_na_numeric', 'fill_na_categorical']:
            col = trans['column']
            strategy = trans.get('strategy', trans.get('method', ''))
            
            if strategy in ['supprimer les lignes', 'Supprimer les lignes']:
                code_lines.append(f"df = df.dropna(subset=['{col}'])")
            elif strategy in ['valeur fixe', 'Valeur fixe']:
                fill_value = trans.get('fill_value')
                code_lines.append(f"df['{col}'].fillna({repr(fill_value)}, inplace=True)")
            elif strategy in ['médiane', 'Médiane']:
                code_lines.append(f"df['{col}'].fillna(df['{col}'].median(), inplace=True)")
            elif strategy in ['moyenne', 'Moyenne']:
                code_lines.append(f"df['{col}'].fillna(df['{col}'].mean(), inplace=True)")
            elif strategy in ['mode (valeur la plus fréquente)', 'Mode (valeur la plus fréquente)']:
                code_lines.append(f"mode_val = df['{col}'].mode()[0] if len(df['{col}'].mode()) > 0 else None")
                code_lines.append(f"if mode_val is not None:")
                code_lines.append(f"    df['{col}'].fillna(mode_val, inplace=True)")
            elif strategy == 'Propagation avant (ffill)':
                code_lines.append(f"df['{col}'].fillna(method='ffill', inplace=True)")
            elif strategy == 'Propagation arrière (bfill)':
                code_lines.append(f"df['{col}'].fillna(method='bfill', inplace=True)")
            elif strategy == 'Remplir avec la moyenne':
                code_lines.append(f"df['{col}'].fillna(df['{col}'].mean(), inplace=True)")
            elif strategy == 'Remplir avec la médiane':
                code_lines.append(f"df['{col}'].fillna(df['{col}'].median(), inplace=True)")
            elif strategy == 'Remplir avec une valeur':
                fill_value = trans.get('value', trans.get('fill_value'))
                code_lines.append(f"df['{col}'].fillna({repr(fill_value)}, inplace=True)")


        # Conversion types
        elif trans_type == 'convert_type':
            col = trans['column']
            target_type = trans['target_type']
            
            if target_type == 'Entier (int)':
                code_lines.append(f"df['{col}'] = pd.to_numeric(df['{col}'], errors='coerce').fillna(0).astype(int)")
            elif target_type == 'Décimal (float)':
                code_lines.append(f"df['{col}'] = pd.to_numeric(df['{col}'], errors='coerce')")
            elif target_type == 'Texte (string)':
                code_lines.append(f"df['{col}'] = df['{col}'].astype(str)")
            elif target_type == 'Date (datetime)':
                code_lines.append(f"df['{col}'] = pd.to_datetime(df['{col}'], errors='coerce')")
            elif target_type == 'Booléen (bool)':
                code_lines.append(f"df['{col}'] = df['{col}'].astype(bool)")
        
        # Doublons
        elif trans_type == 'drop_duplicates':
            keep = trans['keep']
            keep_map = {'première': 'first', 'dernière': 'last', 'aucune': False}
            code_lines.append(f"df = df.drop_duplicates(keep='{keep_map[keep]}')")
        
        # Formatage décimales
        elif trans_type == 'format_decimals':
            col = trans['column']
            decimals = trans['decimals']
            code_lines.append(f"df['{col}'] = df['{col}'].round({decimals})")
        
        # Nettoyage texte
        elif trans_type == 'text_cleaning':
            col = trans['column']
            operation = trans['operation']
            
            if operation == "Supprimer espaces début/fin (trim)":
                code_lines.append(f"df['{col}'] = df['{col}'].str.strip()")
            elif operation == "Convertir en minuscules":
                code_lines.append(f"df['{col}'] = df['{col}'].str.lower()")
            elif operation == "Convertir en majuscules":
                code_lines.append(f"df['{col}'] = df['{col}'].str.upper()")
            elif operation == "Convertir en title case (Première Lettre Majuscule)":
                code_lines.append(f"df['{col}'] = df['{col}'].str.title()")
            elif operation == "Remplacer une valeur":
                replace_from = trans['replace_from']
                replace_to = trans['replace_to']
                code_lines.append(f"df['{col}'] = df['{col}'].str.replace('{replace_from}', '{replace_to}', regex=False)")
            elif operation == "Supprimer caractères spéciaux":
                code_lines.append(f"df['{col}'] = df['{col}'].str.replace(r'[^a-zA-Z0-9\\s]', '', regex=True)")
        
        # Extraction
        elif trans_type == 'extract_pattern':
            source_col = trans['source_column']
            new_col = trans['new_column']
            pattern = trans['pattern']
            extraction_type = trans['extraction_type']
            
            pattern_escaped = pattern.replace('\\', '\\\\')
            code_lines.append(f"# Extraction : {extraction_type}")
            code_lines.append(f"df['{new_col}'] = df['{source_col}'].str.extract(r'({pattern_escaped})', expand=False)")
        
        # Split colonnes
        elif trans_type == 'split_column':
            source_col = trans['source_column']
            new_cols = trans['new_columns']
            split_method = trans['split_method']
            
            if split_method == 'separator':
                separator = trans['separator']
                n_splits = trans['n_splits']
                code_lines.append(f"split_data = df['{source_col}'].str.split('{separator}', n={n_splits-1}, expand=True)")
                for i, col_name in enumerate(new_cols):
                    code_lines.append(f"df['{col_name}'] = split_data[{i}] if {i} < split_data.shape[1] else None")
            
            elif split_method == 'position':
                position = trans['position']
                code_lines.append(f"df['{new_cols[0]}'] = df['{source_col}'].str[:{position}]")
                code_lines.append(f"df['{new_cols[1]}'] = df['{source_col}'].str[{position}:].str.strip()")
            
            elif split_method == 'regex':
                pattern = trans['pattern']
                n_splits = trans['n_splits']
                pattern_escaped = pattern.replace('\\', '\\\\')
                code_lines.append(f"split_data = df['{source_col}'].str.split(r'{pattern_escaped}', n={n_splits-1}, expand=True, regex=True)")
                for i, col_name in enumerate(new_cols):
                    code_lines.append(f"df['{col_name}'] = split_data[{i}] if {i} < split_data.shape[1] else None")
        
        # Find & Replace
        elif trans_type == 'find_replace':
            col = trans['column']
            method = trans['method']
            
            if method == 'exact':
                search = trans['search']
                replace = trans['replace']
                case_sensitive = trans.get('case_sensitive', False)
                code_lines.append(f"df['{col}'] = df['{col}'].str.replace('{search}', '{replace}', case={case_sensitive}, regex=False)")
                
            elif method == 'regex':
                pattern = trans['pattern']
                replace = trans['replace']
                pattern_escaped = pattern.replace('\\', '\\\\')
                code_lines.append(f"df['{col}'] = df['{col}'].str.replace(r'{pattern_escaped}', '{replace}', regex=True)")
                
            elif method == 'multiple':
                replacements = trans['replacements']
                code_lines.append(f"# Remplacements multiples dans '{col}'")
                for r in replacements:
                    code_lines.append(f"df['{col}'] = df['{col}'].str.replace('{r['search']}', '{r['replace']}', regex=False)")
        
        # Filtrage
        elif trans_type == 'filter_rows':
            filters = trans['filters']
            
            code_lines.append(f"# Filtrage : {len(filters)} condition(s)")
            
            for f in filters:
                col = f['column']
                operator = f['operator']
                value = f['value']
                category = f['category']
                
                if category == "Numérique":
                    if operator == "Égal à":
                        code_lines.append(f"df = df[df['{col}'] == {value}]")
                    elif operator == "Différent de":
                        code_lines.append(f"df = df[df['{col}'] != {value}]")
                    elif operator == "Supérieur à":
                        code_lines.append(f"df = df[df['{col}'] > {value}]")
                    elif operator == "Inférieur à":
                        code_lines.append(f"df = df[df['{col}'] < {value}]")
                    elif operator == "Entre":
                        code_lines.append(f"df = df[(df['{col}'] >= {value[0]}) & (df['{col}'] <= {value[1]})]")
                    elif operator == "N'est pas entre":
                        code_lines.append(f"df = df[(df['{col}'] < {value[0]}) | (df['{col}'] > {value[1]})]")
                
                elif category == "Date":
                    if operator == "Avant le":
                        code_lines.append(f"df = df[df['{col}'] < pd.Timestamp('{value}')]")
                    elif operator == "Après le":
                        code_lines.append(f"df = df[df['{col}'] > pd.Timestamp('{value}')]")
                    elif operator == "Égal à":
                        code_lines.append(f"df = df[df['{col}'].dt.date == pd.Timestamp('{value}').date()]")
                    elif operator == "Entre":
                        code_lines.append(f"df = df[(df['{col}'] >= pd.Timestamp('{value[0]}')) & (df['{col}'] <= pd.Timestamp('{value[1]}'))]")
                    elif operator == "N'est pas entre":
                        code_lines.append(f"df = df[(df['{col}'] < pd.Timestamp('{value[0]}')) | (df['{col}'] > pd.Timestamp('{value[1]}'))]")
                
                else:
                    if operator == "Contient":
                        code_lines.append(f"df = df[df['{col}'].str.contains('{value}', case=False, na=False)]")
                    elif operator == "Ne contient pas":
                        code_lines.append(f"df = df[~df['{col}'].str.contains('{value}', case=False, na=False)]")
                    elif operator == "Égal à":
                        code_lines.append(f"df = df[df['{col}'] == '{value}']")
                    elif operator == "Différent de":
                        code_lines.append(f"df = df[df['{col}'] != '{value}']")
                    elif operator == "Commence par":
                        code_lines.append(f"df = df[df['{col}'].str.startswith('{value}', na=False)]")
                    elif operator == "Finit par":
                        code_lines.append(f"df = df[df['{col}'].str.endswith('{value}', na=False)]")
    
    # Export
    code_lines.append("")
    code_lines.append("# Export")
    code_lines.append("df.to_csv('cleaned_data.csv', index=False)")
    
    return "\n".join(code_lines)