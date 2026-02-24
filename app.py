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

st.set_page_config(
    page_title="CleanSheet App",
    page_icon="📑",
    layout="wide"
)


st.title("📑 CleanSheet - Outil de nettoyage de données")
st.markdown("Uploadez votre fichier pour commencer l'analyse et le nettoyage.")


st.sidebar.header("Options")


uploaded_file = st.file_uploader(
    "Choisissez un fichier CSV ou Excel",
    type=['csv', 'xlsx', 'xls', 'json'],
    help="Formats supportés : CSV, Excel (.xlsx, .xls), JSON"
)


if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.json'):
            df = pd.read_json(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        st.success(f"✅ Fichier chargé : {uploaded_file.name}")
        
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




