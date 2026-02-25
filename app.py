import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import missingno as msno    
import matplotlib.pyplot as plt
from io import BytesIO 

# Fonction pour détecter les formats de dates dans une colonne
def detect_date_formats(column):
    """
    Détecte les différents formats de dates présents dans une colonne.
    Retourne un dictionnaire avec les formats détectés et leur fréquence.
    """
    formats_detected = {}
    
    
    date_formats = [
        '%Y-%m-%d',      # 2024-01-15
        '%d/%m/%Y',      # 15/01/2024
        '%m/%d/%Y',      # 01/15/2024
        '%Y/%m/%d',      # 2024/01/15
        '%d-%m-%Y',      # 15-01-2024
        '%m-%d-%Y',      # 01-15-2024
        '%d.%m.%Y',      # 15.01.2024
        '%Y%m%d',        # 20240115
    ]
    
    for value in column.dropna().astype(str).unique()[:100]: 
        for fmt in date_formats:
            try:
                pd.to_datetime(value, format=fmt)
                if fmt not in formats_detected:
                    formats_detected[fmt] = 0
                formats_detected[fmt] += 1
                break 
            except:
                continue
    
    return formats_detected

# Fonction pour rejouer une transformation
def replay_transformation(df, transformation):
    """
    Rejoue une transformation sur un DataFrame.
    
    Args:
        df: DataFrame pandas à transformer
        transformation: Dictionnaire contenant les infos de la transformation
        
    Returns:
        DataFrame modifié
    """
    df_copy = df.copy()  # Toujours travailler sur une copie
    
    trans_type = transformation['type']
    
    # Remplacement NaN colonnes numériques
    if trans_type == 'fill_na_numeric':
        col = transformation['column']
        strategy = transformation['strategy']
        
        if strategy == 'médiane':
            df_copy[col].fillna(df_copy[col].median(), inplace=True)
        elif strategy == 'moyenne':
            df_copy[col].fillna(df_copy[col].mean(), inplace=True)
        elif strategy == 'valeur fixe':
            df_copy[col].fillna(transformation['fill_value'], inplace=True)
        elif strategy == 'supprimer les lignes':
            df_copy = df_copy.dropna(subset=[col])
    
    # Remplacement NaN colonnes catégorielles
    elif trans_type == 'fill_na_categorical':
        col = transformation['column']
        strategy = transformation['strategy']
        
        if strategy == 'valeur fixe':
            df_copy[col].fillna(transformation['fill_value'], inplace=True)
        elif strategy == 'mode (valeur la plus fréquente)':
            mode_val = df_copy[col].mode()[0]
            df_copy[col].fillna(mode_val, inplace=True)
        elif strategy == 'supprimer les lignes':
            df_copy = df_copy.dropna(subset=[col])
    
    # Conversion de types
    elif trans_type == 'convert_type':
        col = transformation['column']
        target = transformation['target_type']
        
        if target == "Numérique (float)":
            df_copy[col] = pd.to_numeric(df_copy[col], errors='coerce')
        elif target == "Numérique (int)":
            df_copy[col] = pd.to_numeric(df_copy[col], errors='coerce').astype('Int64')
        elif target == "Texte (string)":
            df_copy[col] = df_copy[col].astype(str)
        elif target == "Date/Heure":
            df_copy[col] = pd.to_datetime(df_copy[col], errors='coerce')
    
    # Suppression doublons
    elif trans_type == 'drop_duplicates':
        keep = transformation['keep']
        
        if keep == 'première':
            df_copy = df_copy.drop_duplicates(keep='first')
        elif keep == 'dernière':
            df_copy = df_copy.drop_duplicates(keep='last')
        elif keep == 'aucune (supprimer toutes)':
            df_copy = df_copy.drop_duplicates(keep=False)
    
    return df_copy


st.set_page_config(
    page_title="CleanSheet App",
    page_icon="📑",
    layout="wide"
)


st.title("📑 CleanSheet - Outil de nettoyage de données")
st.markdown("Uploadez votre fichier pour commencer l'analyse et le nettoyage.")


st.sidebar.header("Options")

