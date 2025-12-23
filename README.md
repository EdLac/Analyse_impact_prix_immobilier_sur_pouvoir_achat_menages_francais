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
├── Data_Management__Projet_Notebook.ipynb
├── Data_Management_Projet_Streamlit.py
│
├── INPUT/
│   ├── ARTICLES_PRESSE/
│   │   └── *.md / *.txt                
│   │
│   ├── DATADV/
│   │   ├── splitDVF.py                   
│   │   ├── ValeursFoncieres-2020-S2.txt
│   │   ├── ValeursFoncieres-2021.txt
│   │   ├── ValeursFoncieres-2022.txt
│   │   ├── ValeursFoncieres-2023.txt
│   │   ├── ValeursFoncieres-2024.txt
│   │   └── ValeursFoncieres-2025-S1.txt
│   │
│   ├── Dataprojetglobalhorsdvf.xlsx      
│   └── tauxinteretsBdFpourcomp_1990_2025.xlsx
│
├── OUTPUT/
│   ├── 01_Taux_Interet_BdF_Annuel.csv
│   ├── 02_DF_Macro_National.csv
│   ├── 03_DVF_IDF_Appartements.csv
│   ├── 04_DF_Union_Macro_DVF.csv         
│   │
│   ├── G1_France_Prix_Revenu_IPC.png
│   ├── G2_Indices_Prix_Loyers.png
│   ├── G3_Dette_Duree_Transactions.png
│   ├── G4_Prix_m2_Departements.png
│   ├── G5_Top10_Communes_Cheres.png
│   └── G6_Accessibilite_Immobiliere.png
│
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
2. Placer le fichier de données nettoyé :

OUTPUT/04_DF_Union_Macro_DVF.csv (voir OUTPUT)

3. Lancer l’application :

streamlit run Data_Management_Projet_Streamlit.py

## 📌 Contexte académique

Projet réalisé dans le cadre d’un cours de Data Management, visant à démontrer la capacité à :

- Gérer des jeux de données complexes  
- Construire des indicateurs économiques pertinents  
- Développer une application analytique professionnelle  
- Rendre les résultats accessibles à un public non technique  

## 👤 Auteurs  

Edouard LACROIX  
Bernard DRUI  
Oussama GUEDRI  
