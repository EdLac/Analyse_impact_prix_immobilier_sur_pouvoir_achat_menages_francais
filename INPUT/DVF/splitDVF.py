#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Extraction des lignes d'une liste de fichiers .txt
pour UN OU PLUSIEURS codes département saisis par l'utilisateur.

- INPUT_PATH peut être :
    * un dossier : on lit tous les *.txt du dossier
    * un fichier .txt : on ne lit que ce fichier
- Filtre sur la colonne CODE_COL_NAME (ex : "code_departement")
- L'utilisateur peut saisir plusieurs codes :
    ex : 75, 76, 27  ou  75 76 27
- Toutes les lignes dont le code appartient à cette liste sont extraites
  dans un fichier de sortie unique.
"""

import os
import glob
import csv

# ====== PARAMÈTRES À ADAPTER ===================================

# Chemin d'entrée : dossier OU fichier .txt
# EXEMPLE 1 : dossier
# INPUT_PATH = r"C:\Users\berna\OneDrive\Documents"

# EXEMPLE 2 : fichier unique
INPUT_PATH = r"C:\Users\berna\Downloads\DATADVF"

# Nom de la colonne contenant le code département (nom EXACT de l'en-tête)
CODE_COL_NAME = "Code departement"   # à adapter si besoin : "Code_departement", "Code departement", etc.

# Séparateur des colonnes dans le .txt
DELIMITER = "|"                      # souvent ";" pour les fichiers DVF/valeurs foncières

# Encodage des fichiers texte
ENCODING = "utf-8"                   # si problème, essayer "cp1252" ou "latin-1"

# Nom de base du fichier de sortie
OUTPUT_FILENAME_BASE = "extraction_departements"

# ===============================================================
# FONCTIONS UTILITAIRES
# ===============================================================

def collect_txt_files(input_path: str):
    """
    Retourne une liste de fichiers .txt à traiter à partir de INPUT_PATH.
    - Si input_path est un dossier -> tous les *.txt du dossier
    - Si input_path est un fichier .txt -> [input_path]
    - Sinon -> liste vide
    """
    if os.path.isdir(input_path):
        pattern = os.path.join(input_path, "*.txt")
        return glob.glob(pattern)
    elif os.path.isfile(input_path) and input_path.lower().endswith(".txt"):
        return [input_path]
    else:
        return []


def normalize_code(code: str) -> str:
    """
    Normalise légèrement un code de département pour comparer de façon
    plus robuste :
    - strip des espaces
    - majuscules
    - si le code est purement numérique -> suppression des zéros en tête
    (ex : "075" -> "75")
    - sinon (2A, 2B, ...) on garde tel quel
    """
    s = code.strip().upper()
    if not s:
        return s
    # Si tout est numérique, on supprime les zéros en tête
    if s.isdigit():
        return s.lstrip("0") or "0"
    # Sinon, on retourne tel quel (pour 2A, 2B, etc.)
    return s


# ===============================================================
# PROGRAMME PRINCIPAL
# ===============================================================

def main():
    # 1. Demande des codes département à l'utilisateur
    raw_input = input(
        "Entrez un ou plusieurs codes département à extraire "
        "(ex : 75, 76, 27 ou 75 76 27) : "
    ).strip()

    if not raw_input:
        print("Aucun code département saisi. Arrêt du script.")
        return

    # On découpe sur virgule, point-virgule ou espaces
    raw_codes = [c for c in
                 [x.strip() for x in raw_input.replace(";", " ").replace(",", " ").split()]
                 if c]

    if not raw_codes:
        print("Aucun code valide détecté. Arrêt du script.")
        return

    # Normalisation des codes (gestion des zéros en tête, majuscules)
    dept_codes_norm = {normalize_code(c) for c in raw_codes}

    print("Codes départements demandés :", ", ".join(sorted(dept_codes_norm)))
    print("-" * 60)

    # 2. Récupération des fichiers .txt à traiter
    txt_files = collect_txt_files(INPUT_PATH)

    if not txt_files:
        print(f"Aucun fichier .txt trouvé à partir de : {INPUT_PATH}")
        print("Vérifie que :")
        print(" - INPUT_PATH pointe bien vers un dossier existant ou un fichier .txt existant")
        print(" - Les fichiers ont bien l'extension .txt")
        return

    print(f"{len(txt_files)} fichier(s) .txt à traiter.")

    # 3. Dossier de sortie = dossier de INPUT_PATH
    if os.path.isdir(INPUT_PATH):
        output_dir = INPUT_PATH
    else:
        output_dir = os.path.dirname(INPUT_PATH)

    # On construit un suffixe avec les codes demandés (par ex. 27-75-76)
    codes_suffix = "-".join(sorted(dept_codes_norm))
    output_filename = f"{OUTPUT_FILENAME_BASE}_{codes_suffix}.txt"
    output_path = os.path.join(output_dir, output_filename)

    total_lignes_conservees = 0
    writer = None  # sera créé au premier fichier où la colonne existe

    with open(output_path, "w", newline="", encoding=ENCODING) as fout:
        for path in txt_files:
            print(f"Traitement du fichier : {os.path.basename(path)}")

            try:
                with open(path, "r", newline="", encoding=ENCODING) as fin:
                    reader = csv.DictReader(fin, delimiter=DELIMITER)

                    # Vérifier que la colonne existe dans ce fichier
                    if CODE_COL_NAME not in (reader.fieldnames or []):
                        print(f"  ⚠ Colonne '{CODE_COL_NAME}' absente, fichier ignoré.")
                        print(f"    Colonnes trouvées : {reader.fieldnames}")
                        continue

                    # Créer le writer avec les bons fieldnames au premier fichier valide
                    if writer is None:
                        writer = csv.DictWriter(
                            fout,
                            fieldnames=reader.fieldnames,
                            delimiter=DELIMITER,
                        )
                        writer.writeheader()

                    lignes_conservees_fichier = 0
                    for row in reader:
                        raw_code = row.get(CODE_COL_NAME, "")
                        norm_code = normalize_code(raw_code)

                        if norm_code in dept_codes_norm:
                            writer.writerow(row)
                            total_lignes_conservees += 1
                            lignes_conservees_fichier += 1

                    print(f"  → {lignes_conservees_fichier} ligne(s) conservée(s) dans ce fichier.")

            except UnicodeDecodeError:
                print(f"  ⚠ Problème d'encodage pour {path}. "
                      f"Essaie de changer ENCODING (actuel : {ENCODING}).")
            except Exception as e:
                print(f"  ⚠ Erreur lors de la lecture de {path} : {e}")

    print("-" * 60)
    print(f"Terminé. Total de lignes extraites : {total_lignes_conservees}")
    print(f"Résultat enregistré dans : {output_path}")


if __name__ == "__main__":
    main()