if 'transformations_applied' in st.session_state and len(st.session_state.transformations_applied) > 0:
    st.sidebar.subheader("Historique des transformations")
    for i, transformation in enumerate(st.session_state.transformations_applied, start=1):
        st.sidebar.write(f"{i}. {transformation['description']}")
    if st.sidebar.button("↩️ Annuler dernière transformation"):
        # Retirer la dernière transformation
        st.session_state.transformations_applied.pop()
        
        # Repartir du DataFrame original
        df_rebuilt = st.session_state.df_original.copy()
        
        # Rejouer toutes les transformations restantes
        for transformation in st.session_state.transformations_applied:
            df_rebuilt = replay_transformation(df_rebuilt, transformation)
        
        # Mettre à jour le DataFrame de travail
        st.session_state.df_working = df_rebuilt
        
        st.sidebar.success("✅ Transformation annulée")
        st.rerun()

        # Bouton pour tout recommencer
    if st.sidebar.button("🔄 Tout recommencer"):
        # Repartir du DataFrame original
        st.session_state.df_working = st.session_state.df_original.copy()
        
        # Vider l'historique
        st.session_state.transformations_applied = []
        
        st.sidebar.success("✅ Données réinitialisées")
        st.rerun()

uploaded_file = st.file_uploader(
    "Choisissez un fichier CSV ou Excel",
    type=['csv', 'xlsx', 'xls', 'json'],
    help="Formats supportés : CSV, Excel (.xlsx, .xls), JSON"
)


