"""
Module de profiling et analyse de données.
Contient toutes les fonctions d'analyse et de détection d'anomalies.
"""

import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import missingno as msno
import matplotlib.pyplot as plt
import seaborn as sns


def get_basic_info(df):
    """
    Retourne les informations de base du DataFrame.
    
    Args:
        df: DataFrame pandas
        
    Returns:
        dict: Informations de base (lignes, colonnes, mémoire)
    """
    memory_usage = df.memory_usage(deep=True).sum() / 1024**2  # En MB
    
    return {
        'rows': len(df),
        'columns': len(df.columns),
        'memory_mb': round(memory_usage, 2)
    }


def get_missing_values_summary(df):
    """
    Analyse des valeurs manquantes.
    
    Args:
        df: DataFrame pandas
        
    Returns:
        DataFrame: Résumé des valeurs manquantes par colonne
    """
    missing_data = []
    
    for col in df.columns:
        missing_count = df[col].isna().sum()
        missing_pct = (missing_count / len(df)) * 100
        
        if missing_count > 0:
            missing_data.append({
                'Colonne': col,
                'Valeurs manquantes': missing_count,
                'Pourcentage': f"{missing_pct:.2f}%"
            })
    
    if missing_data:
        return pd.DataFrame(missing_data)
    else:
        return None


def get_data_types_summary(df):
    """
    Résumé des types de données.
    
    Args:
        df: DataFrame pandas
        
    Returns:
        DataFrame: Comptage par type de données
    """
    type_counts = df.dtypes.value_counts()
    
    summary = pd.DataFrame({
        'Type': type_counts.index.astype(str),
        'Nombre de colonnes': type_counts.values
    })
    
    return summary


def detect_date_columns(df):
    """
    Détecte les colonnes de type date.
    
    Args:
        df: DataFrame pandas
        
    Returns:
        list: Liste des noms de colonnes de type date
    """
    date_cols = []
    
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            date_cols.append(col)
    
    return date_cols


def analyze_date_column(df, col):
    """
    Analyse détaillée d'une colonne date.
    
    Args:
        df: DataFrame pandas
        col: Nom de la colonne
        
    Returns:
        dict: Statistiques de la colonne date
    """
    date_series = df[col].dropna()
    
    if len(date_series) == 0:
        return None
    
    return {
        'min': date_series.min(),
        'max': date_series.max(),
        'range_days': (date_series.max() - date_series.min()).days,
        'count': len(date_series)
    }


def detect_numeric_anomalies(df, col, threshold=3):
    """
    Détecte les anomalies dans une colonne numérique (méthode Z-score).
    
    Args:
        df: DataFrame pandas
        col: Nom de la colonne
        threshold: Seuil Z-score (défaut: 3)
        
    Returns:
        dict: Informations sur les anomalies détectées
    """
    if df[col].dtype not in ['int64', 'float64']:
        return None
    
    data = df[col].dropna()
    
    if len(data) == 0:
        return None
    
    mean = data.mean()
    std = data.std()
    
    if std == 0:
        return None
    
    z_scores = np.abs((data - mean) / std)
    anomalies = data[z_scores > threshold]
    
    return {
        'count': len(anomalies),
        'percentage': (len(anomalies) / len(data)) * 100,
        'values': anomalies.tolist()[:5]  # 5 premiers exemples
    }


def detect_text_anomalies(df, col):
    """
    Détecte les anomalies dans une colonne texte (longueurs inhabituelles).
    
    Args:
        df: DataFrame pandas
        col: Nom de la colonne
        
    Returns:
        dict: Informations sur les anomalies de longueur
    """
    if df[col].dtype != 'object':
        return None
    
    data = df[col].dropna().astype(str)
    
    if len(data) == 0:
        return None
    
    lengths = data.str.len()
    mean_length = lengths.mean()
    std_length = lengths.std()
    
    if std_length == 0:
        return None
    
    # Détecter les textes anormalement courts ou longs
    z_scores = np.abs((lengths - mean_length) / std_length)
    anomalies = data[z_scores > 3]
    
    return {
        'count': len(anomalies),
        'percentage': (len(anomalies) / len(data)) * 100,
        'mean_length': round(mean_length, 1),
        'examples': anomalies.tolist()[:3]
    }


def create_missing_heatmap(df):
    """
    Crée une heatmap des valeurs manquantes.
    
    Args:
        df: DataFrame pandas
        
    Returns:
        matplotlib figure
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    msno.heatmap(df, ax=ax)
    return fig


def create_distribution_plots(df):
    """
    Crée des graphiques de distribution pour les colonnes numériques.
    
    Args:
        df: DataFrame pandas
        
    Returns:
        list: Liste de figures plotly
    """
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    
    if not numeric_cols:
        return []
    
    figures = []
    
    for col in numeric_cols[:5]:  # Max 5 colonnes
        fig = px.histogram(
            df, 
            x=col,
            title=f"Distribution de {col}",
            nbins=30
        )
        fig.update_layout(
            showlegend=False,
            height=300
        )
        figures.append(fig)
    
    return figures


def get_column_stats(df, col):
    """
    Statistiques détaillées pour une colonne.
    
    Args:
        df: DataFrame pandas
        col: Nom de la colonne
        
    Returns:
        dict: Statistiques de la colonne
    """
    col_data = df[col]
    
    stats = {
        'type': str(col_data.dtype),
        'count': len(col_data),
        'missing': col_data.isna().sum(),
        'missing_pct': (col_data.isna().sum() / len(col_data)) * 100
    }
    
    # Stats numériques
    if col_data.dtype in ['int64', 'float64']:
        stats.update({
            'mean': col_data.mean(),
            'median': col_data.median(),
            'std': col_data.std(),
            'min': col_data.min(),
            'max': col_data.max(),
            'q25': col_data.quantile(0.25),
            'q75': col_data.quantile(0.75)
        })
    
    # Stats texte
    elif col_data.dtype == 'object':
        non_null = col_data.dropna()
        if len(non_null) > 0:
            stats.update({
                'unique': col_data.nunique(),
                'most_common': col_data.value_counts().index[0] if len(non_null) > 0 else None,
                'most_common_count': col_data.value_counts().values[0] if len(non_null) > 0 else 0
            })
    
    return stats

def detect_date_formats_in_column(series):
    """
    Détecte les différents formats de dates dans une colonne.
    
    Args:
        series: Série pandas (une colonne)
        
    Returns:
        dict: Formats détectés avec leur fréquence
    """
    date_formats = [
        '%Y-%m-%d',
        '%d/%m/%Y',
        '%m/%d/%Y',
        '%Y/%m/%d',
        '%d-%m-%Y',
        '%m-%d-%Y',
        '%d.%m.%Y',
        '%Y%m%d',
    ]
    
    format_counts = {}
    
    for date_format in date_formats:
        try:
            parsed = pd.to_datetime(series, format=date_format, errors='coerce')
            valid_count = parsed.notna().sum()
            if valid_count > 0:
                format_counts[date_format] = valid_count
        except:
            continue
    
    return format_counts