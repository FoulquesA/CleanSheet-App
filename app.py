import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import missingno as msno
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO

from utils.data_loader import load_file, detect_date_formats
from utils.profiling import (
    get_basic_info,
    get_missing_values_summary,
    get_data_types_summary,
    detect_date_columns,
    analyze_date_column,
    detect_numeric_anomalies,
    detect_text_anomalies,
    create_missing_heatmap,
    create_distribution_plots,
    get_column_stats,
    detect_date_formats_in_column
)
from utils.transformations import replay_transformation, generate_python_code
from utils.templates_manager import (
    save_template,
    load_templates,
    load_template_data,
    delete_template
)
from utils.translations import get_text, TRANSLATIONS


# Mapping pour normaliser les stratégies stockées vers des clés de traduction
STRATEGY_MAPPING = {
    # Fill NA strategies - normalization vers clés anglaises
    'médiane': 'median',
    'median': 'median',
    'moyenne': 'mean',
    'mean': 'mean',
    'valeur fixe': 'fixed',
    'fixed value': 'fixed',
    'supprimer les lignes': 'drop',
    'drop rows': 'drop',
    'mode': 'mode',
    # Duplicate strategies
    'première': 'first',
    'first': 'first',
    'dernière': 'last',
    'last': 'last',
    'derniere': 'last',
}


def get_transformation_description(transformation, lang):
    """
    Génère dynamiquement la description d'une transformation dans la langue donnée.
    Utilise les clés de traduction existantes dans translations_COMPLETE.py
    """
    trans_type = transformation.get('type')
    
    if trans_type == 'fill_na_numeric' or trans_type == 'fill_na_categorical':
        col = transformation['column']
        strategy_raw = transformation.get('strategy', '').lower()
        strategy_key = STRATEGY_MAPPING.get(strategy_raw, strategy_raw)
        
        # Utiliser les clés history_fill_na_* du fichier de traductions
        translation_key = f'history_fill_na_{strategy_key}'
        description_template = get_text(translation_key, lang)
        
        # Si la clé existe et contient '{}', l'utiliser
        if '{}' in description_template:
            return description_template.format(col)
        else:
            # Fallback si la clé n'existe pas
            strategy_text = get_text(f'trans_missing_{strategy_key}', lang)
            if lang == 'fr':
                return f"NaN remplacés dans '{col}' par {strategy_text}"
            else:
                return f"NaN replaced in '{col}' with {strategy_text}"
    
    elif trans_type == 'convert_type':
        col = transformation['column']
        target = transformation['target_type']
        
        # Utiliser la clé history_convert_type si elle existe
        description_template = get_text('history_convert_type', lang)
        if '{}' in description_template:
            return description_template.format(col, target)
        else:
            if lang == 'fr':
                return f"Conversion '{col}' en {target}"
            else:
                return f"Conversion '{col}' to {target}"
    
    elif trans_type == 'drop_duplicates':
        keep_raw = transformation.get('keep', '').lower()
        keep_key = STRATEGY_MAPPING.get(keep_raw, keep_raw)
        
        # Utiliser les clés history_dup_* 
        description_template = get_text(f'history_dup_{keep_key}', lang)
        
        if description_template and description_template != f'history_dup_{keep_key}':
            # La clé existe, l'utiliser directement
            return description_template
        else:
            # Fallback
            keep_text = get_text(f'trans_dup_{keep_key}', lang)
            if lang == 'fr':
                return f"Doublons supprimés (stratégie: {keep_text})"
            else:
                return f"Duplicates removed (strategy: {keep_text})"
    
    elif trans_type == 'filter_rows':
        # Utiliser la clé history_filter
        desc = transformation.get('description', '')
        
        # Extraire les conditions de la description stockée
        if 'Filtrage appliqué' in desc or 'Filter applied' in desc or 'Filtering applied' in desc:
            if ':' in desc:
                conditions = desc.split(':', 1)[1].strip()
                # Convertir ET/AND selon la langue
                if lang == 'en':
                    conditions = conditions.replace(' ET ', ' AND ')
                else:
                    conditions = conditions.replace(' AND ', ' ET ')
                
                return get_text('history_filter', lang).format(conditions)
        
        return desc
    
    elif trans_type == 'text_cleaning':
        col = transformation.get('column', '')
        operations = transformation.get('operations', [])
        
        # Mapper les opérations vers les clés de traduction
        ops_keys_map = {
            'minuscules': 'lower',
            'lowercase': 'lower',
            'majuscules': 'upper', 
            'uppercase': 'upper',
            'espaces': 'trim',
            'trim spaces': 'trim',
            'accents': 'special',
            'remove accents': 'special',
            'ponctuation': 'special',
            'remove punctuation': 'special',
            'title case': 'title',
            'casse titre': 'title'
        }
        
        # Si une seule opération, utiliser les clés history_text_*
        if len(operations) == 1:
            op = operations[0].lower()
            op_key = ops_keys_map.get(op, op)
            translation_key = f'history_text_{op_key}'
            description_template = get_text(translation_key, lang)
            
            if '{}' in description_template:
                return description_template.format(col)
        
        # Sinon, fallback générique
        if lang == 'fr':
            ops_text = ', '.join(operations)
            return f"Nettoyage texte '{col}': {ops_text}"
        else:
            ops_text = ', '.join(operations)
            return f"Text cleaning '{col}': {ops_text}"
    
    elif trans_type == 'extract_pattern':
        col = transformation.get('column', '')
        new_col = transformation.get('new_column', '')
        
        if lang == 'fr':
            return f"Extraction pattern de '{col}' vers '{new_col}'"
        else:
            return f"Pattern extraction from '{col}' to '{new_col}'"
    
    elif trans_type == 'split_column':
        col = transformation.get('column', '')
        
        if lang == 'fr':
            return f"Division colonne '{col}'"
        else:
            return f"Column split '{col}'"
    
    elif trans_type == 'find_replace':
        col = transformation.get('column', '')
        old_val = transformation.get('old_value', '')
        new_val = transformation.get('new_value', '')
        
        # Utiliser history_text_replace si disponible
        description_template = get_text('history_text_replace', lang)
        if '{}' in description_template and description_template.count('{}') >= 3:
            return description_template.format(old_val, new_val, col)
        else:
            if lang == 'fr':
                return f"Rechercher/Remplacer dans '{col}'"
            else:
                return f"Find/Replace in '{col}'"
    
    # Fallback : utiliser la description stockée
    return transformation.get('description', 'Transformation')


st.set_page_config(
    page_title="CleanSheet App",
    page_icon="📑",
    layout="wide"
)

# Initialiser la langue
if 'language' not in st.session_state:
    st.session_state.language = 'fr'
lang = st.session_state.language

st.title(get_text('app_title', lang))
st.markdown(get_text('app_subtitle', lang))

# Message d'aide global
with st.expander(get_text('help_title', lang), expanded=False):
    st.markdown(get_text('help_content', lang))

st.sidebar.header("Options")

# Sélecteur de langue
language = st.sidebar.selectbox(
    "🌍 Langue / Language",
    options=['fr', 'en'],
    format_func=lambda x: "🇫🇷 Français" if x == 'fr' else "🇬🇧 English",
    index=0 if st.session_state.language == 'fr' else 1,
    key="language_selector"
)

if language != st.session_state.language:
    st.session_state.language = language
    st.rerun()


if 'transformations_applied' in st.session_state and len(st.session_state.transformations_applied) > 0:
    st.sidebar.subheader(get_text('sidebar_history', lang))
    for i, transformation in enumerate(st.session_state.transformations_applied, start=1):
        st.sidebar.write(f"{i}. {get_transformation_description(transformation, lang)}")
    if st.sidebar.button(get_text('sidebar_undo', lang)):
        st.session_state.transformations_applied.pop()
        df_rebuilt = st.session_state.df_original.copy()
        for transformation in st.session_state.transformations_applied:
            df_rebuilt = replay_transformation(df_rebuilt, transformation)
        st.session_state.df_working = df_rebuilt
        st.sidebar.success(get_text('sidebar_undo_success', lang))
        st.rerun()
    
    if st.sidebar.button(get_text('sidebar_reset', lang)):
        st.session_state.df_working = st.session_state.df_original.copy()
        st.session_state.transformations_applied = []
        st.sidebar.success(get_text('sidebar_reset_success', lang))
        st.rerun()

