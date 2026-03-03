"""
Dictionnaire de traductions COMPLET pour l'interface multilingue.
Inclut les suggestions dynamiques et l'historique des transformations.
"""

TRANSLATIONS = {
    'fr': {
        # ========== INTERFACE PRINCIPALE ==========
        'app_title': '📑 CleanSheet - Outil de nettoyage de données',
        'app_subtitle': 'Uploadez votre fichier pour commencer l\'analyse et le nettoyage.',
        
        # ========== AIDE ==========
        'help_title': 'ℹ️ Aide & Conseils d\'utilisation',
        'help_content': """**Comment utiliser l'application :**
    
1. **Upload** : Chargez votre fichier CSV, Excel ou JSON
2. **Profiling** : Analysez vos données pour détecter les problèmes
3. **Transformations** : Nettoyez étape par étape (NaN, doublons, types, etc.)
4. **Export** : Téléchargez vos données propres + le code Python

**Conseils :**
- ✅ Utilisez des fichiers < 200 MB pour de meilleures performances
- ✅ Vérifiez le profiling avant toute transformation
- ✅ Utilisez Undo si une transformation ne vous convient pas
- ✅ Sauvegardez vos workflows en templates pour les réutiliser

**En cas d'erreur :**
- 🔍 Lisez le message d'erreur complet
- 🔄 Utilisez le bouton "Tout recommencer" si nécessaire
- 💾 Sauvegardez vos templates avant des transformations risquées""",
        
        # ========== SIDEBAR ==========
        'sidebar_options': 'Options',
        'sidebar_history': 'Historique des transformations',
        'sidebar_undo': '↩️ Annuler dernière transformation',
        'sidebar_reset': '🔄 Tout recommencer',
        'sidebar_undo_success': '✅ Transformation annulée',
        'sidebar_reset_success': '✅ Données réinitialisées',
        
        # ========== UPLOAD ==========
        'upload_label': 'Choisissez un fichier CSV ou Excel',
        'upload_help': 'Formats supportés : CSV, Excel (.xlsx, .xls), JSON',
        'upload_info': '👆 Uploadez un fichier CSV ou Excel pour commencer',
        'upload_success': '✅ Fichier chargé : {}',
        
        # ========== COMPARAISON ==========
        'comparison_title': '**📊 Impact des transformations :**',
        'comparison_rows': 'Lignes',
        'comparison_missing': 'Valeurs manquantes',
        'comparison_transformations': 'Transformations',
        
        # ========== TABS PRINCIPAUX ==========
        'tab_profiling': '📊 Profiling & Analyse',
        'tab_transformations': '🔧 Transformations',
        'tab_export': '💾 Export',
        'tab_templates': '📋 Templates',
        
        # ========== PROFILING - APERÇU ==========
        'profiling_overview': '📊 Aperçu des données',
        'profiling_rows': 'Nombre de lignes',
        'profiling_cols': 'Nombre de colonnes',
        'profiling_memory': 'Taille mémoire',
        
        # ========== PROFILING - QUICK ==========
        'profiling_quick': '🔍 Profiling rapide',
        'profiling_missing_warning': '⚠️ Total de valeurs manquantes : {}',
        'profiling_missing_success': '✅ Aucune valeur manquante détectée',
        'profiling_cols_label': 'Colonne',
        'profiling_types_label': 'Type',
        'profiling_unique_label': 'Valeurs uniques',
        'profiling_missing_label': 'Valeurs manquantes',
        'profiling_percentage_label': 'Pourcentage',
        
        # ========== PROFILING - TYPES ==========
        'profiling_types': '📝 Types de données',
        
        # ========== PROFILING - DATES ==========
        'profiling_dates': '📅 Analyse des dates',
        'profiling_date_correct': 'Colonne **{}** : format datetime correct',
        'profiling_date_multiple': 'Colonne **{}** : {} formats de dates différents détectés',
        'profiling_date_format': 'Format',
        'profiling_date_values': 'valeur(s)',
        'profiling_date_no_issues': 'Aucun problème de format de date détecté',
        
        # ========== PROFILING - ANOMALIES ==========
        'profiling_anomalies': '⚠️ Détection d\'anomalies',
        'profiling_anomaly_numeric': 'Colonne **{}** : {:.1f}% des valeurs sont numériques, mais certaines ne le sont pas',
        'profiling_anomaly_examples': 'Exemples de valeurs non-numériques :',
        'profiling_duplicates_warning': '🔄 **{} lignes dupliquées** détectées ({:.2f}%)',
        'profiling_duplicates_show': 'Afficher les lignes dupliquées',
        'profiling_anomalies_success': '✅ Aucune anomalie majeure détectée',
        
        # ========== PROFILING - HEATMAP ==========
        'profiling_heatmap': '🔥 Heatmap des valeurs manquantes',
        'profiling_heatmap_caption': 'Les barres blanches indiquent les valeurs manquantes. Cherchez des patterns.',
        
        # ========== PROFILING - DISTRIBUTION ==========
        'profiling_distribution': '📊 Distribution des données numériques',
        'profiling_select_column': 'Choisissez une colonne à visualiser',
        'profiling_distribution_of': 'Distribution de',
        'profiling_boxplot_of': 'Boxplot de',
        'profiling_no_numeric': 'Aucune colonne numérique à visualiser',
        
        # ========== TRANSFORMATIONS - TITRE ==========
        'trans_title': '🔧 Transformations de données',
        
        # ========== TRANSFORMATIONS - TAB NAMES ==========
        'trans_tab_missing': 'Valeurs manquantes',
        'trans_tab_types': 'Conversion de types',
        'trans_tab_duplicates': 'Doublons',
        'trans_tab_filter': 'Filtrage',
        'trans_tab_format': 'Formatage',
        'trans_tab_text': 'Manipulation texte',
        
        # ========== TAB 1 : VALEURS MANQUANTES ==========
        'trans_missing_title': '**Remplacer les valeurs manquantes**',
        'trans_missing_select': 'Choisir une colonne',
        'trans_missing_info': 'Colonne **{}** : {} valeurs manquantes ({:.1f}%)',
        'trans_missing_strategy': 'Stratégie de remplacement',
        'trans_missing_median': 'Médiane',
        'trans_missing_mean': 'Moyenne',
        'trans_missing_fixed': 'Valeur fixe',
        'trans_missing_drop': 'Supprimer les lignes',
        'trans_missing_mode': 'Mode (valeur la plus fréquente)',
        'trans_missing_value': 'Valeur de remplacement',
        'trans_missing_apply': 'Appliquer',
        'trans_missing_none_warning': 'Aucune valeur manquante à traiter dans cette colonne',
        'trans_missing_median_error': 'Impossible de calculer la médiane (toutes les valeurs sont manquantes)',
        'trans_missing_mean_error': 'Impossible de calculer la moyenne (toutes les valeurs sont manquantes)',
        'trans_missing_mode_error': 'Impossible de calculer le mode (colonne vide)',
        'trans_missing_median_success': 'Valeurs manquantes remplacées par la médiane ({:.2f})',
        'trans_missing_mean_success': 'Valeurs manquantes remplacées par la moyenne ({:.2f})',
        'trans_missing_fixed_success': 'Valeurs manquantes remplacées par {}',
        'trans_missing_drop_success': '{} ligne(s) supprimée(s)',
        'trans_missing_drop_warning': 'Aucune ligne à supprimer',
        'trans_missing_mode_success': 'Valeurs manquantes remplacées par le mode (\'{}\')' ,
        'trans_missing_fixed_error': 'Veuillez saisir une valeur de remplacement',
        'trans_missing_error': 'Erreur lors du remplacement : {}',
        'trans_missing_none': '✅ Aucune valeur manquante à traiter',
        
        # ========== DESCRIPTIONS HISTORIQUE - VALEURS MANQUANTES ==========
        'history_fill_na_median': 'NaN remplacés dans \'{}\' par Médiane',
        'history_fill_na_mean': 'NaN remplacés dans \'{}\' par Moyenne',
        'history_fill_na_fixed': 'NaN remplacés dans \'{}\' par Valeur fixe',
        'history_fill_na_drop': 'NaN remplacés dans \'{}\' par Supprimer les lignes',
        'history_fill_na_mode': 'NaN remplacés dans \'{}\' par Mode',
        
        # ========== TAB 2 : CONVERSION DE TYPES ==========
        'trans_convert_title': '**Convertir le type d\'une colonne**',
        'trans_convert_select': 'Choisir une colonne',
        'trans_convert_current': 'Type actuel : **{}**',
        'trans_convert_target': 'Convertir en',
        'trans_convert_float': 'Numérique (float)',
        'trans_convert_int': 'Numérique (int)',
        'trans_convert_string': 'Texte (string)',
        'trans_convert_datetime': 'Date/Heure',
        'trans_convert_apply': 'Appliquer conversion',
        'trans_convert_float_success': 'Colonne \'{}\' convertie en float',
        'trans_convert_int_success': 'Colonne \'{}\' convertie en int',
        'trans_convert_string_success': 'Colonne \'{}\' convertie en string',
        'trans_convert_datetime_success': 'Colonne \'{}\' convertie en datetime',
        'trans_convert_error': 'Erreur lors de la conversion : {}',
        
        # ========== DESCRIPTIONS HISTORIQUE - CONVERSION ==========
        'history_convert': 'Conversion \'{}\' en {}',
        
        # ========== TAB 3 : DOUBLONS ==========
        'trans_dup_title': '**Supprimer les lignes dupliquées**',
        'trans_dup_warning': '⚠️ {} ligne(s) dupliquée(s) détectée(s)',
        'trans_dup_strategy': 'Quelle occurrence garder ?',
        'trans_dup_first': 'Première',
        'trans_dup_last': 'Dernière',
        'trans_dup_none': 'Aucune (supprimer toutes)',
        'trans_dup_apply': 'Supprimer les doublons',
        'trans_dup_success': '{} doublon(s) supprimé(s)',
        'trans_dup_no_duplicates': '✅ Aucun doublon détecté',
        
        # ========== DESCRIPTIONS HISTORIQUE - DOUBLONS ==========
        'history_dup_first': 'Doublons supprimés (stratégie: Première)',
        'history_dup_last': 'Doublons supprimés (stratégie: Dernière)',
        'history_dup_none': 'Doublons supprimés (stratégie: Aucune)',
        
        # ========== TAB 4 : FILTRAGE ==========
        'trans_filter_title': '**Filtrer les lignes selon des critères**',
        'trans_filter_info': 'Les filtres s\'appliquent avec un opérateur ET (toutes les conditions doivent être vraies)',
        'trans_filter_add_title': '➕ Ajouter un filtre',
        'trans_filter_column': 'Colonne à filtrer',
        'trans_filter_type': 'Type détecté',
        'trans_filter_type_numeric': 'Numérique',
        'trans_filter_type_date': 'Date',
        'trans_filter_type_text': 'Texte',
        'trans_filter_operator': 'Opérateur',
        'trans_filter_op_equal': 'Égal à',
        'trans_filter_op_not_equal': 'Différent de',
        'trans_filter_op_greater': 'Supérieur à',
        'trans_filter_op_less': 'Inférieur à',
        'trans_filter_op_between': 'Entre',
        'trans_filter_op_not_between': 'N\'est pas entre',
        'trans_filter_op_before': 'Avant le',
        'trans_filter_op_after': 'Après le',
        'trans_filter_op_contains': 'Contient',
        'trans_filter_op_not_contains': 'Ne contient pas',
        'trans_filter_op_starts': 'Commence par',
        'trans_filter_op_ends': 'Finit par',
        'trans_filter_value_min': 'Valeur min',
        'trans_filter_value_max': 'Valeur max',
        'trans_filter_value': 'Valeur',
        'trans_filter_date_min': 'Date min',
        'trans_filter_date_max': 'Date max',
        'trans_filter_date': 'Date',
        'trans_filter_add_btn': '➕ Ajouter ce filtre',
        'trans_filter_add_success': 'Filtre ajouté : {} {} {}',
        'trans_filter_add_error': 'Veuillez saisir une valeur',
        'trans_filter_active_title': '🔍 Filtres actifs',
        'trans_filter_delete': 'X',
        'trans_filter_reset': '🔄 Réinitialiser tous les filtres',
        'trans_filter_apply': '✅ Appliquer les filtres',
        'trans_filter_no_results': 'Aucune ligne ne correspond aux filtres ! Tous les filtres ont été annulés.',
        'trans_filter_success': 'Filtres appliqués : {} lignes conservées, {} lignes supprimées',
        'trans_filter_none': 'Aucun filtre actif. Ajoutez un filtre ci-dessus.',
        
        # ========== DESCRIPTIONS HISTORIQUE - FILTRAGE ==========
        'history_filter': 'Filtrage appliqué : {}',
        
        # ========== TAB 5 : FORMATAGE ==========
        'trans_format_title': '**Formater l\'affichage des colonnes numériques**',
        'trans_format_choose': 'Choisissez le nombre de décimales pour chaque colonne :',
        'trans_format_column': 'Colonne à formater',
        'trans_format_decimals': 'Nombre de décimales',
        'trans_format_apply': 'Appliquer le formatage',
        'trans_format_success': 'Colonne \'{}\' formatée avec {} décimale(s)',
        'trans_format_current_title': '**Formatages appliqués :**',
        'trans_format_col_label': 'Colonne',
        'trans_format_dec_label': 'Décimales',
        'trans_format_reset': '🔄 Réinitialiser tous les formatages',
        'trans_format_reset_success': 'Formatages réinitialisés',
        'trans_format_none': 'Aucune colonne numérique à formater',
        
        # ========== TAB 6 : MANIPULATION TEXTE ==========
        'trans_text_title': '**Nettoyer, extraire et séparer les données textuelles**',
        'trans_text_tab_clean': 'Nettoyage',
        'trans_text_tab_extract': 'Extraction',
        'trans_text_tab_split': 'Split colonnes',
        'trans_text_tab_replace': 'Find & Replace',
        
        # TAB 6.1 : NETTOYAGE
        'trans_text_clean_title': '**Nettoyer et transformer les colonnes textuelles**',
        'trans_text_clean_select': 'Choisir une colonne texte à nettoyer',
        'trans_text_clean_preview': '**Aperçu de \'{}\' (5 premières valeurs) :**',
        'trans_text_clean_type': 'Type de nettoyage',
        'trans_text_clean_trim': 'Supprimer espaces début/fin (trim)',
        'trans_text_clean_lower': 'Convertir en minuscules',
        'trans_text_clean_upper': 'Convertir en majuscules',
        'trans_text_clean_title_case': 'Convertir en title case (Première Lettre Majuscule)',
        'trans_text_clean_replace': 'Remplacer une valeur',
        'trans_text_clean_special': 'Supprimer caractères spéciaux',
        'trans_text_clean_from': 'Valeur à remplacer',
        'trans_text_clean_to': 'Remplacer par',
        'trans_text_clean_apply': 'Appliquer le nettoyage',
        'trans_text_clean_trim_success': 'Espaces supprimés dans \'{}\'',
        'trans_text_clean_lower_success': '\'{}\' converti en minuscules',
        'trans_text_clean_upper_success': '\'{}\' converti en majuscules',
        'trans_text_clean_title_success': '\'{}\' converti en title case',
        'trans_text_clean_replace_success': '\'{}\' remplacé par \'{}\' dans \'{}\'',
        'trans_text_clean_special_success': 'Caractères spéciaux supprimés dans \'{}\'',
        'trans_text_clean_error': 'Veuillez renseigner les deux valeurs',
        'trans_text_no_columns': 'Aucune colonne textuelle détectée',
        
        # ========== DESCRIPTIONS HISTORIQUE - TEXTE ==========
        'history_text_trim': 'Espaces supprimés dans \'{}\'',
        'history_text_lower': '\'{}\' converti en minuscules',
        'history_text_upper': '\'{}\' converti en majuscules',
        'history_text_title': '\'{}\' converti en title case',
        'history_text_replace': '\'{}\' remplacé par \'{}\' dans \'{}\'',
        'history_text_special': 'Caractères spéciaux supprimés dans \'{}\'',
        
        # ========== SUGGESTIONS DE NETTOYAGE ==========
        'trans_suggestions': '💡 Suggestions de nettoyage',
        'trans_suggestions_count': '{} action(s) recommandée(s) :',
        'trans_priority': 'Priorité',
        'trans_problem': 'Problème détecté',
        'trans_action': 'Action recommandée',
        'trans_reason': 'Pourquoi ?',
        'trans_suggestions_next': '💡 **Prochaine étape** : Ces suggestions seront bientôt automatisables en un clic !',
        'trans_suggestions_clean': '✅ Aucune action de nettoyage nécessaire - vos données sont propres !',
        
        # ========== CONTENU DES SUGGESTIONS (DYNAMIQUE) ==========
        'sugg_high_missing_problem': '{} colonne(s) avec >50% de valeurs manquantes',
        'sugg_high_missing_action': 'Supprimer colonnes : {}',
        'sugg_high_missing_reason': 'Colonnes avec trop peu de données exploitables',
        
        'sugg_medium_missing_problem': 'Colonne \'{}\' : {} NaN',
        'sugg_medium_missing_action_median': 'Remplacer par médiane ({:.2f})',
        'sugg_medium_missing_reason_median': 'Colonne numérique - médiane robuste aux outliers',
        'sugg_medium_missing_action_mode': 'Remplacer par valeur fixe ou mode',
        'sugg_medium_missing_reason_mode': 'Colonne catégorielle',
        
        'sugg_duplicates_problem': '{} lignes dupliquées',
        'sugg_duplicates_action': 'Supprimer les doublons (garder première occurrence)',
        'sugg_duplicates_reason': 'Les doublons faussent les analyses statistiques',
        
        'sugg_convert_problem': 'Colonne \'{}\' devrait être numérique ({:.0f}% convertible)',
        'sugg_convert_action': 'Convertir en numérique (gérer les erreurs)',
        'sugg_convert_reason': 'Permettra des calculs et agrégations',
        
        # ========== EXPORT ==========
        'export_title': '💾 Export des données nettoyées',
        'export_download': '**Téléchargez vos données nettoyées dans le format de votre choix :**',
        'export_csv': '📥 Télécharger CSV',
        'export_excel': '📥 Télécharger Excel',
        'export_json': '📥 Télécharger JSON',
        'export_info': '📊 Le fichier contient **{} lignes** et **{} colonnes**',
        'export_code_title': 'Code Python reproductible',
        'export_code_copy': '**Copiez ce code pour reproduire vos transformations :**',
        'export_code_download': '📋 Télécharger le script Python',
        'export_code_none': 'ℹ️ Aucune transformation appliquée. Le code sera généré après vos modifications.',
        'export_stats_label': '**Statistiques descriptives :**',
        
        # ========== TEMPLATES ==========
        'templates_title': '📋 Templates de nettoyage',
        'templates_info': '💡 Les templates permettent de sauvegarder et réutiliser vos séquences de transformations',
        'templates_save': '**💾 Sauvegarder l\'historique actuel**',
        'templates_load': '**📂 Charger un template existant**',
        'templates_none': 'ℹ️ Aucun template sauvegardé pour le moment',
        'templates_success_count': '{} transformation(s) dans l\'historique',
        'templates_name': 'Nom du template',
        'templates_name_placeholder': 'Ex: Nettoyage clients e-commerce',
        'templates_save_btn': '💾 Sauvegarder comme template',
        'templates_save_success': 'Template \'{}\' sauvegardé !',
        'templates_save_file': 'Fichier : {}',
        'templates_save_error': 'Erreur lors de la sauvegarde : {}',
        'templates_name_error': 'Veuillez donner un nom au template',
        'templates_no_trans': 'Aucune transformation dans l\'historique. Effectuez des transformations d\'abord.',
        'templates_available': '{} template(s) disponible(s)',
        'templates_select': 'Choisir un template',
        'templates_info_title': '**Informations :**',
        'templates_created': 'Créé le : {}',
        'templates_trans_count': 'Transformations : {}',
        'templates_apply': '📥 Appliquer ce template',
        'templates_delete': '🗑️ Supprimer',
        'templates_no_trans_warning': 'Ce template ne contient aucune transformation',
        'templates_all_deleted': 'Le template a supprimé toutes les lignes ! Application annulée.',
        'templates_incompatible': 'Ce template n\'est peut-être pas compatible avec vos données',
        'templates_warning_count': 'Template appliqué avec {} avertissement(s)',
        'templates_success_apply': 'Template \'{}\' appliqué : {}/{} transformation(s) réussie(s)',
        'templates_error': 'Erreur lors de l\'application du template : {}',
        'templates_check_compat': 'Vérifiez que le template est compatible avec vos données (mêmes colonnes, mêmes types)',
        'templates_delete_success': 'Template \'{}\' supprimé',
        'templates_delete_error': 'Erreur : {}',
    },
    
    'en': {
        # ========== MAIN INTERFACE ==========
        'app_title': '📑 CleanSheet - Data Cleaning Tool',
        'app_subtitle': 'Upload your file to start analysis and cleaning.',
        
        # ========== HELP ==========
        'help_title': 'ℹ️ Help & Usage Tips',
        'help_content': """**How to use the application:**

1. **Upload**: Load your CSV, Excel or JSON file
2. **Profiling**: Analyze your data to detect issues
3. **Transformations**: Clean step by step (NaN, duplicates, types, etc.)
4. **Export**: Download your clean data + Python code

**Tips:**
- ✅ Use files < 200 MB for better performance
- ✅ Check profiling before any transformation
- ✅ Use Undo if a transformation doesn't suit you
- ✅ Save your workflows as templates to reuse them

**In case of error:**
- 🔍 Read the complete error message
- 🔄 Use the "Start Over" button if necessary
- 💾 Save your templates before risky transformations""",
        
        # ========== SIDEBAR ==========
        'sidebar_options': 'Options',
        'sidebar_history': 'Transformation History',
        'sidebar_undo': '↩️ Undo Last Transformation',
        'sidebar_reset': '🔄 Start Over',
        'sidebar_undo_success': '✅ Transformation undone',
        'sidebar_reset_success': '✅ Data reset',
        
        # ========== UPLOAD ==========
        'upload_label': 'Choose a CSV or Excel file',
        'upload_help': 'Supported formats: CSV, Excel (.xlsx, .xls), JSON',
        'upload_info': '👆 Upload a CSV or Excel file to start',
        'upload_success': '✅ File loaded: {}',
        
        # ========== COMPARISON ==========
        'comparison_title': '**📊 Transformation Impact:**',
        'comparison_rows': 'Rows',
        'comparison_missing': 'Missing Values',
        'comparison_transformations': 'Transformations',
        
        # ========== MAIN TABS ==========
        'tab_profiling': '📊 Profiling & Analysis',
        'tab_transformations': '🔧 Transformations',
        'tab_export': '💾 Export',
        'tab_templates': '📋 Templates',
        
        # ========== PROFILING - OVERVIEW ==========
        'profiling_overview': '📊 Data Overview',
        'profiling_rows': 'Number of rows',
        'profiling_cols': 'Number of columns',
        'profiling_memory': 'Memory size',
        
        # ========== PROFILING - QUICK ==========
        'profiling_quick': '🔍 Quick Profiling',
        'profiling_missing_warning': '⚠️ Total missing values: {}',
        'profiling_missing_success': '✅ No missing values detected',
        'profiling_cols_label': 'Column',
        'profiling_types_label': 'Type',
        'profiling_unique_label': 'Unique values',
        'profiling_missing_label': 'Missing values',
        'profiling_percentage_label': 'Percentage',
        
        # ========== PROFILING - TYPES ==========
        'profiling_types': '📝 Data Types',
        
        # ========== PROFILING - DATES ==========
        'profiling_dates': '📅 Date Analysis',
        'profiling_date_correct': 'Column **{}**: correct datetime format',
        'profiling_date_multiple': 'Column **{}**: {} different date formats detected',
        'profiling_date_format': 'Format',
        'profiling_date_values': 'value(s)',
        'profiling_date_no_issues': 'No date format issues detected',
        
        # ========== PROFILING - ANOMALIES ==========
        'profiling_anomalies': '⚠️ Anomaly Detection',
        'profiling_anomaly_numeric': 'Column **{}**: {:.1f}% of values are numeric, but some are not',
        'profiling_anomaly_examples': 'Examples of non-numeric values:',
        'profiling_duplicates_warning': '🔄 **{} duplicate rows** detected ({:.2f}%)',
        'profiling_duplicates_show': 'Show duplicate rows',
        'profiling_anomalies_success': '✅ No major anomalies detected',
        
        # ========== PROFILING - HEATMAP ==========
        'profiling_heatmap': '🔥 Missing Values Heatmap',
        'profiling_heatmap_caption': 'White bars indicate missing values. Look for patterns.',
        
        # ========== PROFILING - DISTRIBUTION ==========
        'profiling_distribution': '📊 Numeric Data Distribution',
        'profiling_select_column': 'Choose a column to visualize',
        'profiling_distribution_of': 'Distribution of',
        'profiling_boxplot_of': 'Boxplot of',
        'profiling_no_numeric': 'No numeric columns to visualize',
        
        # ========== TRANSFORMATIONS - TITLE ==========
        'trans_title': '🔧 Data Transformations',
        
        # ========== TRANSFORMATIONS - TAB NAMES ==========
        'trans_tab_missing': 'Missing values',
        'trans_tab_types': 'Type conversion',
        'trans_tab_duplicates': 'Duplicates',
        'trans_tab_filter': 'Filtering',
        'trans_tab_format': 'Formatting',
        'trans_tab_text': 'Text manipulation',
        
        # ========== TAB 1 : MISSING VALUES ==========
        'trans_missing_title': '**Replace missing values**',
        'trans_missing_select': 'Choose a column',
        'trans_missing_info': 'Column **{}**: {} missing values ({:.1f}%)',
        'trans_missing_strategy': 'Replacement strategy',
        'trans_missing_median': 'Median',
        'trans_missing_mean': 'Mean',
        'trans_missing_fixed': 'Fixed value',
        'trans_missing_drop': 'Delete rows',
        'trans_missing_mode': 'Mode (most frequent value)',
        'trans_missing_value': 'Replacement value',
        'trans_missing_apply': 'Apply',
        'trans_missing_none_warning': 'No missing values to process in this column',
        'trans_missing_median_error': 'Cannot calculate median (all values are missing)',
        'trans_missing_mean_error': 'Cannot calculate mean (all values are missing)',
        'trans_missing_mode_error': 'Cannot calculate mode (empty column)',
        'trans_missing_median_success': 'Missing values replaced by median ({:.2f})',
        'trans_missing_mean_success': 'Missing values replaced by mean ({:.2f})',
        'trans_missing_fixed_success': 'Missing values replaced by {}',
        'trans_missing_drop_success': '{} row(s) deleted',
        'trans_missing_drop_warning': 'No rows to delete',
        'trans_missing_mode_success': 'Missing values replaced by mode (\'{}\')' ,
        'trans_missing_fixed_error': 'Please enter a replacement value',
        'trans_missing_error': 'Error during replacement: {}',
        'trans_missing_none': '✅ No missing values to process',
        
        # ========== HISTORY DESCRIPTIONS - MISSING VALUES ==========
        'history_fill_na_median': 'NaN replaced in \'{}\' by Median',
        'history_fill_na_mean': 'NaN replaced in \'{}\' by Mean',
        'history_fill_na_fixed': 'NaN replaced in \'{}\' by Fixed value',
        'history_fill_na_drop': 'NaN replaced in \'{}\' by Delete rows',
        'history_fill_na_mode': 'NaN replaced in \'{}\' by Mode',
        
        # ========== TAB 2 : TYPE CONVERSION ==========
        'trans_convert_title': '**Convert column type**',
        'trans_convert_select': 'Choose a column',
        'trans_convert_current': 'Current type: **{}**',
        'trans_convert_target': 'Convert to',
        'trans_convert_float': 'Numeric (float)',
        'trans_convert_int': 'Numeric (int)',
        'trans_convert_string': 'Text (string)',
        'trans_convert_datetime': 'Date/Time',
        'trans_convert_apply': 'Apply conversion',
        'trans_convert_float_success': 'Column \'{}\' converted to float',
        'trans_convert_int_success': 'Column \'{}\' converted to int',
        'trans_convert_string_success': 'Column \'{}\' converted to string',
        'trans_convert_datetime_success': 'Column \'{}\' converted to datetime',
        'trans_convert_error': 'Error during conversion: {}',
        
        # ========== HISTORY DESCRIPTIONS - CONVERSION ==========
        'history_convert': 'Conversion \'{}\' to {}',
        
        # ========== TAB 3 : DUPLICATES ==========
        'trans_dup_title': '**Remove duplicate rows**',
        'trans_dup_warning': '⚠️ {} duplicate row(s) detected',
        'trans_dup_strategy': 'Which occurrence to keep?',
        'trans_dup_first': 'First',
        'trans_dup_last': 'Last',
        'trans_dup_none': 'None (delete all)',
        'trans_dup_apply': 'Remove duplicates',
        'trans_dup_success': '{} duplicate(s) removed',
        'trans_dup_no_duplicates': '✅ No duplicates detected',
        
        # ========== HISTORY DESCRIPTIONS - DUPLICATES ==========
        'history_dup_first': 'Duplicates removed (strategy: First)',
        'history_dup_last': 'Duplicates removed (strategy: Last)',
        'history_dup_none': 'Duplicates removed (strategy: None)',
        
        # ========== TAB 4 : FILTERING ==========
        'trans_filter_title': '**Filter rows by criteria**',
        'trans_filter_info': 'Filters are applied with AND operator (all conditions must be true)',
        'trans_filter_add_title': '➕ Add a filter',
        'trans_filter_column': 'Column to filter',
        'trans_filter_type': 'Type detected',
        'trans_filter_type_numeric': 'Numeric',
        'trans_filter_type_date': 'Date',
        'trans_filter_type_text': 'Text',
        'trans_filter_operator': 'Operator',
        'trans_filter_op_equal': 'Equal to',
        'trans_filter_op_not_equal': 'Different from',
        'trans_filter_op_greater': 'Greater than',
        'trans_filter_op_less': 'Less than',
        'trans_filter_op_between': 'Between',
        'trans_filter_op_not_between': 'Not between',
        'trans_filter_op_before': 'Before',
        'trans_filter_op_after': 'After',
        'trans_filter_op_contains': 'Contains',
        'trans_filter_op_not_contains': 'Does not contain',
        'trans_filter_op_starts': 'Starts with',
        'trans_filter_op_ends': 'Ends with',
        'trans_filter_value_min': 'Min value',
        'trans_filter_value_max': 'Max value',
        'trans_filter_value': 'Value',
        'trans_filter_date_min': 'Min date',
        'trans_filter_date_max': 'Max date',
        'trans_filter_date': 'Date',
        'trans_filter_add_btn': '➕ Add this filter',
        'trans_filter_add_success': 'Filter added: {} {} {}',
        'trans_filter_add_error': 'Please enter a value',
        'trans_filter_active_title': '🔍 Active filters',
        'trans_filter_delete': 'X',
        'trans_filter_reset': '🔄 Reset all filters',
        'trans_filter_apply': '✅ Apply filters',
        'trans_filter_no_results': 'No rows match the filters! All filters have been cancelled.',
        'trans_filter_success': 'Filters applied: {} rows kept, {} rows removed',
        'trans_filter_none': 'No active filters. Add a filter above.',
        
        # ========== HISTORY DESCRIPTIONS - FILTERING ==========
        'history_filter': 'Filtering applied: {}',
        
        # ========== TAB 5 : FORMATTING ==========
        'trans_format_title': '**Format numeric column display**',
        'trans_format_choose': 'Choose the number of decimal places for each column:',
        'trans_format_column': 'Column to format',
        'trans_format_decimals': 'Number of decimal places',
        'trans_format_apply': 'Apply formatting',
        'trans_format_success': 'Column \'{}\' formatted with {} decimal place(s)',
        'trans_format_current_title': '**Applied formats:**',
        'trans_format_col_label': 'Column',
        'trans_format_dec_label': 'Decimals',
        'trans_format_reset': '🔄 Reset all formats',
        'trans_format_reset_success': 'Formats reset',
        'trans_format_none': 'No numeric columns to format',
        
        # ========== TAB 6 : TEXT MANIPULATION ==========
        'trans_text_title': '**Clean, extract and split text data**',
        'trans_text_tab_clean': 'Cleaning',
        'trans_text_tab_extract': 'Extraction',
        'trans_text_tab_split': 'Split columns',
        'trans_text_tab_replace': 'Find & Replace',
        
        # TAB 6.1 : CLEANING
        'trans_text_clean_title': '**Clean and transform text columns**',
        'trans_text_clean_select': 'Choose a text column to clean',
        'trans_text_clean_preview': '**Preview of \'{}\' (first 5 values):**',
        'trans_text_clean_type': 'Cleaning type',
        'trans_text_clean_trim': 'Remove leading/trailing spaces (trim)',
        'trans_text_clean_lower': 'Convert to lowercase',
        'trans_text_clean_upper': 'Convert to uppercase',
        'trans_text_clean_title_case': 'Convert to title case (First Letter Uppercase)',
        'trans_text_clean_replace': 'Replace a value',
        'trans_text_clean_special': 'Remove special characters',
        'trans_text_clean_from': 'Value to replace',
        'trans_text_clean_to': 'Replace with',
        'trans_text_clean_apply': 'Apply cleaning',
        'trans_text_clean_trim_success': 'Spaces removed in \'{}\'',
        'trans_text_clean_lower_success': '\'{}\' converted to lowercase',
        'trans_text_clean_upper_success': '\'{}\' converted to uppercase',
        'trans_text_clean_title_success': '\'{}\' converted to title case',
        'trans_text_clean_replace_success': '\'{}\' replaced by \'{}\' in \'{}\'',
        'trans_text_clean_special_success': 'Special characters removed in \'{}\'',
        'trans_text_clean_error': 'Please enter both values',
        'trans_text_no_columns': 'No text columns detected',
        
        # ========== HISTORY DESCRIPTIONS - TEXT ==========
        'history_text_trim': 'Spaces removed in \'{}\'',
        'history_text_lower': '\'{}\' converted to lowercase',
        'history_text_upper': '\'{}\' converted to uppercase',
        'history_text_title': '\'{}\' converted to title case',
        'history_text_replace': '\'{}\' replaced by \'{}\' in \'{}\'',
        'history_text_special': 'Special characters removed in \'{}\'',
        
        # ========== CLEANING SUGGESTIONS ==========
        'trans_suggestions': '💡 Cleaning Suggestions',
        'trans_suggestions_count': '{} recommended action(s):',
        'trans_priority': 'Priority',
        'trans_problem': 'Detected problem',
        'trans_action': 'Recommended action',
        'trans_reason': 'Why?',
        'trans_suggestions_next': '💡 **Next step**: These suggestions will soon be automatable with one click!',
        'trans_suggestions_clean': '✅ No cleaning action needed - your data is clean!',
        
        # ========== SUGGESTIONS CONTENT (DYNAMIC) ==========
        'sugg_high_missing_problem': '{} column(s) with >50% missing values',
        'sugg_high_missing_action': 'Drop columns: {}',
        'sugg_high_missing_reason': 'Columns with too little usable data',
        
        'sugg_medium_missing_problem': 'Column \'{}\': {} NaN',
        'sugg_medium_missing_action_median': 'Replace by median ({:.2f})',
        'sugg_medium_missing_reason_median': 'Numeric column - median robust to outliers',
        'sugg_medium_missing_action_mode': 'Replace by fixed value or mode',
        'sugg_medium_missing_reason_mode': 'Categorical column',
        
        'sugg_duplicates_problem': '{} duplicate rows',
        'sugg_duplicates_action': 'Remove duplicates (keep first occurrence)',
        'sugg_duplicates_reason': 'Duplicates distort statistical analyses',
        
        'sugg_convert_problem': 'Column \'{}\' should be numeric ({:.0f}% convertible)',
        'sugg_convert_action': 'Convert to numeric (handle errors)',
        'sugg_convert_reason': 'Will allow calculations and aggregations',
        
        # ========== EXPORT ==========
        'export_title': '💾 Export Clean Data',
        'export_download': '**Download your clean data in your preferred format:**',
        'export_csv': '📥 Download CSV',
        'export_excel': '📥 Download Excel',
        'export_json': '📥 Download JSON',
        'export_info': '📊 File contains **{} rows** and **{} columns**',
        'export_code_title': 'Reproducible Python Code',
        'export_code_copy': '**Copy this code to reproduce your transformations:**',
        'export_code_download': '📋 Download Python Script',
        'export_code_none': 'ℹ️ No transformations applied. Code will be generated after your modifications.',
        'export_stats_label': '**Descriptive statistics:**',
        
        # ========== TEMPLATES ==========
        'templates_title': '📋 Cleaning Templates',
        'templates_info': '💡 Templates allow you to save and reuse your transformation sequences',
        'templates_save': '**💾 Save Current History**',
        'templates_load': '**📂 Load Existing Template**',
        'templates_none': 'ℹ️ No saved templates yet',
        'templates_success_count': '{} transformation(s) in history',
        'templates_name': 'Template name',
        'templates_name_placeholder': 'Ex: E-commerce customer cleaning',
        'templates_save_btn': '💾 Save as template',
        'templates_save_success': 'Template \'{}\' saved!',
        'templates_save_file': 'File: {}',
        'templates_save_error': 'Error during save: {}',
        'templates_name_error': 'Please give the template a name',
        'templates_no_trans': 'No transformations in history. Perform transformations first.',
        'templates_available': '{} template(s) available',
        'templates_select': 'Choose a template',
        'templates_info_title': '**Information:**',
        'templates_created': 'Created on: {}',
        'templates_trans_count': 'Transformations: {}',
        'templates_apply': '📥 Apply this template',
        'templates_delete': '🗑️ Delete',
        'templates_no_trans_warning': 'This template contains no transformations',
        'templates_all_deleted': 'Template deleted all rows! Application cancelled.',
        'templates_incompatible': 'This template may not be compatible with your data',
        'templates_warning_count': 'Template applied with {} warning(s)',
        'templates_success_apply': 'Template \'{}\' applied: {}/{} transformation(s) successful',
        'templates_error': 'Error applying template: {}',
        'templates_check_compat': 'Check that the template is compatible with your data (same columns, same types)',
        'templates_delete_success': 'Template \'{}\' deleted',
        'templates_delete_error': 'Error: {}',
    }
}

def get_text(key, lang='fr'):
    """
    Récupère un texte traduit.
    
    Args:
        key: Clé du texte
        lang: Langue ('fr' ou 'en')
        
    Returns:
        Texte traduit ou clé si non trouvé
    """
    return TRANSLATIONS.get(lang, TRANSLATIONS['fr']).get(key, key)
