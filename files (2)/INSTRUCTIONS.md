# 📋 INSTRUCTIONS - Guide de Déploiement Complet

> **Document à destination de l'équipe projet**  
> Dernière mise à jour : 17 Janvier 2026

---

## 🎯 Vue d'ensemble

Ce document explique **exactement** ce que tu dois faire pour remplacer l'ancien code par la nouvelle version de la plateforme CRR.

**Temps estimé** : 10-15 minutes

---

## 📁 Fichiers fournis

Tu as reçu **4 fichiers** :

| Fichier | Description | Action |
|---------|-------------|--------|
| `app.py` | Application Streamlit complète (~1500 lignes) | **Remplace** l'ancien `app.py` |
| `requirements.txt` | Dépendances Python | **Remplace** l'ancien `requirements.txt` |
| `README.md` | Documentation du projet | **Remplace** l'ancien `README.md` |
| `.gitignore` | Fichiers à ignorer par Git | **Remplace** l'ancien `.gitignore` |

---

## 🚀 Étapes à suivre (dans l'ordre)

### Étape 1 : Préparation locale

```bash
# 1. Ouvre ton terminal et va dans ton dossier projet
cd chemin/vers/Quant-Option-Portfolio

# 2. Vérifie que tu es sur la bonne branche
git branch
# Tu dois voir : * main (ou master)

# 3. Assure-toi d'avoir la dernière version
git pull origin main
```

### Étape 2 : Sauvegarde (optionnel mais recommandé)

```bash
# Crée une copie de sauvegarde de l'ancien code
mkdir -p backup
cp app.py backup/app_old.py
cp style.css backup/style_old.css
cp requirements.txt backup/requirements_old.txt
```

### Étape 3 : Remplacement des fichiers

**Option A - Manuellement :**
1. Télécharge les 4 fichiers que je t'ai fournis
2. Place-les à la **racine** de ton projet `Quant-Option-Portfolio/`
3. Remplace les fichiers existants quand on te le demande

**Option B - Par terminal :**
```bash
# Si tu as téléchargé les fichiers dans ~/Downloads/
cp ~/Downloads/app.py ./app.py
cp ~/Downloads/requirements.txt ./requirements.txt
cp ~/Downloads/README.md ./README.md
cp ~/Downloads/.gitignore ./.gitignore
```

### Étape 4 : Suppression de l'ancien CSS

> ⚠️ **Important** : Le nouveau `app.py` intègre tout le CSS directement dans le code Python. Le fichier `style.css` n'est plus nécessaire.

```bash
# Supprime l'ancien fichier CSS (il n'est plus utilisé)
rm style.css
```

**Pourquoi ?** Le CSS est maintenant intégré dans `app.py` via `st.markdown()`. Cela évite les problèmes de chemin de fichier et rend l'application plus portable.

### Étape 5 : Installation des dépendances

```bash
# Installe/met à jour les packages Python
pip install -r requirements.txt

# OU avec un environnement virtuel (recommandé)
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Étape 6 : Test en local

```bash
# Lance l'application
streamlit run app.py
```

**Vérifie que :**
- [ ] L'application s'ouvre dans ton navigateur (http://localhost:8501)
- [ ] Les 5 onglets sont visibles (Dashboard, CRR Model, Convergence, Hedging, Theory)
- [ ] Le sidebar permet de modifier les paramètres
- [ ] Les graphiques s'affichent correctement
- [ ] La simulation de hedging fonctionne (onglet 🛡️)

### Étape 7 : Commit sur GitHub

```bash
# 1. Vérifie les fichiers modifiés
git status

# Tu dois voir quelque chose comme :
#   modified:   app.py
#   modified:   requirements.txt
#   modified:   README.md
#   modified:   .gitignore
#   deleted:    style.css

# 2. Ajoute tous les fichiers
git add .

# 3. Crée le commit avec un message descriptif
git commit -m "🚀 Major update: Complete platform redesign with 5 tabs

- New professional dark theme (integrated CSS)
- Added interactive binomial tree visualization
- Added Monte Carlo hedging simulation with VaR
- Added convergence analysis dashboard
- Added mathematical theory section with LaTeX
- Removed external style.css dependency
- Updated documentation and README

See CHANGELOG.md for full details"