uploaded_file = st.file_uploader(
    get_text('upload_label', lang),
    type=['csv', 'xlsx', 'xls', 'json'],
    help=get_text('upload_help', lang)
)

if uploaded_file is not None or 'df_working' in st.session_state:
    try:
        if uploaded_file is not None:
            df, filename = load_file(uploaded_file)
            
            if df is not None and ('df_original' not in st.session_state or st.session_state.get('last_file') != uploaded_file.name):
                st.session_state.df_original = df.copy()
                st.session_state.df_working = df.copy()
                st.session_state.last_file = uploaded_file.name
                st.session_state.transformations_applied = []
                st.success(get_text('upload_success', lang).format(uploaded_file.name))
        
        if 'df_working' in st.session_state:
            df = st.session_state.df_working

        # Comparaison avant/après si des transformations ont été appliquées
        if 'transformations_applied' in st.session_state and len(st.session_state.transformations_applied) > 0:
            st.info(get_text('comparison_title', lang))
            col1, col2, col3 = st.columns(3)
            
            with col1:
                original_rows = len(st.session_state.df_original)
                current_rows = len(df)
                delta_rows = current_rows - original_rows
                st.metric(get_text('comparison_rows', lang), f"{current_rows:,}", delta=f"{delta_rows:+,}" if delta_rows != 0 else "0", delta_color="normal")
            
            with col2:
                original_nan = st.session_state.df_original.isnull().sum().sum()
                current_nan = df.isnull().sum().sum()
                delta_nan = current_nan - original_nan
                st.metric(get_text('comparison_missing', lang), f"{current_nan:,}", delta=f"{delta_nan:+,}" if delta_nan != 0 else "0", delta_color="inverse")
            
            with col3:
                st.metric(get_text('comparison_transformations', lang), len(st.session_state.transformations_applied), delta=None)
        
        # Tabs principales de navigation
        tab_profiling, tab_transformations, tab_export, tab_templates = st.tabs([
            get_text('tab_profiling', lang),
            get_text('tab_transformations', lang),
            get_text('tab_export', lang),
            get_text('tab_templates', lang)
        ])
        
        # ========== TAB 1 : PROFILING ==========
        with tab_profiling:
            st.subheader(get_text('profiling_overview', lang))
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(get_text('profiling_rows', lang), f"{len(df):,}")
            with col2:
                st.metric(get_text('profiling_cols', lang), len(df.columns))
            with col3:
                st.metric(get_text('profiling_memory', lang), f"{df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
            
            # Formater le DataFrame selon les décimales définies
            if 'column_decimals' in st.session_state and st.session_state.column_decimals:
                # Créer un dictionnaire de formatage
                format_dict = {col: f"{{:.{decimals}f}}" for col, decimals in st.session_state.column_decimals.items()}
                
                # Afficher avec formatage
                styled_df = df.style.format(format_dict, na_rep="-")
                st.dataframe(styled_df, use_container_width=True, height=400)
            else:
                # Affichage normal
                st.dataframe(df, use_container_width=True, height=400)
            
            st.subheader(get_text('profiling_quick', lang))
            missing_values = df.isnull().sum()
            if missing_values.sum() > 0:
                st.warning(get_text('profiling_missing_warning', lang).format(missing_values.sum()))
                cols_with_missing = missing_values[missing_values > 0]
                missing_df = pd.DataFrame({
                    get_text('profiling_cols_label', lang): cols_with_missing.index,
                    get_text('profiling_missing_label', lang): cols_with_missing.values,
                    get_text('profiling_percentage_label', lang): (cols_with_missing.values / len(df) * 100).round(2)
                })
                st.dataframe(missing_df, use_container_width=True)
            else:
                st.success(get_text('profiling_missing_success', lang))
            
            st.subheader(get_text('profiling_types', lang))
            types_df = pd.DataFrame({
                get_text('profiling_cols_label', lang): df.columns,
                get_text('profiling_types_label', lang): df.dtypes.astype(str),
                get_text('profiling_unique_label', lang): [df[col].nunique() for col in df.columns]
            })
            st.dataframe(types_df, use_container_width=True)

            st.subheader(get_text('profiling_dates', lang))
            date_issues_found = False
            for col in df.columns:
                if pd.api.types.is_datetime64_any_dtype(df[col]):
                    st.success(f"✅ {get_text('profiling_date_correct', lang).format(col)}")
                elif df[col].dtype == 'object':
                    formats = detect_date_formats_in_column(df[col])
                    if len(formats) > 1:
                        date_issues_found = True
                        st.warning(f"📅 {get_text('profiling_date_multiple', lang).format(col, len(formats))}")
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
                            st.write(f"  - {get_text('profiling_date_format', lang)} {format_names.get(fmt, fmt)} : {count} {get_text('profiling_date_values', lang)}")
            
            if not date_issues_found:
                st.info(get_text('profiling_date_no_issues', lang))

            st.subheader(get_text('profiling_anomalies', lang))
            anomalies_found = False
            for col in df.columns:
                if df[col].dtype == 'object':
                    numeric_test = pd.to_numeric(df[col], errors='coerce')
                    convertible_pct = (numeric_test.notna().sum() / len(df)) * 100
                    if convertible_pct > 50 and convertible_pct < 100:
                        anomalies_found = True
                        non_numeric = df[df[col].notna() & numeric_test.isna()][col].unique()[:5]
                        st.warning(f"🔍 {get_text('profiling_anomaly_numeric', lang).format(col, convertible_pct)}")
                        st.write(f"{get_text('profiling_anomaly_examples', lang)} {list(non_numeric)}")

            duplicates_count = df.duplicated().sum()
            if duplicates_count > 0:
                anomalies_found = True
                st.warning(get_text('profiling_duplicates_warning', lang).format(duplicates_count, duplicates_count/len(df)*100))
                if st.checkbox(get_text('profiling_duplicates_show', lang)):
                    st.dataframe(df[df.duplicated(keep=False)].sort_values(by=list(df.columns)), use_container_width=True, height=300)
            
            if not anomalies_found:
                st.success(get_text('profiling_anomalies_success', lang))
            
            if missing_values.sum() > 0:
                st.subheader(get_text('profiling_heatmap', lang))
                plt.clf()
                plt.close('all')
                fig, ax = plt.subplots(figsize=(10, 6))
                msno.matrix(df, ax=ax, sparkline=False)
                st.pyplot(fig)
                plt.clf()
                plt.close('all')
                st.caption(get_text('profiling_heatmap_caption', lang))
            
            st.subheader(get_text('profiling_distribution', lang))
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            if len(numeric_cols) > 0:
                selected_col = st.selectbox(get_text('profiling_select_column', lang), numeric_cols)
                col1, col2 = st.columns(2)
                with col1:
                    fig_hist = px.histogram(df, x=selected_col, title=f"{get_text('profiling_distribution_of', lang)} {selected_col}", nbins=50)
                    st.plotly_chart(fig_hist, use_container_width=True)
                with col2:
                    fig_box = px.box(df, y=selected_col, title=f"{get_text('profiling_boxplot_of', lang)} {selected_col}")
                    st.plotly_chart(fig_box, use_container_width=True)
                st.write(get_text('export_stats_label', lang))
                stats = df[selected_col].describe()
                st.dataframe(stats.to_frame().T, use_container_width=True)
            else:
                st.info(get_text('profiling_no_numeric', lang))
        
        # ========== TAB 2 : TRANSFORMATIONS ==========
        with tab_transformations:
            st.subheader(get_text('trans_title', lang))
            
            tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    get_text('trans_tab_missing', lang),
    get_text('trans_tab_types', lang),
    get_text('trans_tab_duplicates', lang),
    get_text('trans_tab_filter', lang),
    get_text('trans_tab_format', lang),
    get_text('trans_tab_text', lang)
])
            

            with tab1:
                st.write(get_text('trans_missing_title', lang))
                cols_with_na = [col for col in df.columns if df[col].isnull().sum() > 0]
                
                if len(cols_with_na) > 0:
                    col_to_fix = st.selectbox(get_text('trans_missing_select', lang), cols_with_na, key="na_col_select")
                    na_count = df[col_to_fix].isnull().sum()
                    st.info(get_text('trans_missing_info', lang).format(col_to_fix, na_count, na_count/len(df)*100))
                    
                    if df[col_to_fix].dtype in ['int64', 'float64']:
                        strategy = st.radio(
    get_text('trans_missing_strategy', lang),
    [
        get_text('trans_missing_median', lang),
        get_text('trans_missing_mean', lang),
        get_text('trans_missing_fixed', lang),
        get_text('trans_missing_drop', lang)
    ],
    key="na_strategy"
)
                        if strategy == "Valeur fixe":
                            fill_value = st.number_input(get_text('trans_missing_value', lang), value=0.0)
                        
                        if st.button(get_text('trans_missing_apply', lang), key="apply_na"):
                            df_preview = st.session_state.df_working.copy()
                            
                            # Validation : vérifier qu'il y a encore des NaN
                            if df_preview[col_to_fix].isna().sum() == 0:
                                st.warning(get_text('trans_missing_none_warning', lang))
                                st.stop()
                            
                            try:
                                if strategy == "Médiane":
                                    median_val = df_preview[col_to_fix].median()
                                    if pd.isna(median_val):
                                        st.error(get_text('trans_missing_median_error', lang))
                                        st.stop()
                                    df_preview[col_to_fix].fillna(median_val, inplace=True)
                                    st.success(get_text('trans_missing_median_success', lang).format(median_val))
                                    
                                elif strategy == "Moyenne":
                                    mean_val = df_preview[col_to_fix].mean()
                                    if pd.isna(mean_val):
                                        st.error(get_text('trans_missing_mean_error', lang))
                                        st.stop()
                                    df_preview[col_to_fix].fillna(mean_val, inplace=True)
                                    st.success(get_text('trans_missing_mean_success', lang).format(mean_val))
                                    
                                elif strategy == "Valeur fixe":
                                    df_preview[col_to_fix].fillna(fill_value, inplace=True)
                                    st.success(get_text('trans_missing_fixed_success', lang).format(fill_value))
                                    
                                elif strategy == "Supprimer les lignes":
                                    rows_before = len(df_preview)
                                    df_preview = df_preview.dropna(subset=[col_to_fix])
                                    rows_removed = rows_before - len(df_preview)
                                    
                                    if rows_removed == 0:
                                        st.warning(get_text('trans_missing_drop_warning', lang))
                                        st.stop()
                                    
                                    st.success(get_text('trans_missing_drop_success', lang).format(rows_removed))
                                
                                st.session_state.df_working = df_preview
                                st.session_state.transformations_applied.append({
                                    'type': 'fill_na_numeric', 
                                    'column': col_to_fix, 
                                    'strategy': strategy.lower(),
                                    'fill_value': fill_value if strategy == "Valeur fixe" else None,
                                    'description': f"NaN remplacés dans '{col_to_fix}' par {strategy}"
                                })
                                st.rerun()
                                
                            except Exception as e:
                                st.error(get_text('trans_missing_error', lang).format(str(e)))
                    else:
                        strategy = st.radio(
    get_text('trans_missing_strategy', lang),
    [
        get_text('trans_missing_fixed', lang),
        get_text('trans_missing_mode', lang),
        get_text('trans_missing_drop', lang)
    ],
    key="na_strategy_cat"
)
                        if strategy == "Valeur fixe":
                            fill_value = st.text_input(get_text('trans_missing_value', lang), value="Inconnu")
                        
                        if st.button(get_text('trans_missing_apply', lang), key="apply_na_cat"):
                            df_preview = st.session_state.df_working.copy()
                            
                            # Validation : vérifier qu'il y a encore des NaN
                            if df_preview[col_to_fix].isna().sum() == 0:
                                st.warning(get_text('trans_missing_none_warning', lang))
                                st.stop()
                            
                            try:
                                if strategy == "Valeur fixe":
                                    if not fill_value or fill_value.strip() == "":
                                        st.error(get_text('trans_missing_fixed_error', lang))
                                        st.stop()
                                    df_preview[col_to_fix].fillna(fill_value, inplace=True)
                                    st.success(get_text('trans_missing_fixed_success', lang).format(fill_value))
                                    
                                elif strategy == "Mode (valeur la plus fréquente)":
                                    mode_series = df_preview[col_to_fix].mode()
                                    if len(mode_series) == 0:
                                        st.error(get_text('trans_missing_mode_error', lang))
                                        st.stop()
                                    mode_val = mode_series[0]
                                    df_preview[col_to_fix].fillna(mode_val, inplace=True)
                                    st.success(get_text('trans_missing_mode_success', lang).format(mode_val))
                                    
                                elif strategy == "Supprimer les lignes":
                                    rows_before = len(df_preview)
                                    df_preview = df_preview.dropna(subset=[col_to_fix])
                                    rows_removed = rows_before - len(df_preview)
                                    
                                    if rows_removed == 0:
                                        st.warning(get_text('trans_missing_drop_warning', lang))
                                        st.stop()
                                    
                                    st.success(get_text('trans_missing_drop_success', lang).format(rows_removed))
                                
                                st.session_state.df_working = df_preview
                                st.session_state.transformations_applied.append({
                                    'type': 'fill_na_categorical', 
                                    'column': col_to_fix, 
                                    'strategy': strategy.lower(),
                                    'fill_value': fill_value if strategy == "Valeur fixe" else None,
                                    'description': f"NaN remplacés dans '{col_to_fix}' par {strategy}"
                                })
                                st.rerun()
                                
                            except Exception as e:
                                st.error(get_text('trans_missing_error', lang).format(str(e)))

                else:
                    st.success(get_text('trans_missing_none', lang))
            

            with tab2:
                st.write(get_text('trans_convert_title', lang))
                col_to_convert = st.selectbox(get_text('trans_convert_select', lang), df.columns.tolist(), key="convert_col_select")
                current_type = df[col_to_convert].dtype
                st.info(get_text('trans_convert_current', lang).format(current_type))
                target_type = st.selectbox(
    get_text('trans_convert_target', lang),
    [
        get_text('trans_convert_float', lang),
        get_text('trans_convert_int', lang),
        get_text('trans_convert_string', lang),
        get_text('trans_convert_datetime', lang)
    ],
    key="target_type"
)
                
                if st.button(get_text('trans_convert_apply', lang), key="apply_convert"):
                    df_preview = st.session_state.df_working.copy()
                    try:
                        if target_type == "Numérique (float)":
                            df_preview[col_to_convert] = pd.to_numeric(df_preview[col_to_convert], errors='coerce')
                            st.success(get_text('trans_convert_float_success', lang).format(col_to_convert))
                        elif target_type == "Numérique (int)":
                            df_preview[col_to_convert] = pd.to_numeric(df_preview[col_to_convert], errors='coerce').astype('Int64')
                            st.success(get_text('trans_convert_int_success', lang).format(col_to_convert))
                        elif target_type == "Texte (string)":
                            df_preview[col_to_convert] = df_preview[col_to_convert].astype(str)
                            st.success(get_text('trans_convert_string_success', lang).format(col_to_convert))
                        elif target_type == "Date/Heure":
                            df_preview[col_to_convert] = pd.to_datetime(df_preview[col_to_convert], errors='coerce')
                            st.success(get_text('trans_convert_datetime_success', lang).format(col_to_convert))
                        
                        st.session_state.df_working = df_preview
                        st.session_state.transformations_applied.append({
                            'type': 'convert_type', 'column': col_to_convert, 'target_type': target_type,
                            'description': f"Conversion '{col_to_convert}' en {target_type}"
                        })
                        st.rerun()
                    except Exception as e:
                        st.error(get_text('trans_convert_error', lang).format(str(e)))
            

            with tab3:
                st.write(get_text('trans_dup_title', lang))
                dup_count = df.duplicated().sum()
                if dup_count > 0:
                    st.warning(get_text('trans_dup_warning', lang).format(dup_count))
                    keep_strategy = st.radio(
    get_text('trans_dup_strategy', lang),
    [
        get_text('trans_dup_first', lang),
        get_text('trans_dup_last', lang),
        get_text('trans_dup_none', lang)
    ],
    key="dup_strategy"
)
                    
                    if st.button(get_text('trans_dup_apply', lang), key="apply_dup"):
                        df_preview = st.session_state.df_working.copy()
                        if keep_strategy == "Première":
                            df_preview = df_preview.drop_duplicates(keep='first')
                        elif keep_strategy == "Dernière":
                            df_preview = df_preview.drop_duplicates(keep='last')
                        else:
                            df_preview = df_preview.drop_duplicates(keep=False)
                        
                        st.success(get_text('trans_dup_success', lang).format(dup_count))
                        st.session_state.df_working = df_preview
                        st.session_state.transformations_applied.append({
                            'type': 'drop_duplicates', 'keep': keep_strategy.lower(),
                            'description': f"Doublons supprimés (stratégie: {keep_strategy})"
                        })
                        st.rerun()
                else:
                    st.success(get_text('trans_dup_no_duplicates', lang))
            

            with tab4:
                st.write(get_text('trans_filter_title', lang))
                
                if 'filters_list' not in st.session_state:
                    st.session_state.filters_list = []
                
                st.info(get_text('trans_filter_info', lang))
                
                # Section : Ajouter un filtre
                st.subheader(get_text('trans_filter_add_title', lang))
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    filter_col = st.selectbox(
                        get_text('trans_filter_column', lang),
                        df.columns.tolist(),
                        key="filter_col_select"
                    )
                
                with col2:
                    col_type = df[filter_col].dtype
                    
                    if col_type in ['int64', 'float64']:
                        filter_category = "Numérique"
                    elif pd.api.types.is_datetime64_any_dtype(df[filter_col]):
                        filter_category = "Date"
                    else:
                        filter_category = "Texte"
                    
                    st.metric(get_text('trans_filter_type', lang), filter_category)
                
                # Options de filtre selon le type
                if filter_category == "Numérique":
                    operator = st.selectbox(
                        "Opérateur",
                        ["Égal à", "Différent de", "Supérieur à", "Inférieur à", "Entre", "N'est pas entre"],
                        key="num_operator"
                    )
                    
                    if operator in ["Entre", "N'est pas entre"]:
                        col1, col2 = st.columns(2)
                        with col1:
                            min_val = st.number_input("Valeur min", value=float(df[filter_col].min()), key="num_min")
                        with col2:
                            max_val = st.number_input("Valeur max", value=float(df[filter_col].max()), key="num_max")
                        filter_value = (min_val, max_val)
                    else:
                        filter_value = st.number_input(
                            "Valeur",
                            value=float(df[filter_col].median()),
                            key="num_value"
                        )
                
                elif filter_category == "Date":
                    operator = st.selectbox(
                        "Opérateur",
                        ["Avant le", "Après le", "Entre", "N'est pas entre", "Égal à"],
                        key="date_operator"
                    )
                    
                    if operator in ["Entre", "N'est pas entre"]:
                        col1, col2 = st.columns(2)
                        with col1:
                            date_min = st.date_input("Date min", key="date_min")
                        with col2:
                            date_max = st.date_input("Date max", key="date_max")
                        filter_value = (pd.Timestamp(date_min), pd.Timestamp(date_max))
                    else:
                        date_val = st.date_input("Date", key="date_value")
                        filter_value = pd.Timestamp(date_val)
                
                else:  # Texte
                    operator = st.selectbox(
                        "Opérateur",
                        ["Contient", "Ne contient pas", "Égal à", "Différent de", "Commence par", "Finit par"],
                        key="text_operator"
                    )
                    
                    filter_value = st.text_input("Valeur", key="text_value")
                
                if st.button(get_text('trans_filter_add_btn', lang), key="add_filter_btn"):
                    if filter_value or operator in ["Entre", "N'est pas entre"]:
                        # Ajouter le filtre à la liste
                        st.session_state.filters_list.append({
                            'column': filter_col,
                            'category': filter_category,
                            'operator': operator,
                            'value': filter_value
                        })
                        st.success(get_text('trans_filter_add_success', lang).format(filter_col, operator, filter_value))
                        st.rerun()
                    else:
                        st.error(get_text('trans_filter_add_error', lang))
                
                # Section : Filtres actifs
                if st.session_state.filters_list:
                    st.divider()
                    st.subheader(get_text('trans_filter_active_title', lang))
                    
                    for i, f in enumerate(st.session_state.filters_list):
                        col1, col2 = st.columns([5, 1])
                        
                        with col1:
                            st.write(f"**{i+1}.** {f['column']} {f['operator']} {f['value']}")
                        
                        with col2:
                            if st.button(get_text('trans_filter_delete', lang), key=f"delete_filter_{i}"):
                                st.session_state.filters_list.pop(i)
                                st.rerun()
                    
                    st.divider()
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if st.button(get_text('trans_filter_reset', lang), key="reset_filters"):
                            st.session_state.filters_list = []
                            st.rerun()
                    
                    with col2:
                        if st.button(get_text('trans_filter_apply', lang), key="apply_filters"):
                            df_preview = st.session_state.df_working.copy()
                            initial_count = len(df_preview)
                            
                            # Appliquer chaque filtre
                            for f in st.session_state.filters_list:
                                col = f['column']
                                operator = f['operator']
                                value = f['value']
                                category = f['category']
                                
                                # FILTRES NUMÉRIQUES
                                if category == "Numérique":
                                    if operator == "Égal à":
                                        df_preview = df_preview[df_preview[col] == value]
                                    elif operator == "Différent de":
                                        df_preview = df_preview[df_preview[col] != value]
                                    elif operator == "Supérieur à":
                                        df_preview = df_preview[df_preview[col] > value]
                                    elif operator == "Inférieur à":
                                        df_preview = df_preview[df_preview[col] < value]
                                    elif operator == "Entre":
                                        df_preview = df_preview[(df_preview[col] >= value[0]) & (df_preview[col] <= value[1])]
                                    elif operator == "N'est pas entre":
                                        df_preview = df_preview[(df_preview[col] < value[0]) | (df_preview[col] > value[1])]
                                
                                # FILTRES DATES
                                elif category == "Date":
                                    if operator == "Avant le":
                                        df_preview = df_preview[df_preview[col] < value]
                                    elif operator == "Après le":
                                        df_preview = df_preview[df_preview[col] > value]
                                    elif operator == "Égal à":
                                        df_preview = df_preview[df_preview[col].dt.date == value.date()]
                                    elif operator == "Entre":
                                        df_preview = df_preview[(df_preview[col] >= value[0]) & (df_preview[col] <= value[1])]
                                    elif operator == "N'est pas entre":
                                        df_preview = df_preview[(df_preview[col] < value[0]) | (df_preview[col] > value[1])]
                                
                                # FILTRES TEXTE
                                else:
                                    if operator == "Contient":
                                        df_preview = df_preview[df_preview[col].str.contains(str(value), case=False, na=False)]
                                    elif operator == "Ne contient pas":
                                        df_preview = df_preview[~df_preview[col].str.contains(str(value), case=False, na=False)]
                                    elif operator == "Égal à":
                                        df_preview = df_preview[df_preview[col] == value]
                                    elif operator == "Différent de":
                                        df_preview = df_preview[df_preview[col] != value]
                                    elif operator == "Commence par":
                                        df_preview = df_preview[df_preview[col].str.startswith(str(value), na=False)]
                                    elif operator == "Finit par":
                                        df_preview = df_preview[df_preview[col].str.endswith(str(value), na=False)]
                            
                            final_count = len(df_preview)
                            removed_count = initial_count - final_count
                            
                            if final_count == 0:
                                st.error(get_text('trans_filter_no_results', lang))
                            else:
                                # Description des filtres
                                filter_descriptions = []
                                for f in st.session_state.filters_list:
                                    filter_descriptions.append(f"{f['column']} {f['operator']} {f['value']}")
                                
                                description = f"Filtrage appliqué : {' ET '.join(filter_descriptions)}"
                                
                                st.success(get_text('trans_filter_success', lang).format(final_count, removed_count))
                                
                                # Sauvegarder
                                st.session_state.df_working = df_preview
                                st.session_state.transformations_applied.append({
                                    'type': 'filter_rows',
                                    'filters': st.session_state.filters_list.copy(),
                                    'rows_before': initial_count,
                                    'rows_after': final_count,
                                    'description': description
                                })
                                
                                # Réinitialiser les filtres
                                st.session_state.filters_list = []
                                st.rerun()
                else:
                    st.info(get_text('trans_filter_none', lang))
            

            with tab5:
                st.write(get_text('trans_format_title', lang))
                
                # Initialiser le dictionnaire de formatage s'il n'existe pas
                if 'column_decimals' not in st.session_state:
                    st.session_state.column_decimals = {}
                
                numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
                
                if len(numeric_cols) > 0:
                    st.write(get_text('trans_format_choose', lang))
                    
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        selected_col = st.selectbox(
                            get_text('trans_format_column', lang),
                            numeric_cols,
                            key="format_col_select"
                        )
                    
                    with col2:
                        current_decimals = st.session_state.column_decimals.get(selected_col, 2)
                        decimals = st.number_input(
                            get_text('trans_format_decimals', lang),
                            min_value=0,
                            max_value=10,
                            value=current_decimals,
                            key="format_decimals"
                        )
                    
                    if st.button(get_text('trans_format_apply', lang), key="apply_format"):
                        st.session_state.column_decimals[selected_col] = decimals
                        st.success(get_text('trans_format_success', lang).format(selected_col, decimals))
                        st.rerun()
                    
                    # Afficher les formatages actuels
                    if st.session_state.column_decimals:
                        st.write(get_text('trans_format_current_title', lang))
                        format_df = pd.DataFrame([
                            {get_text('trans_format_col_label', lang): col, get_text('trans_format_dec_label', lang): dec}
                            for col, dec in st.session_state.column_decimals.items()
                        ])
                        st.dataframe(format_df, use_container_width=True, hide_index=True)
                        
                        if st.button(get_text('trans_format_reset', lang), key="reset_formats"):
                            st.session_state.column_decimals = {}
                            st.success(get_text('trans_format_reset_success', lang))
                            st.rerun()
                else:
                    st.info(get_text('trans_format_none', lang))


            with tab6:
                st.write(get_text('trans_text_title', lang))
                
                # Sous-tabs pour les opérations texte
                text_tab1, text_tab2, text_tab3, text_tab4 = st.tabs([
    get_text('trans_text_tab_clean', lang),
    get_text('trans_text_tab_extract', lang),
    get_text('trans_text_tab_split', lang),
    get_text('trans_text_tab_replace', lang)
])
                
                # ========== SOUS-TAB 1 : NETTOYAGE ==========
                with text_tab1:
                    st.write("**Nettoyer et transformer les colonnes textuelles**")
                    
                    text_cols = df.select_dtypes(include=['object']).columns.tolist()
                    
                    if len(text_cols) > 0:
                        selected_text_col = st.selectbox(
                            "Choisir une colonne texte à nettoyer",
                            text_cols,
                            key="text_clean_col"
                        )
                        
                        st.write(f"**Aperçu de '{selected_text_col}' (5 premières valeurs) :**")
                        st.code("\n".join(df[selected_text_col].dropna().head(5).astype(str).tolist()))
                        
                        cleaning_option = st.radio(
                            "Type de nettoyage",
                            [
                                "Supprimer espaces début/fin (trim)",
                                "Convertir en minuscules",
                                "Convertir en majuscules",
                                "Convertir en title case (Première Lettre Majuscule)",
                                "Remplacer une valeur",
                                "Supprimer caractères spéciaux"
                            ],
                            key="cleaning_option"
                        )
                        
                        replace_from = None
                        replace_to = None
                        
                        if cleaning_option == "Remplacer une valeur":
                            col1, col2 = st.columns(2)
                            with col1:
                                replace_from = st.text_input("Valeur à remplacer", key="replace_from")
                            with col2:
                                replace_to = st.text_input("Remplacer par", key="replace_to")
                        
                        if st.button("Appliquer le nettoyage", key="apply_text_clean"):
                            df_preview = st.session_state.df_working.copy()
                            
                            if cleaning_option == "Supprimer espaces début/fin (trim)":
                                df_preview[selected_text_col] = df_preview[selected_text_col].str.strip()
                                description = f"Espaces supprimés dans '{selected_text_col}'"
                                st.success(f"✅ {description}")
                                
                            elif cleaning_option == "Convertir en minuscules":
                                df_preview[selected_text_col] = df_preview[selected_text_col].str.lower()
                                description = f"'{selected_text_col}' converti en minuscules"
                                st.success(f"✅ {description}")
                                
                            elif cleaning_option == "Convertir en majuscules":
                                df_preview[selected_text_col] = df_preview[selected_text_col].str.upper()
                                description = f"'{selected_text_col}' converti en majuscules"
                                st.success(f"✅ {description}")
                                
                            elif cleaning_option == "Convertir en title case (Première Lettre Majuscule)":
                                df_preview[selected_text_col] = df_preview[selected_text_col].str.title()
                                description = f"'{selected_text_col}' converti en title case"
                                st.success(f"✅ {description}")
                                
                            elif cleaning_option == "Remplacer une valeur":
                                if replace_from and replace_to is not None:
                                    df_preview[selected_text_col] = df_preview[selected_text_col].str.replace(replace_from, replace_to, regex=False)
                                    description = f"'{replace_from}' remplacé par '{replace_to}' dans '{selected_text_col}'"
                                    st.success(f"✅ {description}")
                                else:
                                    st.error("❌ Veuillez renseigner les deux valeurs")
                                    st.stop()
                                    
                            elif cleaning_option == "Supprimer caractères spéciaux":
                                df_preview[selected_text_col] = df_preview[selected_text_col].str.replace(r'[^a-zA-Z0-9\s]', '', regex=True)
                                description = f"Caractères spéciaux supprimés dans '{selected_text_col}'"
                                st.success(f"✅ {description}")
                            
                            st.session_state.df_working = df_preview
                            st.session_state.transformations_applied.append({
                                'type': 'text_cleaning',
                                'column': selected_text_col,
                                'operation': cleaning_option,
                                'replace_from': replace_from,
                                'replace_to': replace_to,
                                'description': description
                            })
                            st.rerun()
                    else:
                        st.info(get_text('trans_text_no_columns', lang))
                
                # ========== SOUS-TAB 2 : EXTRACTION ==========
                with text_tab2:
                    st.write("**Extraire des informations depuis une colonne texte**")
                    
                    text_cols = df.select_dtypes(include=['object']).columns.tolist()
                    
                    if len(text_cols) > 0:
                        col1, col2 = st.columns([2, 1])
                        
                        with col1:
                            source_col = st.selectbox(
                                "Colonne source (contenant les données à extraire)",
                                text_cols,
                                key="extract_source_col"
                            )
                        
                        with col2:
                            new_col_name = st.text_input(
                                "Nom de la nouvelle colonne",
                                value=f"{source_col}_extracted",
                                key="extract_new_col"
                            )
                        
                        st.write(f"**Aperçu de '{source_col}' (5 premières valeurs) :**")
                        st.code("\n".join(df[source_col].dropna().head(5).astype(str).tolist()))
                        
                        extraction_type = st.radio(
                            "Type d'extraction",
                            [
                                "Email",
                                "Numéro de téléphone (France)",
                                "Code postal (France - 5 chiffres)",
                                "URL",
                                "Pattern personnalisé (regex)"
                            ],
                            key="extraction_type"
                        )
                        
                        custom_pattern = None
                        if extraction_type == "Pattern personnalisé (regex)":
                            st.info("💡 Exemples de patterns : `\\d{5}` (5 chiffres), `CMD-\\d+` (CMD- suivi de chiffres)")
                            custom_pattern = st.text_input(
                                "Pattern regex",
                                value=r"\d+",
                                help="Expression régulière pour extraire le pattern souhaité",
                                key="custom_pattern"
                            )
                        
                        if st.button("Extraire les données", key="apply_extraction"):
                            df_preview = st.session_state.df_working.copy()
                            
                            if extraction_type == "Email":
                                pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
                                description = f"Emails extraits de '{source_col}' vers '{new_col_name}'"
                                
                            elif extraction_type == "Numéro de téléphone (France)":
                                pattern = r'0[1-9]\d{8}'
                                description = f"Téléphones extraits de '{source_col}' vers '{new_col_name}'"
                                
                            elif extraction_type == "Code postal (France - 5 chiffres)":
                                pattern = r'\b\d{5}\b'
                                description = f"Codes postaux extraits de '{source_col}' vers '{new_col_name}'"
                                
                            elif extraction_type == "URL":
                                pattern = r'https?://[^\s]+'
                                description = f"URLs extraites de '{source_col}' vers '{new_col_name}'"
                                
                            elif extraction_type == "Pattern personnalisé (regex)":
                                pattern = custom_pattern
                                description = f"Pattern '{pattern}' extrait de '{source_col}' vers '{new_col_name}'"
                            
                            try:
                                if '(' in pattern and ')' in pattern:
                                    df_preview[new_col_name] = df_preview[source_col].str.extract(pattern, expand=False)
                                else:
                                    df_preview[new_col_name] = df_preview[source_col].str.extract(f'({pattern})', expand=False)
                                
                                extracted_count = df_preview[new_col_name].notna().sum()
                                total_count = len(df_preview)
                                
                                st.success(f"✅ {description}")
                                st.info(f"📊 {extracted_count}/{total_count} valeurs extraites ({extracted_count/total_count*100:.1f}%)")
                                
                                st.write("**Aperçu des valeurs extraites (5 premières) :**")
                                preview_df = df_preview[[source_col, new_col_name]].head(5)
                                st.dataframe(preview_df, use_container_width=True)
                                
                                st.session_state.df_working = df_preview
                                st.session_state.transformations_applied.append({
                                    'type': 'extract_pattern',
                                    'source_column': source_col,
                                    'new_column': new_col_name,
                                    'extraction_type': extraction_type,
                                    'pattern': pattern,
                                    'description': description
                                })
                                st.rerun()
                                
                            except Exception as e:
                                st.error(f"❌ Erreur lors de l'extraction : {str(e)}")
                                st.info("💡 Vérifiez votre pattern regex si vous utilisez un pattern personnalisé")
                    else:
                        st.info(get_text('trans_text_no_columns', lang))
                
                # ========== SOUS-TAB 3 : SPLIT COLONNES ==========
                with text_tab3:
                    st.write("**Séparer une colonne en plusieurs colonnes**")
                    
                    text_cols = df.select_dtypes(include=['object']).columns.tolist()
                    
                    if len(text_cols) > 0:
                        source_col = st.selectbox(
                            "Colonne à séparer",
                            text_cols,
                            key="split_source_col"
                        )
                        
                        st.write(f"**Aperçu de '{source_col}' (5 premières valeurs) :**")
                        st.code("\n".join(df[source_col].dropna().head(5).astype(str).tolist()))
                        
                        split_type = st.radio(
                            "Comment séparer ?",
                            [
                                "Par séparateur (espace, virgule, etc.)",
                                "Position fixe (premiers X caractères)",
                                "Pattern regex"
                            ],
                            key="split_type"
                        )
                        
                        separator = None
                        n_splits = 2
                        position = None
                        pattern = None
                        
                        if split_type == "Par séparateur (espace, virgule, etc.)":
                            col1, col2 = st.columns([2, 1])
                            
                            with col1:
                                separator = st.text_input(
                                    "Séparateur",
                                    value=" ",
                                    help="Ex: espace, virgule, tiret, @, etc.",
                                    key="split_separator"
                                )
                            
                            with col2:
                                n_splits = st.number_input(
                                    "Nombre de colonnes",
                                    min_value=2,
                                    max_value=10,
                                    value=2,
                                    help="Nombre de colonnes à créer",
                                    key="split_n_cols"
                                )
                            
                            st.info(f"💡 Exemple : 'Jean Dupont' → sépare par '{separator}' en {n_splits} colonne(s)")
                        
                        elif split_type == "Position fixe (premiers X caractères)":
                            position = st.number_input(
                                "Nombre de caractères à extraire au début",
                                min_value=1,
                                max_value=100,
                                value=5,
                                help="Ex: 5 pour extraire les 5 premiers caractères",
                                key="split_position"
                            )
                            
                            st.info(f"💡 Exemple : '75001 Paris' → Colonne 1: premiers {position} caractères, Colonne 2: le reste")
                        
                        elif split_type == "Pattern regex":
                            pattern = st.text_input(
                                "Pattern regex (séparateur)",
                                value=r"\s+",
                                help="Ex: \\s+ (un ou plusieurs espaces), [,;] (virgule ou point-virgule)",
                                key="split_pattern"
                            )
                            
                            n_splits = st.number_input(
                                "Nombre de colonnes",
                                min_value=2,
                                max_value=10,
                                value=2,
                                key="split_pattern_n_cols"
                            )
                        
                        st.write("**Noms des nouvelles colonnes :**")
                        
                        if split_type == "Position fixe (premiers X caractères)":
                            n_splits = 2
                        
                        new_col_names = []
                        cols = st.columns(n_splits)
                        
                        for i in range(n_splits):
                            with cols[i]:
                                col_name = st.text_input(
                                    f"Colonne {i+1}",
                                    value=f"{source_col}_{i+1}",
                                    key=f"split_new_col_{i}"
                                )
                                new_col_names.append(col_name)
                        
                        if st.button("Séparer la colonne", key="apply_split"):
                            df_preview = st.session_state.df_working.copy()
                            
                            try:
                                if split_type == "Par séparateur (espace, virgule, etc.)":
                                    split_data = df_preview[source_col].str.split(separator, n=n_splits-1, expand=True)
                                    
                                    for i, col_name in enumerate(new_col_names):
                                        if i < split_data.shape[1]:
                                            df_preview[col_name] = split_data[i]
                                        else:
                                            df_preview[col_name] = None
                                    
                                    description = f"'{source_col}' séparé par '{separator}' en {n_splits} colonne(s)"
                                    transformation_info = {
                                        'split_method': 'separator',
                                        'separator': separator,
                                        'n_splits': n_splits
                                    }
                                
                                elif split_type == "Position fixe (premiers X caractères)":
                                    df_preview[new_col_names[0]] = df_preview[source_col].str[:position]
                                    df_preview[new_col_names[1]] = df_preview[source_col].str[position:].str.strip()
                                    
                                    description = f"'{source_col}' séparé à la position {position}"
                                    transformation_info = {
                                        'split_method': 'position',
                                        'position': position
                                    }
                                
                                elif split_type == "Pattern regex":
                                    split_data = df_preview[source_col].str.split(pattern, n=n_splits-1, expand=True, regex=True)
                                    
                                    for i, col_name in enumerate(new_col_names):
                                        if i < split_data.shape[1]:
                                            df_preview[col_name] = split_data[i]
                                        else:
                                            df_preview[col_name] = None
                                    
                                    description = f"'{source_col}' séparé par pattern '{pattern}' en {n_splits} colonne(s)"
                                    transformation_info = {
                                        'split_method': 'regex',
                                        'pattern': pattern,
                                        'n_splits': n_splits
                                    }
                                
                                st.success(f"✅ {description}")
                                
                                st.write("**Aperçu du résultat (5 premières lignes) :**")
                                preview_cols = [source_col] + new_col_names
                                st.dataframe(df_preview[preview_cols].head(5), use_container_width=True)
                                
                                st.session_state.df_working = df_preview
                                st.session_state.transformations_applied.append({
                                    'type': 'split_column',
                                    'source_column': source_col,
                                    'new_columns': new_col_names,
                                    'description': description,
                                    **transformation_info
                                })
                                st.rerun()
                                
                            except Exception as e:
                                st.error(f"❌ Erreur lors de la séparation : {str(e)}")
                                st.info("💡 Vérifiez que le séparateur existe bien dans vos données")
                    else:
                        st.info(get_text('trans_text_no_columns', lang))

                # ========== SOUS-TAB 4 : FIND & REPLACE AVANCÉ ==========
                with text_tab4:
                    st.write("**Rechercher et remplacer avec patterns avancés**")
                    
                    text_cols = df.select_dtypes(include=['object']).columns.tolist()
                    
                    if len(text_cols) > 0:
                        selected_col = st.selectbox(
                            "Colonne à modifier",
                            text_cols,
                            key="findreplace_col"
                        )
                        
                        st.write(f"**Aperçu de '{selected_col}' (5 premières valeurs) :**")
                        st.code("\n".join(df[selected_col].dropna().head(5).astype(str).tolist()))
                        
                        # Mode de recherche
                        search_mode = st.radio(
                            "Mode de recherche",
                            [
                                "Texte exact",
                                "Pattern regex",
                                "Remplacements multiples"
                            ],
                            key="search_mode"
                        )
                        
                        # MODE 1 : Texte exact
                        if search_mode == "Texte exact":
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                search_text = st.text_input(
                                    "Texte à chercher",
                                    key="search_text"
                                )
                            
                            with col2:
                                replace_text = st.text_input(
                                    "Remplacer par",
                                    key="replace_text"
                                )
                            
                            case_sensitive = st.checkbox(
                                "Sensible à la casse (Maj/min)",
                                value=False,
                                key="case_sensitive"
                            )
                            
                            if st.button("Remplacer", key="apply_exact_replace"):
                                if search_text:
                                    df_preview = st.session_state.df_working.copy()
                                    
                                    df_preview[selected_col] = df_preview[selected_col].str.replace(
                                        search_text, 
                                        replace_text, 
                                        case=case_sensitive,
                                        regex=False
                                    )
                                    
                                    description = f"'{search_text}' → '{replace_text}' dans '{selected_col}'"
                                    if not case_sensitive:
                                        description += " (insensible casse)"
                                    
                                    st.success(f"✅ {description}")
                                    
                                    st.session_state.df_working = df_preview
                                    st.session_state.transformations_applied.append({
                                        'type': 'find_replace',
                                        'column': selected_col,
                                        'method': 'exact',
                                        'search': search_text,
                                        'replace': replace_text,
                                        'case_sensitive': case_sensitive,
                                        'description': description
                                    })
                                    st.rerun()
                                else:
                                    st.error("❌ Veuillez saisir un texte à chercher")
                        
                        # MODE 2 : Pattern regex
                        elif search_mode == "Pattern regex":
                            st.info("💡 Exemples : `\\d+` (chiffres), `[aeiou]` (voyelles), `\\s+` (espaces)")
                            
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                regex_pattern = st.text_input(
                                    "Pattern regex à chercher",
                                    value=r"\d+",
                                    key="regex_pattern"
                                )
                            
                            with col2:
                                regex_replace = st.text_input(
                                    "Remplacer par",
                                    key="regex_replace"
                                )
                            
                            st.write("**Exemples de patterns utiles :**")
                            st.markdown("""
                            - `\\d+` : Tous les chiffres
                            - `\\s+` : Espaces multiples → un seul espace
                            - `[^a-zA-Z0-9]` : Tous les caractères spéciaux
                            - `^\\s+|\\s+$` : Espaces début/fin
                            - `(\\d{2})/(\\d{2})/(\\d{4})` : Dates DD/MM/YYYY
                            """)
                            
                            if st.button("Remplacer (regex)", key="apply_regex_replace"):
                                if regex_pattern:
                                    df_preview = st.session_state.df_working.copy()
                                    
                                    try:
                                        df_preview[selected_col] = df_preview[selected_col].str.replace(
                                            regex_pattern,
                                            regex_replace,
                                            regex=True
                                        )
                                        
                                        description = f"Pattern '{regex_pattern}' → '{regex_replace}' dans '{selected_col}'"
                                        
                                        st.success(f"✅ {description}")
                                        
                                        st.write("**Aperçu du résultat (5 premières) :**")
                                        st.dataframe(df_preview[[selected_col]].head(5), use_container_width=True)
                                        
                                        st.session_state.df_working = df_preview
                                        st.session_state.transformations_applied.append({
                                            'type': 'find_replace',
                                            'column': selected_col,
                                            'method': 'regex',
                                            'pattern': regex_pattern,
                                            'replace': regex_replace,
                                            'description': description
                                        })
                                        st.rerun()
                                        
                                    except Exception as e:
                                        st.error(f"❌ Erreur regex : {str(e)}")
                                        st.info("💡 Vérifiez la syntaxe de votre pattern regex")
                                else:
                                    st.error("❌ Veuillez saisir un pattern")
                        
                        # MODE 3 : Remplacements multiples
                        elif search_mode == "Remplacements multiples":
                            st.info("💡 Définissez plusieurs remplacements à appliquer en une seule fois")
                            
                            # Initialiser la liste de remplacements
                            if 'multi_replacements' not in st.session_state:
                                st.session_state.multi_replacements = [{"search": "", "replace": ""}]
                            
                            st.write("**Liste des remplacements :**")
                            
                            # Afficher les paires de remplacement
                            for i, replacement in enumerate(st.session_state.multi_replacements):
                                col1, col2, col3 = st.columns([5, 5, 1])
                                
                                with col1:
                                    search = st.text_input(
                                        f"Chercher",
                                        value=replacement["search"],
                                        key=f"multi_search_{i}",
                                        label_visibility="collapsed"
                                    )
                                
                                with col2:
                                    replace = st.text_input(
                                        f"Remplacer par",
                                        value=replacement["replace"],
                                        key=f"multi_replace_{i}",
                                        label_visibility="collapsed"
                                    )
                                
                                with col3:
                                    if st.button("Supprimer", key=f"delete_multi_{i}"):
                                        st.session_state.multi_replacements.pop(i)
                                        st.rerun()
                                
                                st.session_state.multi_replacements[i] = {"search": search, "replace": replace}
                            
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                if st.button("➕ Ajouter un remplacement", key="add_multi"):
                                    st.session_state.multi_replacements.append({"search": "", "replace": ""})
                                    st.rerun()
                            
                            with col2:
                                if st.button("Appliquer tous les remplacements", key="apply_multi"):
                                    # Filtrer les remplacements vides
                                    valid_replacements = [
                                        r for r in st.session_state.multi_replacements 
                                        if r["search"] != ""
                                    ]
                                    
                                    if valid_replacements:
                                        df_preview = st.session_state.df_working.copy()
                                        
                                        # Appliquer chaque remplacement
                                        for r in valid_replacements:
                                            df_preview[selected_col] = df_preview[selected_col].str.replace(
                                                r["search"],
                                                r["replace"],
                                                regex=False
                                            )
                                        
                                        description = f"{len(valid_replacements)} remplacements dans '{selected_col}'"
                                        
                                        st.success(f"✅ {description}")
                                        
                                        st.write("**Remplacements appliqués :**")
                                        for r in valid_replacements:
                                            st.write(f"- '{r['search']}' → '{r['replace']}'")
                                        
                                        st.session_state.df_working = df_preview
                                        st.session_state.transformations_applied.append({
                                            'type': 'find_replace',
                                            'column': selected_col,
                                            'method': 'multiple',
                                            'replacements': valid_replacements,
                                            'description': description
                                        })
                                        
                                        # Réinitialiser la liste
                                        st.session_state.multi_replacements = [{"search": "", "replace": ""}]
                                        st.rerun()
                                    else:
                                        st.error("❌ Aucun remplacement valide défini")

                            
                    else:
                        st.info(get_text('trans_text_no_columns', lang))

            # Suggestions de nettoyage
            st.subheader(get_text('trans_suggestions', lang))
            suggestions = []
            
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
            
            if duplicates_count > 0:
                suggestions.append({
                    'priorité': '🟠 IMPORTANTE',
                    'problème': f"{duplicates_count} lignes dupliquées",
                    'action': "Supprimer les doublons (garder première occurrence)",
                    'raison': "Les doublons faussent les analyses statistiques"
                })
            
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
            
            if suggestions:
                st.write(f"**{get_text('trans_suggestions_count', lang).format(len(suggestions))}**")
                suggestions_df = pd.DataFrame(suggestions)
                priority_order = {'🔴 HAUTE': 0, '🟠 IMPORTANTE': 1, '🟡 MOYENNE': 2}
                suggestions_df['_sort'] = suggestions_df['priorité'].map(priority_order)
                suggestions_df = suggestions_df.sort_values('_sort').drop('_sort', axis=1)
                st.dataframe(suggestions_df, use_container_width=True, hide_index=True,
                    column_config={
                        'priorité': st.column_config.TextColumn(get_text('trans_priority', lang), width='small'),
                        'problème': st.column_config.TextColumn(get_text('trans_problem', lang), width='medium'),
                        'action': st.column_config.TextColumn(get_text('trans_action', lang), width='medium'),
                        'raison': st.column_config.TextColumn(get_text('trans_reason', lang), width='medium')
                    })
                st.info(get_text('trans_suggestions_next', lang))
            else:
                st.success(get_text('trans_suggestions_clean', lang))
        
        # ========== TAB 3 : EXPORT ==========
        with tab_export:
            st.subheader(get_text('export_title', lang))
            
            st.write(get_text('export_download', lang))
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                # Export CSV
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label=get_text('export_csv', lang),
                    data=csv,
                    file_name=f"cleaned_{st.session_state.get('last_file', 'data')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            with col2:
                # Export Excel
                buffer = BytesIO()
                with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False, sheet_name='Données nettoyées')
                
                st.download_button(
                    label=get_text('export_excel', lang),
                    data=buffer.getvalue(),
                    file_name=f"cleaned_{st.session_state.get('last_file', 'data').replace('.csv', '')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
            
            with col3:
                # Export JSON
                json_str = df.to_json(orient='records', indent=2, force_ascii=False)
                st.download_button(
                    label=get_text('export_json', lang),
                    data=json_str,
                    file_name=f"cleaned_{st.session_state.get('last_file', 'data').replace('.csv', '').replace('.xlsx', '')}.json",
                    mime="application/json",
                    use_container_width=True)
            st.info(get_text('export_info', lang).format(len(df), len(df.columns)))

            st.divider()
    
            # Génération de code Python
            st.subheader(get_text('export_code_title', lang))
            
            if 'transformations_applied' in st.session_state and len(st.session_state.transformations_applied) > 0:
                st.write(get_text('export_code_copy', lang))
                
                python_code = generate_python_code(
                    st.session_state.transformations_applied,
                    st.session_state.get('last_file', 'data.csv')
                )
                
                st.code(python_code, language='python')
                
                # Bouton pour copier
                st.download_button(
                    label=get_text('export_code_download', lang),
                    data=python_code,
                    file_name="cleaning_script.py",
                    mime="text/x-python",
                    use_container_width=True
                )
            else:
                st.info(get_text('export_code_none', lang))

        # ========== TAB 4 : TEMPLATES ==========
        with tab_templates:
            st.subheader(get_text('templates_title', lang))
            
            st.info(get_text('templates_info', lang))
            
            # Deux colonnes : Sauvegarder / Charger
            col1, col2 = st.columns(2)
            
            # ===== COLONNE 1 : SAUVEGARDER =====
            with col1:
                st.write(get_text('templates_save', lang))
                
                if 'transformations_applied' in st.session_state and len(st.session_state.transformations_applied) > 0:
                    st.success(get_text('templates_success_count', lang).format(len(st.session_state.transformations_applied)))
                    
                    template_name = st.text_input(
                        get_text('templates_name', lang),
                        placeholder=get_text('templates_name_placeholder', lang),
                        key="template_name_input"
                    )
                    
                    if st.button(get_text('templates_save_btn', lang), key="save_template_btn"):
                        if template_name:
                            try:
                                filepath = save_template(template_name, st.session_state.transformations_applied)
                                st.success(get_text('templates_save_success', lang).format(template_name))
                                st.info(get_text('templates_save_file', lang).format(filepath))
                                st.rerun()
                            except Exception as e:
                                st.error(get_text('templates_save_error', lang).format(str(e)))
                        else:
                            st.error(get_text('templates_name_error', lang))
                else:
                    st.warning(get_text('templates_no_trans', lang))
            
            # ===== COLONNE 2 : CHARGER =====
            with col2:
                st.write(get_text('templates_load', lang))
                
                templates = load_templates()
                
                if templates:
                    st.success(get_text('templates_available', lang).format(len(templates)))
                    
                    # Sélection du template
                    template_options = {t['name']: t for t in templates}
                    selected_template_name = st.selectbox(
                        get_text('templates_select', lang),
                        options=list(template_options.keys()),
                        key="template_select"
                    )
                    
                    selected_template = template_options[selected_template_name]
                    
                    # Infos du template
                    st.write(get_text('templates_info_title', lang))
                    st.write(f"{get_text('templates_created', lang).format(selected_template['created_at'][:10])}")
                    st.write(f"{get_text('templates_trans_count', lang).format(selected_template['count'])}")
                    
                    col_load, col_delete = st.columns(2)
                    
                    with col_load:
                        if st.button(get_text('templates_apply', lang), key="load_template_btn"):
                            try:
                                # Charger les transformations du template
                                template_data = load_template_data(selected_template['filepath'])
                                template_transformations = template_data['transformations']
                                
                                # Validation : vérifier compatibilité basique
                                if len(template_transformations) == 0:
                                    st.warning(get_text('templates_no_trans_warning', lang))
                                    st.stop()
                                
                                # Appliquer toutes les transformations
                                df_result = st.session_state.df_original.copy()
                                
                                success_count = 0
                                warning_count = 0
                                
                                for transformation in template_transformations:
                                    df_before = len(df_result)
                                    df_result = replay_transformation(df_result, transformation)
                                    
                                    # Compter si la transformation a réussi
                                    if len(df_result) > 0:
                                        success_count += 1
                                    else:
                                        warning_count += 1
                                
                                if len(df_result) == 0:
                                    st.error(get_text('templates_all_deleted', lang))
                                    st.info(get_text('templates_incompatible', lang))
                                    st.stop()
                                
                                # Mettre à jour
                                st.session_state.df_working = df_result
                                st.session_state.transformations_applied = template_transformations.copy()
                                
                                if warning_count > 0:
                                    st.warning(get_text('templates_warning_count', lang).format(warning_count))
                                st.success(get_text('templates_success_apply', lang).format(selected_template_name, success_count, len(template_transformations)))
                                st.rerun()
                                
                            except Exception as e:
                                st.error(get_text('templates_error', lang).format(str(e)))
                                st.info(get_text('templates_check_compat', lang))

                    
                    with col_delete:
                        if st.button(get_text('templates_delete', lang), key="delete_template_btn"):
                            try:
                                delete_template(selected_template['filepath'])
                                st.success(get_text('templates_delete_success', lang).format(selected_template_name))
                                st.rerun()
                            except Exception as e:
                                st.error(get_text('templates_delete_error', lang).format(str(e)))
                else:
                    st.info(get_text('templates_none', lang))
               

    except Exception as e:
        st.error(f"❌ Erreur lors du chargement du fichier : {str(e)}")
        st.info("Vérifiez que votre fichier est bien formaté.")

else:
    st.info(get_text('upload_info', lang))
