"""
================================================================================
    OBSERVATOIRE STRATÉGIQUE DE L'IMMOBILIER FRANÇAIS
    Application Streamlit Professionnelle - Version 2.1
================================================================================

Fonctionnalités :
- Graphiques principaux : 
  • France : G1 (variations %), G2 (prix vs loyers), G3 (dette / prêts / transactions), G6 (accessibilité)
  • Île-de-France : G4 (prix par département), G5 (Top 10 communes), distribution des prix
- Détection automatique des échelles de données (base 1 vs base 100)
- Filtres dynamiques par période et département
- Export des données en CSV
- Design executive professionnel
- Module de graphiques personnalisés

================================================================================
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
from datetime import datetime
import unicodedata
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords 
from nltk.stem.snowball import FrenchStemmer
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
try :
    nltk.download('punkt_tab', quiet=True) 
except :
    pass


# =============================================================================
# 1. CONFIGURATION DE LA PAGE
# =============================================================================
st.set_page_config(
    page_title="Observatoire Immobilier France",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# 2. DESIGN PROFESSIONNEL - PALETTE "EXECUTIVE DARK"
# =============================================================================
COLORS = {
    # Fond et structure
    "bg_primary": "#0f172a",
    "bg_secondary": "#1e293b",
    "bg_card": "#1e293b",
    "border": "#334155",
    
    # Textes
    "text_primary": "#FFFFFF",
    "text_secondary": "#94a3b8",
    "text_accent": "#38bdf8",
    
    # Accents
    "accent_blue": "#3b82f6",
    "accent_red": "#ef4444",
    "accent_green": "#22c55e",
    "accent_orange": "#f97316",
    "accent_purple": "#a855f7",
    "accent_cyan": "#06b6d4",
    "accent_yellow": "#eab308",
    
    # Séries graphiques
    "france": "#3b82f6",
    "paris": "#ef4444",
    "idf": "#22c55e",
    "loyers": "#f97316",
    "ipc": "#06b6d4",
    "icc": "#ec4899",
    "taux": "#62f5c8",
    "pib": "#84cc16",
    "dette": "#06b6d4",
    "revenu": "#22c55e"
}

# Couleurs par département Île-de-France
DEPT_COLORS = {
    "75": "#ef4444",  # Paris - Rouge
    "92": "#3b82f6",  # Hauts-de-Seine - Bleu
    "94": "#22c55e",  # Val-de-Marne - Vert
    "93": "#a855f7",  # Seine-Saint-Denis - Violet
    "78": "#f97316",  # Yvelines - Orange
    "91": "#eab308",  # Essonne - Jaune
    "95": "#06b6d4",  # Val-d'Oise - Cyan
    "77": "#ec4899"   # Seine-et-Marne - Rose
}

NOMS_DEPARTEMENTS = {
    "75": "Paris",
    "77": "Seine-et-Marne",
    "78": "Yvelines",
    "91": "Essonne",
    "92": "Hauts-de-Seine",
    "93": "Seine-Saint-Denis",
    "94": "Val-de-Marne",
    "95": "Val-d'Oise"
}

# CSS Professionnel
st.markdown(f"""
<style>
    /* ===== FOND GLOBAL ===== */
    .stApp {{
        background: linear-gradient(180deg, {COLORS['bg_primary']} 0%, #131c2e 100%);
    }}
    
    /* ===== SIDEBAR ===== */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {COLORS['bg_secondary']} 0%, {COLORS['bg_primary']} 100%);
        border-right: 1px solid {COLORS['border']};
    }}
    [data-testid="stSidebar"] * {{
        color: {COLORS['text_primary']} !important;
    }}
    
    /* ===== TYPOGRAPHIE ===== */
    h1, h2, h3, h4, h5, h6 {{
        color: {COLORS['text_primary']} !important;
        font-weight: 600;
    }}
    p, span, label, .stMarkdown {{
        color: {COLORS['text_primary']} !important;
    }}
    
    /* ===== WIDGETS ===== */
    .stSelectbox > div > div,
    .stMultiSelect > div > div {{
        background-color: {COLORS['bg_card']};
        border: 1px solid {COLORS['border']};
        color: white;
    }}
    .stSlider > div > div > div {{
        background-color: {COLORS['accent_blue']};
    }}
    
    /* ===== METRICS CARDS ===== */
    div[data-testid="stMetric"] {{
        background: linear-gradient(135deg, {COLORS['bg_card']} 0%, #263548 100%);
        border: 1px solid {COLORS['border']};
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }}
    div[data-testid="stMetricLabel"] {{
        color: {COLORS['text_secondary']} !important;
    }}
    div[data-testid="stMetricValue"] {{
        color: {COLORS['text_accent']} !important;
        font-size: 1.8rem;
        font-weight: 700;
    }}
    
    /* ===== TABS ===== */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
        background: transparent;
    }}
    .stTabs [data-baseweb="tab"] {{
        color: {COLORS['text_secondary']};
        background: {COLORS['bg_card']};
        border-radius: 8px 8px 0 0;
        padding: 12px 24px;
        border: 1px solid {COLORS['border']};
        border-bottom: none;
    }}
    .stTabs [aria-selected="true"] {{
        color: {COLORS['text_primary']} !important;
        background: {COLORS['accent_blue']};
        border-bottom: 3px solid {COLORS['accent_orange']};
    }}
    
    /* ===== EXPANDER ===== */
    .streamlit-expanderHeader {{
        background: {COLORS['bg_card']};
        border-radius: 8px;
        color: white !important;
    }}
    
    /* ===== INFO BOXES ===== */
    .stAlert {{
        background: {COLORS['bg_card']};
        border-left: 4px solid {COLORS['accent_blue']};
        color: white;
    }}
    
    /* ===== HEADER CUSTOM ===== */
    .header-banner {{
        background: linear-gradient(135deg, {COLORS['accent_blue']} 0%, #1e40af 100%);
        padding: 25px 35px;
        border-radius: 16px;
        margin-bottom: 25px;
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.3);
    }}
    .header-title {{
        color: white;
        font-size: 2.4rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }}
    .header-subtitle {{
        color: #cbd5e1;
        font-size: 1.1rem;
        margin-top: 8px;
    }}
    
    /* ===== SECTION TITLES ===== */
    .section-title {{
        color: {COLORS['text_accent']};
        font-size: 1.4rem;
        font-weight: 600;
        border-left: 4px solid {COLORS['accent_orange']};
        padding-left: 15px;
        margin: 20px 0;
    }}
    
    /* ===== DATAFRAME ===== */
    .stDataFrame {{
        border: 1px solid {COLORS['border']};
        border-radius: 8px;
    }}
