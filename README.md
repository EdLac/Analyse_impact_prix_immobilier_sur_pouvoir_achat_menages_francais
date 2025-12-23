# 🏛️ Observatoire Stratégique de l’Immobilier Français

Application d’analyse et de visualisation de données immobilières françaises, développée dans le cadre d’un **projet de Data Management**.  
Le projet combine **données macroéconomiques nationales** et **transactions immobilières (DVF) en Île-de-France**, avec une interface interactive réalisée sous **Streamlit**.

---

## 🎯 Objectifs du projet

- Centraliser et nettoyer des **données immobilières hétérogènes**
- Construire des **indicateurs économiques pertinents** (accessibilité, ratios, évolutions)
- Proposer un **tableau de bord interactif** destiné à l’analyse stratégique
- Illustrer des concepts de **data management, data visualisation et text mining**

---

## 📊 Sources de données

Les données utilisées proviennent exclusivement de sources publiques officielles :

- **INSEE**
  - Prix des logements
  - Revenus des ménages
  - Loyers
  - PIB, inflation (IPC), indice du coût de la construction (ICC)
- **Banque de France**
  - Taux d’intérêt immobiliers
  - Durée moyenne des prêts
  - Dette immobilière des ménages
- **DGFiP – Base DVF**
  - Transactions immobilières (appartements)
  - Prix au m²
  - Valeur foncière
  - Surface bâtie  
  - Périmètre : **Île-de-France (8 départements)**

---

## 🧱 Structure du projet

```text
├── Data_Management__Projet_Notebook.ipynb # Notebook d’analyse et de préparation des données
├── Data_Management_Projet_Streamlit.py # Application Streamlit finale
├── OUTPUT/
│ └── 04_DF_Union_Macro_DVF.csv # Dataset consolidé (macro + DVF)
├── INPUT/
│ └── ARTICLES_PRESSE/ # Corpus textuel pour le text mining
└── README.md
```

---

## ⚙️ Fonctionnalités principales

### 📈 Analyse macroéconomique (France)

- Évolution des **prix immobiliers vs revenus vs inflation**
- Comparaison **France / Paris**
- Analyse de la dette immobilière et des transactions
- Indicateurs d’accessibilité :
  - Ratio Prix / Revenu
  - Ratio Prix / Loyers
  - Ratio Paris / France
  - Taux d’endettement immobilier

### 🗼 Focus Île-de-France (DVF)

- Prix médian au m² par département
- Top 10 des communes les plus chères / les plus abordables
- Distribution des prix (violin plots)
- Filtres dynamiques par département et période

### ⚙️ Graphiques personnalisés

- Création de graphiques sur mesure
- Choix de la source (Macro France ou DVF IdF)
- Export des données filtrées en **CSV**

### ☁️ Text Mining

- Analyse d’articles de presse immobilière
- Nettoyage linguistique (tokenisation, stopwords, stemming)
- Génération d’un **nuage de mots** en français
- Visualisation des étapes intermédiaires

---

## 🧠 Méthodologie Data Management

- Nettoyage avancé :
  - Harmonisation des formats
  - Détection et suppression d’outliers
  - Gestion des valeurs manquantes
- Normalisation des indices (base 1 / base 100)
- Construction d’indicateurs dérivés
- Validation de la cohérence temporelle
- Taux de complétude final > **95 %**

---

## 🖥️ Technologies utilisées

- **Python**
- **Pandas / NumPy**
- **Plotly / Matplotlib**
- **Streamlit**
- **NLTK**
- **WordCloud**

---

## ▶️ Lancer l’application

1. Installer les dépendances :
```bash
pip install streamlit pandas numpy plotly matplotlib nltk wordcloud
```
2. Placer le fichier de données :

OUTPUT/04_DF_Union_Macro_DVF.csv

3. Lancer l’application :

streamlit run Data_Management_Projet_Streamlit.py

## 📌 Contexte académique

Projet réalisé dans le cadre d’un cours de Data Management, visant à démontrer la capacité à :

- Gérer des jeux de données complexes  
- Construire des indicateurs économiques pertinents  
- Développer une application analytique professionnelle  
- Rendre les résultats accessibles à un public non technique  
