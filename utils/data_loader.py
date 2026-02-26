"""
Module de chargement de fichiers.
Gère CSV, Excel, JSON avec détection automatique des types et dates.
"""

import pandas as pd
import streamlit as st
from datetime import datetime


def detect_date_formats(df):
    """
    Détecte et convertit automatiquement les colonnes de dates.
    
    Args:
        df: DataFrame pandas
        
    Returns:
        DataFrame avec colonnes dates converties
    """
    date_formats = [
        '%Y-%m-%d',
        '%d/%m/%Y',
        '%m/%d/%Y',
        '%Y/%m/%d',
        '%d-%m-%Y',
        '%Y-%m-%d %H:%M:%S',
        '%d/%m/%Y %H:%M:%S'
    ]
    
    for col in df.columns:
        if df[col].dtype == 'object':
            for date_format in date_formats:
                try:
                    df[col] = pd.to_datetime(df[col], format=date_format)
                    break
                except:
                    continue
    
    return df


def load_file(uploaded_file):
    """
    Charge un fichier CSV, Excel ou JSON.
    
    Args:
        uploaded_file: Fichier uploadé via st.file_uploader
        
    Returns:
        tuple: (DataFrame, nom_fichier) ou (None, None) si erreur
    """
    try:
        filename = uploaded_file.name
        
        # CSV
        if filename.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        
        # Excel
        elif filename.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(uploaded_file)
        
        # JSON
        elif filename.endswith('.json'):
            df = pd.read_json(uploaded_file)
        
        else:
            st.error(f"❌ Format de fichier non supporté : {filename}")
            return None, None
        
        # Détection automatique des dates
        df = detect_date_formats(df)
        
        return df, filename
        
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement du fichier : {str(e)}")
        return None, None