</style>
""", unsafe_allow_html=True)

# =============================================================================
# 3. FONCTIONS UTILITAIRES
# =============================================================================

def normalize_str(s: str) -> str:
    """Normalise une chaîne (accents, minuscules, tirets→espaces) pour matcher les régions."""
    if pd.isna(s):
        return ""
    s = str(s)
    s_norm = ''.join(
        c for c in unicodedata.normalize("NFKD", s)
        if not unicodedata.combining(c)
    )
    return s_norm.lower().replace("-", " ").strip()


def detecter_echelle(values):
    """
    Détecte si les données sont en base 1 ou base 100.
    Retourne le multiplicateur à appliquer.
    """
    if values is None or len(values) == 0:
        return 1
    clean_values = [v for v in values if pd.notna(v) and v > 0]
    if not clean_values:
        return 1
    max_val = max(clean_values)
    # Si max < 10, on est en base 1 → multiplier par 100
    return 100 if max_val < 10 else 1


def format_euro(value, precision=0):
    """Formate un nombre en euros."""
    if pd.isna(value):
        return "N/A"
    if abs(value) >= 1e9:
        return f"{value/1e9:.1f} Md€"
    if abs(value) >= 1e6:
        return f"{value/1e6:.1f} M€"
    if abs(value) >= 1e3:
        return f"{value/1e3:.{precision}f} k€"
    return f"{value:.{precision}f} €"


def get_plotly_template():
    """Template Plotly personnalisé pour le thème dark."""
    return {
        'layout': {
            'paper_bgcolor': 'rgba(0,0,0,0)',
            'plot_bgcolor': 'rgba(0,0,0,0)',
            'font': {'color': COLORS['text_primary'], 'family': 'Arial'},
            'xaxis': {
                'gridcolor': COLORS['border'],
                'linecolor': COLORS['border'],
                'tickfont': {'color': COLORS['text_secondary']}
            },
            'yaxis': {
                'gridcolor': COLORS['border'],
                'linecolor': COLORS['border'],
                'tickfont': {'color': COLORS['text_secondary']}
            },
            'legend': {
                'bgcolor': 'rgba(30,41,59,0.9)',
                'bordercolor': COLORS['border'],
                'font': {'color': COLORS['text_primary']}
            }
        }
    }

# =============================================================================
# 4. CHARGEMENT DES DONNÉES
# =============================================================================

@st.cache_data
def load_data():
    """Charge et prépare les données depuis le fichier CSV (même dossier que ce script)."""

    # Chemin basé sur l'emplacement du script Streamlit
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "./OUTPUT/04_DF_Union_Macro_DVF.csv")

    # Si le fichier n'existe pas, on renvoie None pour que l'app affiche le message d'erreur prévu plus bas
    if not os.path.exists(file_path):
        return None, None, None, None

    # Lecture robuste du CSV
    try:
        df = pd.read_csv(file_path, sep=';', encoding='utf-8-sig', low_memory=False)
    except Exception:
        try:
            df = pd.read_csv(file_path, sep=';', encoding='latin-1', low_memory=False)
        except Exception:
            return None, None, None, None

    loaded_path = file_path

    # Nettoyage des colonnes
    df.columns = df.columns.str.strip()

    # Normalisation des noms de colonnes utiles
    cols_lower = {c.lower(): c for c in df.columns}

    # Colonne Région
    region_col = None
    for c in df.columns:
        if c.lower().strip() == "region":
            region_col = c
            break

    if region_col is None:
        # fallback : cherche un nom proche
        region_col = next((c for c in df.columns if "region" in c.lower()), None)

    if region_col is not None:
        df["Region_clean"] = df[region_col].apply(normalize_str)
    else:
        df["Region_clean"] = ""

    # Conversions numériques
    cols_numeriques = [
        'RevenuMoyen_kEUR_par_menage', 'IndPrixLogements_France_base2000',
        'IndPrixLogements_Paris_base2000', 'IndiceLoyers_base2000',
        'Prix_m2', 'ValeurFonciere_EUR', 'Surface_Bati_m2',
        'PIB_MdEUR', 'DetteImmoMenages_MdEUR', 'TauxInteretLongTerme',
        'IPC_base2000', 'ICC_base2000',
        'Indice_RevenuMoyen_base2000', 'Indice_RevenuMoyen_base1',
        'Ratio_PrixLog_Revenu', 'Ratio_Paris_France', 'Ratio_Prix_Loyers',
        'Taux_Endettement_Immo', 'DureePrets_annees',
        'NbTransacLogementsAnciens', 'MontantTransacLogementsAnciens_MdEUR'
    ]

    for col in cols_numeriques:
        if col in df.columns:
            if df[col].dtype == 'object':
                df[col] = (
                    df[col].astype(str)
                    .str.replace(' ', '')
                    .str.replace(',', '.')
                    .str.replace('\xa0', '')
                )
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Colonne Année
    col_annee = next((c for c in df.columns if 'ann' in c.lower()), None)
    if col_annee:
        df['Annee'] = pd.to_numeric(df[col_annee], errors='coerce')

    # Code département (string formaté)
    dept_col = None
    for c in df.columns:
        if "departement" in c.lower():
            dept_col = c
            break

    if dept_col is not None:
        df['Dept_Str'] = df[dept_col].fillna('').astype(str).str.strip()

        def _format_dept(x):
            s = str(x).strip()
            if s == "":
                return ""
            s2 = s.split('.')[0]  # cas "75.0"
            if s2.isdigit():
                return s2.zfill(2)
            return s2

        df['Dept_Str'] = df['Dept_Str'].apply(_format_dept)
    else:
        df['Dept_Str'] = ""

    # Séparation Macro France / DVF Île-de-France (normalisé)
    df_macro = (
        df[df['Region_clean'] == 'france']
        .drop_duplicates(subset=['Annee'])
        .sort_values('Annee')
        .copy()
    )

    # IdF : tolérant ('ile de france', 'idf', etc.)
    idf_mask = df['Region_clean'].str.contains("ile de france") | df['Region_clean'].str.contains("idf")
    df_idf = df[idf_mask & df['Dept_Str'].isin(DEPT_COLORS.keys())].copy()

    # Filtrage des outliers DVF (méthode simplifiée)
    if 'Prix_m2' in df_idf.columns and not df_idf.empty:
        df_idf = df_idf[(df_idf['Prix_m2'] >= 500) & (df_idf['Prix_m2'] <= 25000)]

    return df, df_macro, df_idf, loaded_path


# Chargement des données
df_full, df_macro, df_idf, data_path = load_data()

if df_full is None or df_macro is None:
    st.error("❌ **Fichier de données introuvable ou illisible**")
    st.info("Placez le fichier `04_DF_Union_Macro_DVF.csv` dans le dossier de l'application.")
    st.stop()

# =============================================================================
# 5. SIDEBAR - FILTRES GLOBAUX
# =============================================================================

with st.sidebar:
    st.markdown("## 🎛️ Paramètres d'analyse")
    
    # ─────────────────────────────────────────────────────────────────────────
    # Période macro
    # ─────────────────────────────────────────────────────────────────────────
    st.markdown("### 📅 Période")
    
    annees_macro = sorted(df_macro['Annee'].dropna().unique())
    if len(annees_macro) >= 2:
        periode_macro = st.select_slider(
            "Années (Macro France)",
            options=annees_macro,
            value=(int(min(annees_macro)), int(max(annees_macro)))
        )
    else:
        periode_macro = (int(min(annees_macro)), int(max(annees_macro)))
    
    df_macro_f = df_macro[
        (df_macro['Annee'] >= periode_macro[0]) &
        (df_macro['Annee'] <= periode_macro[1])
    ].copy()
    
    # ─────────────────────────────────────────────────────────────────────────
    # Départements Île-de-France
    # ─────────────────────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 🗺️ Départements IdF")
    
    if df_idf is not None and not df_idf.empty:
        depts_dispo = sorted(df_idf['Dept_Str'].dropna().unique())
    else:
        depts_dispo = []
    
    depts_selected = st.multiselect(
        "Sélection",
        options=depts_dispo,
        default=depts_dispo,
        format_func=lambda x: f"{x} - {NOMS_DEPARTEMENTS.get(x, x)}"
    )
    
    df_idf_f = df_idf[df_idf['Dept_Str'].isin(depts_selected)].copy() if not df_idf.empty else df_idf.copy()
    
    # ─────────────────────────────────────────────────────────────────────────
    # Options graphiques
    # ─────────────────────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 🎨 Affichage")
    
    show_markers = st.checkbox("Marqueurs sur courbes", value=True)
    show_annotations = st.checkbox("Annotations", value=True)
    
    # ─────────────────────────────────────────────────────────────────────────
    # Stats
    # ─────────────────────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 📊 Données chargées")
    st.markdown(f"**Macro France:** {len(df_macro_f)} années (filtre courant)")
    if df_idf_f is not None and not df_idf_f.empty:
        st.markdown(f"**DVF IdF:** {len(df_idf_f):,} transactions (filtre courant)")
    else:
        st.markdown("**DVF IdF:** 0 transaction (vérifier le filtre ou les données)")
    
    if data_path:
        st.caption(f"📁 {os.path.basename(data_path)}")

# =============================================================================
# 6. HEADER PRINCIPAL
# =============================================================================

st.markdown("""
<div class="header-banner">
    <p class="header-title">🏛️ Observatoire Stratégique de l'Immobilier</p>
    <p class="header-subtitle">Analyse du pouvoir d'achat immobilier France / Île-de-France • 1990-2025</p>