if uploaded_file is not None or 'df_working' in st.session_state:
    try:
        # Chargement du fichier seulement si nouveau ou pas en session
        if uploaded_file is not None and ('df_original' not in st.session_state or st.session_state.get('last_file') != uploaded_file.name):
            if uploaded_file.name.endswith('.csv'):
                df_loaded = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith('.json'):
                df_loaded = pd.read_json(uploaded_file)
            else:
                df_loaded = pd.read_excel(uploaded_file)
            
            # Stockage dans session_state
            st.session_state.df_original = df_loaded.copy()  
            st.session_state.df_working = df_loaded.copy()   
            st.session_state.last_file = uploaded_file.name
            st.session_state.transformations_applied = []    
            
            st.success(f"✅ Fichier chargé : {uploaded_file.name}")
        
        # Récupération du DataFrame de travail (TOUJOURS)
        if 'df_working' in st.session_state:
            df = st.session_state.df_working
        
        st.subheader("📊 Aperçu des données")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Nombre de lignes", f"{len(df):,}")
        with col2:
            st.metric("Nombre de colonnes", len(df.columns))
        with col3:
            st.metric("Taille mémoire", f"{df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
        # Affichage du DataFrame
        st.dataframe(df, use_container_width=True, height=400)
        

        # Comparaison avant/après si des transformations ont été appliquées
        if 'transformations_applied' in st.session_state and len(st.session_state.transformations_applied) > 0:
            st.info("**📊 Impact des transformations :**")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                original_rows = len(st.session_state.df_original)
                current_rows = len(df)
                delta_rows = current_rows - original_rows
                
                st.metric(
                    "Lignes", 
                    f"{current_rows:,}", 
                    delta=f"{delta_rows:+,}" if delta_rows != 0 else "0",
                    delta_color="normal"
                )
            
            with col2:
                original_nan = st.session_state.df_original.isnull().sum().sum()
                current_nan = df.isnull().sum().sum()
                delta_nan = current_nan - original_nan
                
                st.metric(
                    "Valeurs manquantes", 
                    f"{current_nan:,}", 
                    delta=f"{delta_nan:+,}" if delta_nan != 0 else "0",
                    delta_color="inverse"
                )
            
            with col3:
                st.metric(
                    "Transformations", 
                    len(st.session_state.transformations_applied),
                    delta=None
                )
       
        st.subheader("🔍 Profiling rapide")
        
        missing_values = df.isnull().sum()
        if missing_values.sum() > 0:
            st.warning(f"⚠️ Total de valeurs manquantes : {missing_values.sum():,}")
            
            cols_with_missing = missing_values[missing_values > 0]
            missing_df = pd.DataFrame({
                'Colonne': cols_with_missing.index,
                'Valeurs manquantes': cols_with_missing.values,
                'Pourcentage': (cols_with_missing.values / len(df) * 100).round(2)
            })
            st.dataframe(missing_df, use_container_width=True)
        else:
            st.success("✅ Aucune valeur manquante détectée")
        
        st.subheader("📝 Types de données")
        types_df = pd.DataFrame({
            'Colonne': df.columns,
            'Type': df.dtypes.astype(str),
            'Valeurs uniques': [df[col].nunique() for col in df.columns]
        })
        st.dataframe(types_df, use_container_width=True)

        st.subheader("📅 Analyse des dates")
        
        date_issues_found = False
        
        for col in df.columns:
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                st.success(f"✅ Colonne **{col}** : format datetime correct")
            
            elif df[col].dtype == 'object':
                formats = detect_date_formats(df[col])
                
                if len(formats) > 1:
                    date_issues_found = True
                    st.warning(f"📅 Colonne **{col}** : {len(formats)} formats de dates différents détectés")
                    
                    format_names = {
                        '%Y-%m-%d': 'YYYY-MM-DD',
                        '%d/%m/%Y': 'DD/MM/YYYY',
                        '%m/%d/%Y': 'MM/DD/YYYY',
                        '%Y/%m/%d': 'YYYY/MM/DD',
                        '%d-%m-%Y': 'DD-MM-YYYY',
                        '%m-%d-%Y': 'MM-DD-YYYY',
                        '%d.%m.%Y': 'DD.MM.YYYY',
                        '%Y%m%d': 'YYYYMMDD',
                    }
                    
                    for fmt, count in formats.items():
                        st.write(f"  - Format {format_names.get(fmt, fmt)} : {count} valeur(s)")
        
        if not date_issues_found:
            st.info("ℹ️ Aucun problème de format de date détecté")

        st.subheader("⚠️ Détection d'anomalies")
                
        anomalies_found = False
                
                
        for col in df.columns:
            if df[col].dtype == 'object':  
                numeric_test = pd.to_numeric(df[col], errors='coerce')
                convertible_pct = (numeric_test.notna().sum() / len(df)) * 100
                
                if convertible_pct > 50 and convertible_pct < 100:
                    anomalies_found = True
                    non_numeric = df[df[col].notna() & numeric_test.isna()][col].unique()[:5]
                    st.warning(f"🔍 Colonne **{col}** : {convertible_pct:.1f}% des valeurs sont numériques, mais certaines ne le sont pas")
                    st.write(f"Exemples de valeurs non-numériques : {list(non_numeric)}")

        duplicates_count = df.duplicated().sum()
        if duplicates_count > 0:
            anomalies_found = True
            st.warning(f"🔄 **{duplicates_count} lignes dupliquées** détectées ({(duplicates_count/len(df)*100):.2f}%)")
                    
            if st.checkbox("Afficher les lignes dupliquées"):
               st.dataframe(df[df.duplicated(keep=False)].sort_values(by=list(df.columns)), 
                        use_container_width=True, height=300)
                
        if not anomalies_found:
            st.success("✅ Aucune anomalie majeure détectée")
        
        
        if missing_values.sum() > 0:
            st.subheader("🔥 Heatmap des valeurs manquantes")
            
            plt.clf()
            plt.close('all')    
            fig, ax = plt.subplots(figsize=(10, 6))
            msno.matrix(df, ax=ax, sparkline=False)
            st.pyplot(fig)
            
            plt.clf()
            plt.close('all')
            
            st.caption("Les barres blanches indiquent les valeurs manquantes. Cherchez des patterns.")
            
            
            
        st.subheader("📊 Distribution des données numériques")
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if len(numeric_cols) > 0:
            # Sélecteur de colonne
            selected_col = st.selectbox(
                "Choisissez une colonne à visualiser",
                numeric_cols
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Histogramme
                fig_hist = px.histogram(
                    df, 
                    x=selected_col,
                    title=f"Distribution de {selected_col}",
                    nbins=50
                )
                st.plotly_chart(fig_hist, use_container_width=True)
            
            with col2:
                # Boxplot pour détecter outliers
                fig_box = px.box(
                    df,
                    y=selected_col,
                    title=f"Boxplot de {selected_col}"
                )
                st.plotly_chart(fig_box, use_container_width=True)
            
            # Stats descriptives
            st.write("**Statistiques descriptives :**")
            stats = df[selected_col].describe()
            st.dataframe(stats.to_frame().T, use_container_width=True)
            
        else:
            st.info("Aucune colonne numérique à visualiser")

        
# Section de transformations interactives
        st.subheader("🔧 Transformations de données")
        
        # Tabs pour organiser les différents types de transformations
        tab1, tab2, tab3, tab4 = st.tabs([
            "Valeurs manquantes", 
            "Conversion de types", 
            "Doublons",
            "Filtrage"
        ])
        
        # TAB 1 : Gestion des valeurs manquantes
        with tab1:
            st.write("**Remplacer les valeurs manquantes**")
            
            cols_with_na = [col for col in df.columns if df[col].isnull().sum() > 0]
            
            if len(cols_with_na) > 0:
                col_to_fix = st.selectbox(
                    "Choisir une colonne",
                    cols_with_na,
                    key="na_col_select"
                )
                
                na_count = df[col_to_fix].isnull().sum()
                st.info(f"Colonne **{col_to_fix}** : {na_count} valeurs manquantes ({na_count/len(df)*100:.1f}%)")
                
                # Options selon le type de colonne
                if df[col_to_fix].dtype in ['int64', 'float64']:
                    strategy = st.radio(
                        "Stratégie de remplacement",
                        ["Médiane", "Moyenne", "Valeur fixe", "Supprimer les lignes"],
                        key="na_strategy"
                    )
                    
                    if strategy == "Valeur fixe":
                        fill_value = st.number_input("Valeur de remplacement", value=0.0)
                    
                    if st.button("Appliquer", key="apply_na"):
                        df_preview = st.session_state.df_working.copy()
                        
                        if strategy == "Médiane":
                            df_preview[col_to_fix].fillna(df_preview[col_to_fix].median(), inplace=True)
                            st.success(f"✅ Valeurs manquantes remplacées par la médiane ({df_preview[col_to_fix].median():.2f})")
                        elif strategy == "Moyenne":
                            df_preview[col_to_fix].fillna(df_preview[col_to_fix].mean(), inplace=True)
                            st.success(f"✅ Valeurs manquantes remplacées par la moyenne ({df_preview[col_to_fix].mean():.2f})")
                        elif strategy == "Valeur fixe":
                            df_preview[col_to_fix].fillna(fill_value, inplace=True)
                            st.success(f"✅ Valeurs manquantes remplacées par {fill_value}")
                        elif strategy == "Supprimer les lignes":
                            df_preview = df_preview.dropna(subset=[col_to_fix])
                            st.success(f"✅ {na_count} lignes supprimées")
                        
                        # Mise à jour du DataFrame de travail
                        st.session_state.df_working = df_preview
                        st.session_state.transformations_applied.append({
                        'type': 'fill_na_numeric',
                        'column': col_to_fix,
                        'strategy': strategy.lower(),  # "médiane" ou "moyenne" ou "valeur fixe"
                        'fill_value': fill_value if strategy == "Valeur fixe" else None,
                        'description': f"NaN remplacés dans '{col_to_fix}' par {strategy}"
                        })
                        st.rerun()
                
                else:  # Colonnes non-numériques
                    strategy = st.radio(
                        "Stratégie de remplacement",
                        ["Valeur fixe", "Mode (valeur la plus fréquente)", "Supprimer les lignes"],
                        key="na_strategy_cat"
                    )
                    
                    if strategy == "Valeur fixe":
                        fill_value = st.text_input("Valeur de remplacement", value="Inconnu")
                    
                    if st.button("Appliquer", key="apply_na_cat"):
                        df_preview = st.session_state.df_working.copy()
                        
                        if strategy == "Valeur fixe":
                            df_preview[col_to_fix].fillna(fill_value, inplace=True)
                            st.success(f"✅ Valeurs manquantes remplacées par '{fill_value}'")
                        elif strategy == "Mode (valeur la plus fréquente)":
                            mode_val = df_preview[col_to_fix].mode()[0]
                            df_preview[col_to_fix].fillna(mode_val, inplace=True)
                            st.success(f"✅ Valeurs manquantes remplacées par le mode ('{mode_val}')")
                        elif strategy == "Supprimer les lignes":
                            df_preview = df_preview.dropna(subset=[col_to_fix])
                            st.success(f"✅ {na_count} lignes supprimées")
                        
                        st.session_state.df_working = df_preview
                        st.session_state.transformations_applied.append({
                        'type': 'fill_na_categorical',
                        'column': col_to_fix,
                        'strategy': strategy.lower(),
                        'fill_value': fill_value if strategy == "Valeur fixe" else None,
                        'description': f"NaN remplacés dans '{col_to_fix}' par {strategy}"
                        })
                        st.rerun()
            else:
                st.success("✅ Aucune valeur manquante à traiter")
        
        # TAB 2 : Conversion de types
        with tab2:
            st.write("**Convertir le type d'une colonne**")
            
            col_to_convert = st.selectbox(
                "Choisir une colonne",
                df.columns.tolist(),
                key="convert_col_select"
            )
            
            current_type = df[col_to_convert].dtype
            st.info(f"Type actuel : **{current_type}**")
            
            target_type = st.selectbox(
                "Convertir en",
                ["Numérique (float)", "Numérique (int)", "Texte (string)", "Date/Heure"],
                key="target_type"
            )
            
            if st.button("Appliquer conversion", key="apply_convert"):
                df_preview = st.session_state.df_working.copy()
                
                try:
                    if target_type == "Numérique (float)":
                        df_preview[col_to_convert] = pd.to_numeric(df_preview[col_to_convert], errors='coerce')
                        st.success(f"✅ Colonne '{col_to_convert}' convertie en float")
                    elif target_type == "Numérique (int)":
                        df_preview[col_to_convert] = pd.to_numeric(df_preview[col_to_convert], errors='coerce').astype('Int64')
                        st.success(f"✅ Colonne '{col_to_convert}' convertie en int")
                    elif target_type == "Texte (string)":
                        df_preview[col_to_convert] = df_preview[col_to_convert].astype(str)
                        st.success(f"✅ Colonne '{col_to_convert}' convertie en string")
                    elif target_type == "Date/Heure":
                        df_preview[col_to_convert] = pd.to_datetime(df_preview[col_to_convert], errors='coerce')
                        st.success(f"✅ Colonne '{col_to_convert}' convertie en datetime")
                    
                    st.session_state.df_working = df_preview
                    st.session_state.transformations_applied.append({
                    'type': 'convert_type',
                    'column': col_to_convert,
                    'target_type': target_type,
                    'description': f"Conversion '{col_to_convert}' en {target_type}"})
                    st.rerun()
                
                except Exception as e:
                    st.error(f"❌ Erreur lors de la conversion : {str(e)}")
        
        # TAB 3 : Gestion des doublons
        with tab3:
            st.write("**Supprimer les lignes dupliquées**")
            
            dup_count = df.duplicated().sum()
            
            if dup_count > 0:
                st.warning(f"⚠️ {dup_count} ligne(s) dupliquée(s) détectée(s)")
                
                keep_strategy = st.radio(
                    "Quelle occurrence garder ?",
                    ["Première", "Dernière", "Aucune (supprimer toutes)"],
                    key="dup_strategy"
                )
                
                if st.button("Supprimer les doublons", key="apply_dup"):
                    df_preview = st.session_state.df_working.copy()
                    
                    if keep_strategy == "Première":
                        df_preview = df_preview.drop_duplicates(keep='first')
                    elif keep_strategy == "Dernière":
                        df_preview = df_preview.drop_duplicates(keep='last')
                    else:
                        df_preview = df_preview.drop_duplicates(keep=False)
                    
                    st.success(f"✅ {dup_count} doublon(s) supprimé(s)")
                    st.session_state.df_working = df_preview
                    st.session_state.transformations_applied.append({
                    'type': 'drop_duplicates',
                    'keep': keep_strategy.lower(),
                    'description': f"Doublons supprimés (stratégie: {keep_strategy})"})
                    st.rerun()
            else:
                st.success("✅ Aucun doublon détecté")
        
        with tab4:
            st.write("**Filtrer les données**")
            st.info("🚧 Fonctionnalité à venir dans la prochaine session")


# Section de suggestions automatiques
        st.subheader("💡 Suggestions de nettoyage")
        
        suggestions = []
        
        # Suggestions basées sur valeurs manquantes
        if missing_values.sum() > 0:
            high_missing_cols = missing_values[missing_values > len(df) * 0.5]
            if len(high_missing_cols) > 0:
                suggestions.append({
                    'priorité': '🔴 HAUTE',
                    'problème': f"{len(high_missing_cols)} colonne(s) avec >50% de valeurs manquantes",
                    'action': f"Supprimer colonnes : {', '.join(high_missing_cols.index.tolist())}",
                    'raison': "Colonnes avec trop peu de données exploitables"
                })
            
            medium_missing_cols = missing_values[(missing_values > 0) & (missing_values <= len(df) * 0.5)]
            if len(medium_missing_cols) > 0:
                for col in medium_missing_cols.index:
                    if df[col].dtype in ['int64', 'float64']:
                        suggestions.append({
                            'priorité': '🟡 MOYENNE',
                            'problème': f"Colonne '{col}' : {missing_values[col]} NaN",
                            'action': f"Remplacer par médiane ({df[col].median():.2f})",
                            'raison': "Colonne numérique - médiane robuste aux outliers"
                        })
                    else:
                        suggestions.append({
                            'priorité': '🟡 MOYENNE',
                            'problème': f"Colonne '{col}' : {missing_values[col]} NaN",
                            'action': f"Remplacer par valeur fixe ou mode",
                            'raison': "Colonne catégorielle"
                        })
        
        # Suggestions basées sur doublons
        if duplicates_count > 0:
            suggestions.append({
                'priorité': '🟠 IMPORTANTE',
                'problème': f"{duplicates_count} lignes dupliquées",
                'action': "Supprimer les doublons (garder première occurrence)",
                'raison': "Les doublons faussent les analyses statistiques"
            })
        
        # Suggestions basées sur types incohérents
        for col in df.columns:
            if df[col].dtype == 'object':
                numeric_test = pd.to_numeric(df[col], errors='coerce')
                convertible_pct = (numeric_test.notna().sum() / len(df)) * 100
                
                if convertible_pct > 80:
                    suggestions.append({
                        'priorité': '🟡 MOYENNE',
                        'problème': f"Colonne '{col}' devrait être numérique ({convertible_pct:.0f}% convertible)",
                        'action': f"Convertir en numérique (gérer les erreurs)",
                        'raison': "Permettra des calculs et agrégations"
                    })
        
        # Affichage des suggestions
        if suggestions:
            st.write(f"**{len(suggestions)} action(s) recommandée(s) :**")
            
            suggestions_df = pd.DataFrame(suggestions)
            
            # Trier par priorité
            priority_order = {'🔴 HAUTE': 0, '🟠 IMPORTANTE': 1, '🟡 MOYENNE': 2}
            suggestions_df['_sort'] = suggestions_df['priorité'].map(priority_order)
            suggestions_df = suggestions_df.sort_values('_sort').drop('_sort', axis=1)
            
            # Afficher dans un tableau stylé
            st.dataframe(
                suggestions_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    'priorité': st.column_config.TextColumn('Priorité', width='small'),
                    'problème': st.column_config.TextColumn('Problème détecté', width='medium'),
                    'action': st.column_config.TextColumn('Action recommandée', width='medium'),
                    'raison': st.column_config.TextColumn('Pourquoi ?', width='medium')
                }
            )
            
            st.info("💡 **Prochaine étape** : Ces suggestions seront bientôt automatisables en un clic !")
        else:
            st.success("✅ Aucune action de nettoyage nécessaire - vos données sont propres !")


    except Exception as e:
        st.error(f"❌ Erreur lors du chargement du fichier : {str(e)}")
        st.info("Vérifiez que votre fichier est bien formaté.")

else:
    st.info("👆 Uploadez un fichier CSV ou Excel pour commencer")




