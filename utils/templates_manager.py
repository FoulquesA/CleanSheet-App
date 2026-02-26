"""
Module de gestion des templates de nettoyage.
Permet de sauvegarder, charger et supprimer des templates.
"""

import json
import os
from datetime import datetime


def save_template(name, transformations):
    """
    Sauvegarde un template de nettoyage.
    
    Args:
        name: Nom du template
        transformations: Liste des transformations à sauvegarder
        
    Returns:
        Chemin du fichier sauvegardé
    """
    # Créer le dossier templates s'il n'existe pas
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    # Préparer les données du template
    template_data = {
        'name': name,
        'created_at': datetime.now().isoformat(),
        'transformations': transformations
    }
    
    # Nom de fichier sécurisé (sans caractères spéciaux)
    safe_filename = "".join(c for c in name if c.isalnum() or c in (' ', '-', '_')).strip()
    safe_filename = safe_filename.replace(' ', '_')
    filepath = f"templates/{safe_filename}.json"
    
    # Sauvegarder en JSON
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(template_data, f, indent=2, ensure_ascii=False, default=str)
    
    return filepath


def load_templates():
    """
    Charge la liste de tous les templates disponibles.
    
    Returns:
        Liste de dictionnaires avec les infos des templates
    """
    if not os.path.exists('templates'):
        return []
    
    templates = []
    
    for filename in os.listdir('templates'):
        if filename.endswith('.json'):
            filepath = os.path.join('templates', filename)
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    template_data = json.load(f)
                    templates.append({
                        'filename': filename,
                        'filepath': filepath,
                        'name': template_data.get('name', 'Sans nom'),
                        'created_at': template_data.get('created_at', 'Inconnu'),
                        'count': len(template_data.get('transformations', []))
                    })
            except:
                continue
    
    return templates


def load_template_data(filepath):
    """
    Charge les données complètes d'un template.
    
    Args:
        filepath: Chemin du fichier template
        
    Returns:
        Données du template (dict)
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def delete_template(filepath):
    """
    Supprime un template.
    
    Args:
        filepath: Chemin du fichier à supprimer
    """
    if os.path.exists(filepath):
        os.remove(filepath)