</div>
""", unsafe_allow_html=True)

st.write(
    "Présentation des Sources de Données\n\n"
    "L'application s'appuie sur trois sources de données publiques officielles : "
    "l'INSEE pour les indicateurs macroéconomiques français (prix logements, revenus, loyers, PIB, dette, etc.), "
    "la Banque de France pour les taux d'intérêt immobiliers, "
    "et la Direction Générale des Finances Publiques (DGFiP) pour les transactions immobilières via la base DVF.\n\n"
    "Les données macroéconomiques couvrent une période de 35 ans (1990-2025) avec 35 observations annuelles et 15 variables initiales, "
    "enrichies de 20 indicateurs calculés (ratios d'accessibilité, variations annuelles, taux d'endettement). "
    "Les données DVF portent sur les ventes d'appartements en Île-de-France depuis 2020, représentant plusieurs millions de transactions filtrées sur 8 départements (Paris et petite couronne).\n\n"
    "La qualité des données est assurée par un processus rigoureux de nettoyage et validation : filtrage des outliers par méthode IQR (suppression de 2-5% des transactions extrêmes), "
    "interpolation linéaire pour les valeurs manquantes mineures, et contrôles de cohérence temporelle. Le taux de complétude global dépasse 95% après traitement.\n\n"
    "Les indicateurs enrichis permettent d'analyser l'accessibilité immobilière via des ratios clés : Prix/Revenus (effort d'achat), Paris/France (écart de valorisation), Prix/Loyers (rendement locatif), et Taux d'endettement (Dette/Revenu).\n"
)

# Ajout du lien hypertexte à la fin


import pathlib, base64
import streamlit as st

html_path = pathlib.Path(__file__).parent / ".\presentation_jeu_donnees.html"

if html_path.exists():
    b64 = base64.b64encode(html_path.read_bytes()).decode("utf-8")
    data_url = f"data:text/html;base64,{b64}"
    st.markdown(
        f'<a href="{data_url}" target="_blank">🔗 Voir la présentation détaillée des données</a>',
        unsafe_allow_html=True
    )
else:
    st.error("Fichier 'presentation_jeu_donnees.html' introuvable.")





# =============================================================================
# 7. ONGLETS PRINCIPAUX
# =============================================================================

tabs = st.tabs([
    "📈 Tableau de Bord",
    "🇫🇷 Macro-économie France",
    "🗼 Focus Île-de-France",
    "⚙️ Graphiques Personnalisés",
    "☁️ Text Mining"
])

# =============================================================================
# TAB 1 : TABLEAU DE BORD (KPIs + Résumé)
# =============================================================================

with tabs[0]:
    
# --------------------------------------------------------------------
# KPIs Macro – tendance longue
# --------------------------------------------------------------------
    st.markdown('<p class="section-title">Indicateurs Clés France – Tendances Longues</p>', unsafe_allow_html=True)

    if not df_macro.empty:
        # Limiter les KPIs macro aux années <= 2020 (données macro disponibles jusqu'en 2020)
        df_macro_sorted = df_macro.sort_values("Annee").dropna(subset=["Annee"]).copy()
        df_macro_kpi = df_macro_sorted[df_macro_sorted["Annee"] <= 2020].copy()
        if df_macro_kpi.empty:
            # Si aucune donnée <= 2020 on retombe sur l'historique
            df_macro_kpi = df_macro_sorted.copy()

        last_year = int(df_macro_kpi["Annee"].max())
        target_ref_year = last_year - 30

        candidates = df_macro_kpi[df_macro_kpi["Annee"] >= target_ref_year]["Annee"]
        if not candidates.empty:
            ref_year = int(candidates.min())
        else:
            ref_year = int(df_macro_kpi["Annee"].min())

        df_last = df_macro_kpi[df_macro_kpi["Annee"] == last_year].iloc[0]
        df_ref = df_macro_kpi[df_macro_kpi["Annee"] == ref_year].iloc[0]
        horizon = last_year - ref_year

        mult = detecter_echelle(df_macro_kpi['IndPrixLogements_France_base2000'].tolist())

        col1, col2, col3, col4 = st.columns(4)

        # 1. Prix logements France (indice)
        with col1:
            val_last = df_last.get('IndPrixLogements_France_base2000', np.nan) * mult
            val_ref = df_ref.get('IndPrixLogements_France_base2000', np.nan) * mult
            if pd.notna(val_last) and pd.notna(val_ref) and val_ref > 0:
                delta = (val_last / val_ref - 1) * 100
                st.metric("🏷️ Prix logements (indice)", f"{val_last:.0f}", f"{delta:+.0f}% sur ~{horizon} ans")
            else:
                st.metric("🏷️ Prix logements (indice)", "N/A", "")

        # 2. Inflation (IPC)
        with col2:
            val_last = df_last.get('IPC_base2000', np.nan) * mult
            val_ref = df_ref.get('IPC_base2000', np.nan) * mult
            if pd.notna(val_last) and pd.notna(val_ref) and val_ref > 0:
                delta = (val_last / val_ref - 1) * 100
                st.metric("📈 Inflation (IPC)", f"{val_last:.0f}", f"{delta:+.0f}% sur ~{horizon} ans")
            else:
                st.metric("📈 Inflation (IPC)", "N/A", "")

        # 3. Revenu moyen / ménage
        with col3:
            val_last = df_last.get('RevenuMoyen_kEUR_par_menage', np.nan)
            val_ref = df_ref.get('RevenuMoyen_kEUR_par_menage', np.nan)
            if pd.notna(val_last) and pd.notna(val_ref) and val_ref > 0:
                delta = (val_last / val_ref - 1) * 100
                st.metric("💰 Revenu moyen / ménage", f"{val_last:.1f} k€", f"{delta:+.0f}% sur ~{horizon} ans")
            else:
                st.metric("💰 Revenu moyen / ménage", "N/A", "")

        # 4. Effort d'achat (Prix / Revenu)
        with col4:
            val_last = df_last.get('Ratio_PrixLog_Revenu', np.nan)
            val_ref = df_ref.get('Ratio_PrixLog_Revenu', np.nan)
            if pd.notna(val_last) and pd.notna(val_ref) and val_ref > 0:
                delta = (val_last / val_ref - 1) * 100
                st.metric("📉 Effort d'achat (Prix/Revenu)", f"{val_last:.2f}", f"{delta:+.0f}% sur ~{horizon} ans")
            else:
                st.metric("📉 Effort d'achat", "N/A", "")

    
    # ─────────────────────────────────────────────────────────────────────────
    # KPIs Île-de-France
    # ─────────────────────────────────────────────────────────────────────────
    st.markdown('<p class="section-title">Focus Île-de-France</p>', unsafe_allow_html=True)

    if df_idf_f is not None and not df_idf_f.empty:
        col1, col2, col3, col4 = st.columns(4)

        # Prix médian m2
        with col1:
            val = df_idf_f['Prix_m2'].median()
            st.metric("🏷️ Prix médian m² (IdF)", f"{val:,.0f} €")

        # Prix moyen m2
        with col2:
            val = df_idf_f['Prix_m2'].mean()
            st.metric("📊 Prix moyen m² (IdF)", f"{val:,.0f} €")

        # Nb transactions
        with col3:
            val = len(df_idf_f)
            st.metric("📋 Transactions (IdF)", f"{val:,}")

        # Valeur foncière médiane
        with col4:
            if 'ValeurFonciere_EUR' in df_idf_f.columns:
                val = df_idf_f['ValeurFonciere_EUR'].median()
                st.metric("💶 Valeur foncière médiane", f"{val:,.0f} €")
            else:
                st.metric("💶 Valeur foncière médiane", "N/A")

    st.markdown("---")
    
    # ─────────────────────────────────────────────────────────────────────────
    # G1 : Variations annuelles Prix vs Revenu vs IPC (reconstruit en Plotly)
    # ─────────────────────────────────────────────────────────────────────────
    st.markdown('<p class="section-title">G1 - Dynamique Prix vs Revenus (Variations annuelles %)</p>', unsafe_allow_html=True)
    
    if not df_macro_f.empty and len(df_macro_f) > 1:
        df_var = df_macro_f.copy().sort_values('Annee')
        mult = detecter_echelle(df_var['IndPrixLogements_France_base2000'].tolist())
        
        # Calcul des variations annuelles
        df_var['Var_Prix'] = (df_var['IndPrixLogements_France_base2000'] * mult).pct_change() * 100
        
        if 'Indice_RevenuMoyen_base2000' in df_var.columns:
            df_var['Var_Revenu'] = df_var['Indice_RevenuMoyen_base2000'].pct_change() * 100
        elif 'RevenuMoyen_kEUR_par_menage' in df_var.columns:
            df_var['Var_Revenu'] = df_var['RevenuMoyen_kEUR_par_menage'].pct_change() * 100
        
        if 'IPC_base2000' in df_var.columns:
            df_var['Var_IPC'] = (df_var['IPC_base2000'] * mult).pct_change() * 100
        
        df_var = df_var.dropna(subset=['Var_Prix'])
        
        fig = go.Figure()
        
        # Prix immobiliers
        fig.add_trace(go.Scatter(
            x=df_var['Annee'], y=df_var['Var_Prix'],
            name="Prix immobiliers",
            mode='lines+markers' if show_markers else 'lines',
            line=dict(color=COLORS['accent_red'], width=3),
            marker=dict(size=8)
        ))
        
        # Revenus
        if 'Var_Revenu' in df_var.columns:
            fig.add_trace(go.Scatter(
                x=df_var['Annee'], y=df_var['Var_Revenu'],
                name="Revenus ménages",
                mode='lines+markers' if show_markers else 'lines',
                line=dict(color=COLORS['accent_green'], width=3),
                marker=dict(size=8)
            ))
        
        # IPC
        if 'Var_IPC' in df_var.columns:
            fig.add_trace(go.Scatter(
                x=df_var['Annee'], y=df_var['Var_IPC'],
                name="Inflation (IPC)",
                mode='lines+markers' if show_markers else 'lines',
                line=dict(color=COLORS['accent_cyan'], width=2, dash='dash'),
                marker=dict(size=6)
            ))
        
        # Ligne de référence à 0
        fig.add_hline(y=0, line_dash="dash", line_color=COLORS['text_secondary'], opacity=0.5)
        
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            yaxis_title="Variation annuelle (%)",
            xaxis_title="Année",
            legend=dict(orientation="h", y=1.12),
            hovermode="x unified",
            height=450
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.info("💡 **Lecture** : Quand la courbe rouge (prix) est au-dessus de la verte (revenus), le pouvoir d'achat immobilier se dégrade.")

# =============================================================================
# TAB 2 : MACRO-ÉCONOMIE FRANCE
# =============================================================================

with tabs[1]:
    
    st.markdown('<p class="section-title">Analyse Macro-économique France</p>', unsafe_allow_html=True)
    
    # Menu de sélection des graphiques (aligné avec le notebook : G6, G7, G13)
    graph_choice = st.selectbox(
        "📊 Sélectionner le graphique",
        [
            "G2 - Indices Prix France/Paris vs Loyers",
            "G3 - Dette, Durée prêts, Transactions",
            "G6 - Indicateurs d'accessibilité"
        ],
        key="macro_graph_select"
    )
    
    st.markdown("---")
    
    # Détection échelle (pour les indices prix)
    mult = detecter_echelle(df_macro_f['IndPrixLogements_France_base2000'].tolist())
    
    # ─────────────────────────────────────────────────────────────────────────
    # G2 : Indices Prix France/Paris vs Loyers
    # ─────────────────────────────────────────────────────────────────────────
    if "G2" in graph_choice:
        st.markdown("### 🏠 Indices Prix France/Paris vs Loyers")
        st.info("Le décrochage entre prix de vente et loyers illustre la baisse du rendement locatif.")
        
        fig = go.Figure()
        
        # Prix France
        fig.add_trace(go.Scatter(
            x=df_macro_f['Annee'],
            y=df_macro_f['IndPrixLogements_France_base2000'] * mult,
            name="Prix logements France",
            mode='lines+markers' if show_markers else 'lines',
            line=dict(color=COLORS['france'], width=3),
            marker=dict(size=7)
        ))
        
        # Prix Paris
        if 'IndPrixLogements_Paris_base2000' in df_macro_f.columns:
            fig.add_trace(go.Scatter(
                x=df_macro_f['Annee'],
                y=df_macro_f['IndPrixLogements_Paris_base2000'] * mult,
                name="Prix logements Paris",
                mode='lines+markers' if show_markers else 'lines',
                line=dict(color=COLORS['paris'], width=3),
                marker=dict(size=7)
            ))
        
        # Loyers
        if 'IndiceLoyers_base2000' in df_macro_f.columns:
            fig.add_trace(go.Scatter(
                x=df_macro_f['Annee'],
                y=df_macro_f['IndiceLoyers_base2000'] * mult,
                name="Indice Loyers",
                mode='lines+markers' if show_markers else 'lines',
                line=dict(color=COLORS['loyers'], width=3),
                marker=dict(size=7)
            ))
        
        fig.add_hline(y=100, line_dash="dash", line_color=COLORS['text_secondary'],
                      annotation_text="Base 100 (2000)" if show_annotations else None)
        
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            yaxis_title="Indice (base 2000 = 100)",
            xaxis_title="Année",
            legend=dict(orientation="h", y=1.12),
            hovermode="x unified",
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # ─────────────────────────────────────────────────────────────────────────
    # G3 : Dette, Durée prêts, Transactions
    # ─────────────────────────────────────────────────────────────────────────
    elif "G3" in graph_choice:
        st.markdown("### 🏦 Indicateurs du marché immobilier")
        
        # Choix du sous-graphique
        sub_choice = st.radio(
            "Indicateur",
            ["Durée moyenne des prêts", "Dette immobilière ménages", "Montant des transactions"],
            horizontal=True
        )
        
        fig = go.Figure()
        
        if sub_choice == "Durée moyenne des prêts" and 'DureePrets_annees' in df_macro_f.columns:
            fig.add_trace(go.Bar(
                x=df_macro_f['Annee'],
                y=df_macro_f['DureePrets_annees'],
                name="Durée (années)",
                marker_color=COLORS['taux']
            ))
            fig.update_layout(yaxis_title="Durée moyenne (années)")
        
        elif sub_choice == "Dette immobilière ménages" and 'DetteImmoMenages_MdEUR' in df_macro_f.columns:
            fig.add_trace(go.Bar(
                x=df_macro_f['Annee'],
                y=df_macro_f['DetteImmoMenages_MdEUR'],
                name="Dette (Md€)",
                marker_color=COLORS['dette']
            ))
            fig.update_layout(yaxis_title="Dette immobilière (Md€)")
        
        elif 'MontantTransacLogementsAnciens_MdEUR' in df_macro_f.columns:
            fig.add_trace(go.Bar(
                x=df_macro_f['Annee'],
                y=df_macro_f['MontantTransacLogementsAnciens_MdEUR'],
                name="Transactions (Md€)",
                marker_color=COLORS['idf']
            ))
            fig.update_layout(yaxis_title="Montant transactions (Md€)")
        
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis_title="Année",
            height=450,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # ─────────────────────────────────────────────────────────────────────────
    # G6 : Indicateurs d'accessibilité (ratios avec légendes et échelle)
    # ─────────────────────────────────────────────────────────────────────────
    elif "G6" in graph_choice:
        st.markdown("### 🏠 Indicateurs d'accessibilité immobilière")
        
        col1, col2 = st.columns(2)
        
        # ------------------------ Ratio Prix / Revenu ------------------------
        with col1:
            st.markdown("#### Ratio Prix / Revenu")
            if 'Ratio_PrixLog_Revenu' in df_macro_f.columns:
                mask = df_macro_f['Ratio_PrixLog_Revenu'].notna()
                df_ratio = df_macro_f[mask].copy()
                
                fig1 = go.Figure()
                fig1.add_trace(go.Scatter(
                    x=df_ratio['Annee'],
                    y=df_ratio['Ratio_PrixLog_Revenu'],
                    name="Ratio Prix / Revenu",
                    mode='lines+markers' if show_markers else 'lines',
                    line=dict(color=COLORS['paris'], width=2),
                    marker=dict(size=6)
                ))
                fig1.add_trace(go.Scatter(
                    x=df_ratio['Annee'],
                    y=[1] * len(df_ratio),
                    name="Base 1 (année 2000)",
                    mode='lines',
                    line=dict(color=COLORS['text_secondary'], dash="dash"),
                ))
                
                ratio_series = df_ratio['Ratio_PrixLog_Revenu']
                if not ratio_series.empty:
                    y_min = float(ratio_series.min())
                    y_max = float(ratio_series.max())
                    padding = (y_max - y_min) * 0.15 if y_max > y_min else 0.5
                    fig1.update_yaxes(
                        title_text="Nombre d'années de revenu moyen",
                        range=[max(0, y_min - padding), y_max + padding]
                    )
                else:
                    fig1.update_yaxes(title_text="Nombre d'années de revenu moyen")
                
                fig1.update_layout(
                    template="plotly_dark",
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    height=320,
                    hovermode="x unified",
                    showlegend=True,
                    legend=dict(orientation="h", y=1.15),
                    margin=dict(t=40, b=40, l=60, r=30)
                )
                st.plotly_chart(fig1, use_container_width=True)
            else:
                st.warning("Données non disponibles pour le ratio Prix / Revenu.")
        
        # --------------------- Ratio Paris / France --------------------------
        with col2:
            st.markdown("#### Écart Paris / France")
            if 'Ratio_Paris_France' in df_macro_f.columns:
                mask = df_macro_f['Ratio_Paris_France'].notna()
                df_ratio2 = df_macro_f[mask].copy()
                
                fig2 = go.Figure()
                fig2.add_trace(go.Scatter(
                    x=df_ratio2['Annee'],
                    y=df_ratio2['Ratio_Paris_France'],
                    name="Ratio Paris / France",
                    mode='lines+markers' if show_markers else 'lines',
                    line=dict(color=COLORS['paris'], width=2),
                    marker=dict(size=6)
                ))
                fig2.add_trace(go.Scatter(
                    x=df_ratio2['Annee'],
                    y=[1] * len(df_ratio2),
                    name="Paris = France (ratio 1)",
                    mode='lines',
                    line=dict(color=COLORS['text_secondary'], dash="dash"),
                ))
                
                ratio_series2 = df_ratio2['Ratio_Paris_France']
                if not ratio_series2.empty:
                    y_min2 = float(ratio_series2.min())
                    y_max2 = float(ratio_series2.max())
                    padding2 = (y_max2 - y_min2) * 0.15 if y_max2 > y_min2 else 0.2
                    fig2.update_yaxes(
                        title_text="Ratio Prix Paris / Prix France",
                        range=[max(0, y_min2 - padding2), y_max2 + padding2]
                    )
                else:
                    fig2.update_yaxes(title_text="Ratio Prix Paris / Prix France")
                
                fig2.update_layout(
                    template="plotly_dark",
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    height=320,
                    hovermode="x unified",
                    showlegend=True,
                    legend=dict(orientation="h", y=1.15),
                    margin=dict(t=40, b=40, l=60, r=30)
                )
                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.warning("Données non disponibles pour le ratio Paris / France.")
        
        col3, col4 = st.columns(2)
        
        # -------------------- Taux d'endettement immob. ---------------------
        with col3:
            st.markdown("#### Taux d'endettement immobilier")
            if 'Taux_Endettement_Immo' in df_macro_f.columns:
                fig3 = go.Figure()
                fig3.add_trace(go.Bar(
                    x=df_macro_f['Annee'],
                    y=df_macro_f['Taux_Endettement_Immo'],
                    marker_color=COLORS['dette'],
                    name="Taux d'endettement"
                ))
                fig3.update_layout(
                    template="plotly_dark",
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    yaxis_title="Années de revenu",
                    height=320,
                    showlegend=False,
                    margin=dict(t=40, b=40, l=60, r=30)
                )
                st.plotly_chart(fig3, use_container_width=True)
            else:
                st.warning("Données non disponibles pour le taux d'endettement.")
        
        # ---------------------- Ratio Prix / Loyers --------------------------
        with col4:
            st.markdown("#### Ratio Prix / Loyers")
            if 'Ratio_Prix_Loyers' in df_macro_f.columns:
                mask = df_macro_f['Ratio_Prix_Loyers'].notna()
                df_ratio4 = df_macro_f[mask].copy()
                
                fig4 = go.Figure()
                fig4.add_trace(go.Scatter(
                    x=df_ratio4['Annee'],
                    y=df_ratio4['Ratio_Prix_Loyers'],
                    name="Ratio Prix / Loyers",
                    mode='lines+markers' if show_markers else 'lines',
                    line=dict(color=COLORS['loyers'], width=2),
                    marker=dict(size=6)
                ))
                fig4.add_trace(go.Scatter(
                    x=df_ratio4['Annee'],
                    y=[1] * len(df_ratio4),
                    name="Seuil 1 (rendement stable)",
                    mode='lines',
                    line=dict(color=COLORS['text_secondary'], dash="dash"),
                ))
                
                ratio_series4 = df_ratio4['Ratio_Prix_Loyers']
                if not ratio_series4.empty:
                    y_min4 = float(ratio_series4.min())
                    y_max4 = float(ratio_series4.max())
                    padding4 = (y_max4 - y_min4) * 0.15 if y_max4 > y_min4 else 0.2
                    fig4.update_yaxes(
                        title_text="Ratio Prix / Loyers",
                        range=[max(0, y_min4 - padding4), y_max4 + padding4]
                    )
                else:
                    fig4.update_yaxes(title_text="Ratio Prix / Loyers")
                
                fig4.update_layout(
                    template="plotly_dark",
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    height=320,
                    hovermode="x unified",
                    showlegend=True,
                    legend=dict(orientation="h", y=1.15),
                    margin=dict(t=40, b=40, l=60, r=30)
                )
                st.plotly_chart(fig4, use_container_width=True)
            else:
                st.warning("Données non disponibles pour le ratio Prix / Loyers.")

# =============================================================================
# TAB 3 : FOCUS ÎLE-DE-FRANCE
# =============================================================================

with tabs[2]:
    
    st.markdown('<p class="section-title">Analyse Île-de-France</p>', unsafe_allow_html=True)
    
    if df_idf_f is None or df_idf_f.empty:
        st.warning("⚠️ Aucune donnée disponible pour les départements IdF sélectionnés ou dans le fichier.")
    else:
        # Menu de sélection (aligné avec le notebook : G4, G5, Distribution/violin)
        graph_idf_choice = st.selectbox(
            "📊 Sélectionner le graphique",
            [
                "G4 - Prix m² par département",
                "G5 - Top 10 communes les plus chères / moins chères",
                "Distribution des prix au m² (violin plot)"
            ],
            key="idf_graph_select"
        )
        
        st.markdown("---")
        
        # ─────────────────────────────────────────────────────────────────────
        # G4 : Prix par département (Barres, médiane seulement)
        # ─────────────────────────────────────────────────────────────────────
        if "G4" in graph_idf_choice:
            st.markdown("### 🏢 Prix médian au m² par département (Idf)")
            
            # Agrégation : médiane + nombre de ventes
            df_dept = df_idf_f.groupby('Dept_Str').agg(
                Prix_median=('Prix_m2', 'median'),
                Nb_ventes=('Prix_m2', 'count')
            ).reset_index()
            
            df_dept['Nom'] = df_dept['Dept_Str'].map(lambda x: f"{x} - {NOMS_DEPARTEMENTS.get(x, x)}")
            df_dept = df_dept.sort_values('Prix_median', ascending=True)
            
            colors = [DEPT_COLORS.get(d, '#666') for d in df_dept['Dept_Str']]
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=df_dept['Prix_median'],
                y=df_dept['Nom'],
                orientation='h',
                marker_color=colors,
                text=df_dept['Prix_median'].apply(lambda x: f"{x:,.0f} €/m²"),
                textposition='outside',
                name="Prix médian €/m²"
            ))
            
            med_idf = df_idf_f['Prix_m2'].median()
            fig.add_vline(
                x=med_idf,
                line_dash="dash",
                line_color=COLORS['accent_orange'],
                annotation_text=f"Médiane IdF: {med_idf:,.0f} €" if show_annotations else None,
                annotation_position="top"
            )
            
            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis_title="Prix médian au m² (€)",
                height=450,
                showlegend=True,
                legend=dict(orientation="h", y=1.08)
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            with st.expander("📋 Données détaillées par département"):
                st.dataframe(
                    df_dept[['Nom', 'Prix_median', 'Nb_ventes']]
                    .rename(columns={
                        'Nom': 'Département',
                        'Prix_median': 'Prix médian (€/m²)',
                        'Nb_ventes': 'Transactions'
                    })
                    .style.format({
                        'Prix médian (€/m²)': '{:,.0f}',
                        'Transactions': '{:,}'
                    }),
                    use_container_width=True
                )
        
        # ─────────────────────────────────────────────────────────────────────
        # G5 : Top 10 communes plus chères / moins chères
        # ─────────────────────────────────────────────────────────────────────
        elif "G5" in graph_idf_choice:
            st.markdown("### 💎 Top 10 communes les plus chères / moins chères")
            
            col_top, col_opts = st.columns([1, 3])
            with col_top:
                mode_top = st.radio(
                    "Classement",
                    ["Top 10 plus chères", "Top 10 moins chères"],
                    horizontal=False
                )
            with col_opts:
                seuil = st.slider("Minimum de ventes pour fiabilité", 10, 200, 50)
            
            if 'Commune' in df_idf_f.columns:
                df_commune = df_idf_f.groupby(['Commune', 'Dept_Str']).agg(
                    Prix_median=('Prix_m2', 'median'),
                    Prix_moyen=('Prix_m2', 'mean'),
                    Nb_ventes=('Prix_m2', 'count')
                ).reset_index()
                
                df_commune = df_commune[df_commune['Nb_ventes'] >= seuil]
                
                if mode_top == "Top 10 plus chères":
                    df_top10 = df_commune.nlargest(10, 'Prix_median').sort_values('Prix_median', ascending=True)
                    titre = f"Top 10 communes les plus chères (min {seuil} transactions)"
                else:
                    df_top10 = df_commune.nsmallest(10, 'Prix_median').sort_values('Prix_median', ascending=True)
                    titre = f"Top 10 communes les plus abordables (min {seuil} transactions)"
                
                df_top10['Label'] = df_top10['Commune'] + " (" + df_top10['Dept_Str'] + ")"
                colors = [DEPT_COLORS.get(d, '#666') for d in df_top10['Dept_Str']]
                
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=df_top10['Prix_median'],
                    y=df_top10['Label'],
                    orientation='h',
                    marker_color=colors,
                    text=df_top10.apply(
                        lambda r: f"{r['Prix_median']:,.0f} €/m² ({r['Nb_ventes']} ventes)",
                        axis=1
                    ),
                    textposition='outside',
                    name="Prix médian €/m²"
                ))
                
                fig.update_layout(
                    template="plotly_dark",
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    title=titre,
                    xaxis_title="Prix médian au m² (€)",
                    height=500,
                    showlegend=True,
                    legend=dict(orientation="h", y=1.05)
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Colonne 'Commune' non disponible dans les données DVF IdF.")
        
        # ─────────────────────────────────────────────────────────────────────
        # Distribution des prix (violin)
        # ─────────────────────────────────────────────────────────────────────
        elif "Distribution" in graph_idf_choice:
            st.markdown("### 📊 Distribution des prix au m² par département (violin plot)")
            
            fig = px.violin(
                df_idf_f,
                x='Dept_Str',
                y='Prix_m2',
                color='Dept_Str',
                color_discrete_map=DEPT_COLORS,
                box=True
            )
            
            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis_title="Département",
                yaxis_title="Prix au m² (€)",
                legend=dict(orientation="h", y=1.05),
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# TAB 4 : GRAPHIQUES PERSONNALISÉS (VERSION PROPRE & FILTRÉE)
# =============================================================================

with tabs[3]:
    
    st.markdown('<p class="section-title">Créateur de graphiques</p>', unsafe_allow_html=True)
    
    col_config, col_result = st.columns([1, 2])
    
    # =====================================================================
    # CONFIGURATION UTILISATEUR
    # =====================================================================
    with col_config:
        st.markdown("### ⚙️ Configuration")
        
        # Choix de la source
        source = st.radio("Source de données", ["Macro France", "Île-de-France"])
        df_work = df_macro_f.copy() if source == "Macro France" else df_idf_f.copy()
        
        if df_work is None or df_work.empty:
            st.warning("Pas de données disponibles pour la source sélectionnée.")
        else:
            # =============================================================
            # LISTES CONTRÔLÉES DE COLONNES AUTORISÉES POUR DES GRAPHIQUES
            # =============================================================
            
            if source == "Macro France":
                allowed_y = [
                    'IndPrixLogements_France_base2000',
                    'IndPrixLogements_Paris_base2000',
                    'IndiceLoyers_base2000',
                    'Indice_RevenuMoyen_base2000',
                    'RevenuMoyen_kEUR_par_menage',
                    'DetteImmoMenages_MdEUR',
                    'MontantTransacLogementsAnciens_MdEUR',
                    'NbTransacLogementsAnciens',
                    'TauxInteretLongTerme',
                    'PIB_MdEUR',
                    'IPC_base2000',
                    'ICC_base2000',
                    'Ratio_PrixLog_Revenu',
                    'Ratio_Prix_Loyers',
                    'Ratio_Paris_France',
                    'Evol_PrixLog_France_pct',
                    'Evol_Revenu_pct',
                    'Evol_Dette_pct'
                ]
            else:  # SOURCE IDF
                allowed_y = [
                    'Prix_m2',
                    'ValeurFonciere_EUR',
                    'Surface_Bati_m2'
                ]
            
            # Sélection finale des colonnes autorisées disponibles dans le DF
            num_cols = [c for c in allowed_y if c in df_work.columns]
            
            # Axe X = année si dispo
            default_x = "Annee" if "Annee" in df_work.columns else num_cols[0]
            x_col = st.selectbox("Axe X", [default_x] + [c for c in num_cols if c != default_x])
            
            # Axe Y (une ou plusieurs variables autorisées)
            y_cols = st.multiselect(
                "Axe(s) Y",
                num_cols,
                default=[c for c in num_cols if c != x_col][:1]
            )
            
            # Type de graphique
            chart_type = st.selectbox("Type", ["Ligne", "Barres", "Aire", "Scatter", "Histogramme"])
            
            # Option "colorer par département" uniquement si source IdF
            color_options = ["Aucun"]
            if source == "Île-de-France" and 'Dept_Str' in df_work.columns:
                color_options.append("Dept_Str")
            
            color_by = st.selectbox("Colorer par", color_options)
    
    # =====================================================================
    # RÉSULTAT DU GRAPHIQUE
    # =====================================================================
    with col_result:
        st.markdown("### 📊 Résultat")
        
        if df_work is None or df_work.empty:
            st.info("Aucune donnée à afficher pour cette source.")
        
        elif not y_cols:
            st.info("👆 Sélectionnez au moins une variable pour l'axe Y.")
        
        else:
            try:
                color_param = color_by if color_by != "Aucun" else None
                
                # ---------------------------------------------------------
                # GRAPH TYPE : LIGNE
                # ---------------------------------------------------------
                if chart_type == "Ligne":
                    
                    if color_param is None:
                        fig = px.line(df_work, x=x_col, y=y_cols, markers=show_markers)
                    else:
                        if len(y_cols) > 1:
                            st.warning(
                                "Avec 'Colorer par', seule la première série Y est utilisée. "
                                "Les couleurs représentent les catégories (ex : départements)."
                            )
                        fig = px.line(
                            df_work,
                            x=x_col,
                            y=y_cols[0],
                            color=color_param,
                            markers=show_markers
                        )
                
                # ---------------------------------------------------------
                # GRAPH TYPE : BARRES
                # ---------------------------------------------------------
                elif chart_type == "Barres":
                    
                    if color_param is None:
                        fig = px.bar(df_work, x=x_col, y=y_cols, barmode='group')
                    else:
                        if len(y_cols) > 1:
                            st.warning(
                                "Avec 'Colorer par', seule la première série Y est utilisée."
                            )
                        fig = px.bar(df_work, x=x_col, y=y_cols[0], color=color_param)
                
                # ---------------------------------------------------------
                # GRAPH TYPE : AIRE
                # ---------------------------------------------------------
                elif chart_type == "Aire":
                    
                    if color_param is None:
                        fig = px.area(df_work, x=x_col, y=y_cols)
                    else:
                        if len(y_cols) > 1:
                            st.warning(
                                "Avec 'Colorer par', seule la première série Y est utilisée."
                            )
                        fig = px.area(df_work, x=x_col, y=y_cols[0], color=color_param)
                
                # ---------------------------------------------------------
                # GRAPH TYPE : SCATTER
                # ---------------------------------------------------------
                elif chart_type == "Scatter":
                    
                    if len(y_cols) >= 2:
                        fig = px.scatter(df_work, x=y_cols[0], y=y_cols[1], color=color_param)
                    else:
                        fig = px.scatter(df_work, x=x_col, y=y_cols[0], color=color_param)
                
                # ---------------------------------------------------------
                # GRAPH TYPE : HISTOGRAMME
                # ---------------------------------------------------------
                else:  # Histogramme
                    fig = px.histogram(df_work, x=y_cols[0], color=color_param, nbins=30)
                
                # ---------------------------------------------------------
                # STYLE
                # ---------------------------------------------------------
                fig.update_layout(
                    template="plotly_dark",
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    title=f"{chart_type} : {', '.join(y_cols)}",
                    height=500,
                    showlegend=True,
                    legend=dict(orientation="h", y=1.08)
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # EXPORT CSV
                with st.expander("📥 Exporter les données"):
                    cols_export = [x_col] + y_cols
                    csv = df_work[cols_export].dropna().to_csv(index=False, sep=';')
                    st.download_button(
                        "📄 Télécharger CSV",
                        csv,
                        f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        "text/csv"
                    )
            
            except Exception as e:
                st.error(f"Erreur : {e}")

# =============================================================================
# TAB 5 : TEXT MINING (articles de presse, nuage de mots)
# =============================================================================

# --- Fonctions utilitaires Text Mining ---------------------------------------

def charger_corpus(repertoire_textes: str) -> str:
    texte_brut = ""

    if not os.path.isdir(repertoire_textes):
        raise FileNotFoundError(f"Le dossier '{repertoire_textes}' n'existe pas.")

    for nom_fichier in os.listdir(repertoire_textes):
        chemin = os.path.join(repertoire_textes, nom_fichier)
        if not os.path.isfile(chemin):
            continue

        if nom_fichier.lower().endswith(".md"):
            try:
                result = subprocess.run(
                    ["pandoc", chemin, "-t", "plain"],
                    capture_output=True,
                    text=True,
                    check=True,
                )
                contenu = result.stdout
            except Exception:
                with open(chemin, "r", encoding="utf-8") as f:
                    contenu = f.read()
        else:
            with open(chemin, "r", encoding="utf-8") as f:
                contenu = f.read()

        texte_brut += contenu + " "

    return texte_brut


def nettoyer_texte(texte_brut: str) -> dict:
    etapes = {}

    # Texte brut concaténé
    etapes["texte_brut"] = texte_brut

    # Passage en minuscules
    texte = texte_brut.lower()
    etapes["minuscules"] = texte

    # Nettoyage (ponctuation, chiffres…)
    texte = re.sub(r"[^a-zàâäéèêëïîôöùûüçœæ\s]", " ", texte)
    texte = re.sub(r"\s+", " ", texte).strip()
    etapes["nettoye"] = texte

    # Tokenisation
    tokens = word_tokenize(texte, language="french")
    etapes["tokens"] = tokens

    # Stopwords + mots indésirables
    stopwords_fr = set(stopwords.words("french"))
    mots_sale = {"forbes", "brandvoice", "newsletter", "service", "club", "logo"}
    stopwords_fr.update(mots_sale)

    tokens_filtres = [mot for mot in tokens if mot not in stopwords_fr and len(mot) > 2]
    etapes["tokens_filtres"] = tokens_filtres

    # Racinisation
    stemmer = FrenchStemmer()
    tokens_stemmes = []
    for mot in tokens_filtres:
        try:
            tokens_stemmes.append(stemmer.stem(mot))
        except Exception:
            tokens_stemmes.append(mot)

    tokens_stemmes = [mot for mot in tokens_stemmes if len(mot) > 2]
    etapes["tokens_stemmes"] = tokens_stemmes

    return etapes


def generer_wordcloud(tokens_stemmes):
    texte_final = " ".join(tokens_stemmes)

    wordcloud = WordCloud(
        width=1000,
        height=600,
        background_color="white",
        colormap="viridis",
        collocations=False,
    ).generate(texte_final)

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    ax.set_title("Nuage de mots")
    return fig


# --- Contenu de l’onglet Text Mining ----------------------------------------

with tabs[4]:
    st.markdown('<p class="section-title">Text Mining – Articles de presse</p>', unsafe_allow_html=True)

    st.write(
        "Cette section charge les articles d’un dossier, les nettoie et génère un "
        "nuage de mots à partir des racines (stemming) en français."
    )

    # Saisie du dossier
    repertoire_default = "/Users/edouardlacroix/Desktop/Projet DataManagment PS1 FINAL/INPUT/ARTICLES_PRESSE"
    repertoire_textes = st.text_input(
        "Dossier contenant les articles (.md, .txt, etc.)",
        value=repertoire_default,
        key="tm_repertoire",
    )

    if st.button("Lancer l'analyse", key="tm_bouton"):
        try:
            texte_brut = charger_corpus(repertoire_textes)
            if not texte_brut.strip():
                st.warning("Aucun texte trouvé dans ce dossier.")
            else:
                etapes = nettoyer_texte(texte_brut)

                # Zone d'affichage des étapes
                st.subheader("Étapes du traitement")

                with st.expander("Texte brut concaténé"):
                    st.text_area(
                        "Texte brut",
                        value=etapes["texte_brut"][:20000],
                        height=200,
                    )

                with st.expander("Après passage en minuscules"):
                    st.text_area(
                        "Minuscules",
                        value=etapes["minuscules"][:20000],
                        height=200,
                    )

                with st.expander("Après nettoyage (ponctuation/chiffres)"):
                    st.text_area(
                        "Nettoyé",
                        value=etapes["nettoye"][:20000],
                        height=200,
                    )

                with st.expander("Tokens (avant stopwords)"):
                    st.write(etapes["tokens"][:500])

                with st.expander("Tokens (après stopwords et mots courts)"):
                    st.write(etapes["tokens_filtres"][:500])

                with st.expander("Tokens après racinisation"):
                    st.write(etapes["tokens_stemmes"][:500])

                # Nuage de mots
                st.subheader("Nuage de mots")
                fig = generer_wordcloud(etapes["tokens_stemmes"])
                st.pyplot(fig)

        except FileNotFoundError as e:
            st.error(str(e))
        except Exception as e:
            st.error(f"Une erreur est survenue : {e}")