# 4. Push vers GitHub
git push origin main
```

### Étape 8 : Vérification sur GitHub

1. Va sur https://github.com/AlexisAHG/Quant-Option-Portfolio
2. Vérifie que les fichiers sont bien mis à jour
3. Vérifie que le README s'affiche correctement (avec les badges)

---

## 📂 Structure finale du projet

Après toutes les étapes, ton dossier doit ressembler à ça :

```
Quant-Option-Portfolio/
├── app.py                          # ✅ NOUVEAU (remplacé)
├── requirements.txt                # ✅ NOUVEAU (remplacé)
├── README.md                       # ✅ NOUVEAU (remplacé)
├── .gitignore                      # ✅ NOUVEAU (remplacé)
├── LICENSE                         # Existant (garde-le)
├── CHANGELOG.md                    # ✅ NOUVEAU (à ajouter)
├── INSTRUCTIONS.md                 # ✅ Ce fichier
│
├── Comparatif_des_interfaces_graphiques_pour_le_projet_CRR.ipynb  # Garde
├── Modèle_SABR_Compréhension_et_simulation.ipynb                  # Garde
├── Stochastic_Volatility_Models.ipynb                             # Garde
│
├── spx.csv                         # Garde (données)
├── vix_daily.csv                   # Garde (données)
│
└── backup/                         # Optionnel (ta sauvegarde)
    ├── app_old.py
    ├── style_old.css
    └── requirements_old.txt
```

**Note** : Le fichier `style.css` n'existe plus (CSS intégré dans app.py)

---

## 🧪 Tests à effectuer

Avant de considérer le déploiement comme terminé, vérifie chaque point :

### Dashboard (Onglet 1)
- [ ] Les 5 métriques en haut s'affichent (BS Price, CRR Price, u, d, p)
- [ ] Les Greeks s'affichent (Δ, Γ, ν, Θ, ρ)
- [ ] Le graphique de convergence s'affiche
- [ ] La comparaison des modèles est visible

### CRR Model (Onglet 2)
- [ ] L'arbre binomial s'affiche (hover sur les nœuds pour voir les valeurs)
- [ ] Les paramètres CRR sont corrects
- [ ] La condition de non-arbitrage est vérifiée

### Convergence (Onglet 3)
- [ ] Les 4 graphiques s'affichent
- [ ] Le slider "Maximum Steps" fonctionne
- [ ] Les valeurs de référence BS sont affichées

### Hedging Simulation (Onglet 4)
- [ ] Le bouton "Run Simulation" lance la simulation
- [ ] Les métriques de hedging s'affichent (Mean Error, VaR, etc.)
- [ ] Les 4 graphiques de résultats apparaissent

### Theory (Onglet 5)
- [ ] Les formules LaTeX s'affichent correctement
- [ ] Les sections CRR, BS, et limitations sont visibles

---

## ⚠️ Problèmes courants et solutions

### Problème : "ModuleNotFoundError: No module named 'plotly'"
```bash
pip install plotly
```

### Problème : "StreamlitAPIException: Unable to find style.css"
→ **Solution** : Tu utilises probablement l'ancien `app.py`. Assure-toi d'avoir remplacé le fichier.

### Problème : Les graphiques ne s'affichent pas
→ **Solution** : Vérifie que Plotly est bien installé :
```bash
pip install --upgrade plotly
```

### Problème : Le CSS ne s'applique pas / design cassé
→ **Solution** : Le nouveau `app.py` contient tout le CSS. Vide le cache Streamlit :
```bash
streamlit cache clear
```
Puis relance l'application.

### Problème : Git refuse de push
```bash
git pull origin main --rebase
git push origin main
```

---

## 📞 Checklist finale

Avant de dire "c'est terminé", coche tout :

- [ ] J'ai remplacé `app.py`
- [ ] J'ai remplacé `requirements.txt`
- [ ] J'ai remplacé `README.md`
- [ ] J'ai remplacé `.gitignore`
- [ ] J'ai supprimé `style.css`
- [ ] J'ai testé l'application en local
- [ ] Tous les 5 onglets fonctionnent
- [ ] J'ai commit et push sur GitHub
- [ ] J'ai vérifié sur GitHub que tout est en ligne

---

## 🎉 C'est terminé !

Une fois toutes les étapes complétées, ta plateforme CRR est opérationnelle.

**Prochaines étapes possibles :**
1. Ajouter les surfaces de volatilité implicite (avec yfinance)
2. Intégrer le modèle Heston
3. Déployer sur Streamlit Cloud pour un accès en ligne

---

*Document créé le 17/01/2026 pour le projet Pi² - ESILV*
