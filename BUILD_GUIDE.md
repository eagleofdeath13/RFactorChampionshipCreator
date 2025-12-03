# Guide de Build et Distribution

Ce guide explique comment créer un package distribuable de l'application **rFactor Championship Creator**.

---

## 📋 Prérequis pour le Build

### Environnement de Développement

- **Python 3.12+** avec `uv` installé
- **Node.js 18+** et **npm**
- **Git** (optionnel)

### Installation des Dépendances

```bash
# Python dependencies (avec uv)
uv sync

# Frontend dependencies
cd frontend
npm install
cd ..
```

---

## 🏗️ Processus de Build Complet

### Option 1 : Build Automatique (Recommandé)

**Étape unique** - Crée le package complet prêt à distribuer :

```bash
create_distribution.bat
```

Ce script effectue automatiquement :
1. ✅ Build du frontend React (`frontend/dist/`)
2. ✅ Build de l'exécutable PyInstaller (`dist/rfactor_championship_creator/`)
3. ✅ Copie du launcher et de la configuration
4. ✅ Création d'une archive ZIP

**Résultat :**
- Dossier : `dist/rfactor_championship_creator_v1.0/`
- Archive : `dist/rFactor_Championship_Creator_v1.0.zip`

---

### Option 2 : Build Manuel (Étape par Étape)

#### Étape 1 : Build du Frontend React

```bash
build_frontend.bat
```

**Ou manuellement :**

```bash
cd frontend
npm install
npm run build
cd ..
```

**Sortie :** `frontend/dist/` (fichiers HTML/CSS/JS statiques)

#### Étape 2 : Build de l'Exécutable

```bash
build_executable.bat
```

**Ou manuellement :**

```bash
# Installer les dépendances Python
uv sync

# Nettoyer les builds précédents
rmdir /s /q dist\rfactor_championship_creator
rmdir /s /q build

# Build avec PyInstaller
python -m PyInstaller rfactor_app.spec --clean
```

**Sortie :** `dist/rfactor_championship_creator/` (exécutable + dépendances)

#### Étape 3 : Préparer le Package de Distribution

Manuellement :

```bash
# Créer le dossier de distribution
mkdir dist\rfactor_championship_creator_v1.0

# Copier l'exécutable
xcopy dist\rfactor_championship_creator\* dist\rfactor_championship_creator_v1.0\ /E /I /Y

# Copier les fichiers nécessaires
copy RUN_APP.bat dist\rfactor_championship_creator_v1.0\
copy config.template.json dist\rfactor_championship_creator_v1.0\config.json
copy INSTALL.md dist\rfactor_championship_creator_v1.0\
copy README.md dist\rfactor_championship_creator_v1.0\
```

#### Étape 4 : Créer l'Archive ZIP

Avec PowerShell :

```powershell
Compress-Archive -Path "dist\rfactor_championship_creator_v1.0\*" -DestinationPath "dist\rFactor_Championship_Creator_v1.0.zip" -Force
```

Avec 7-Zip (si installé) :

```bash
7z a -tzip dist\rFactor_Championship_Creator_v1.0.zip dist\rfactor_championship_creator_v1.0\*
```

---

## 📦 Structure du Package Final

```
rfactor_championship_creator_v1.0/
├── rfactor_championship_creator.exe    # Exécutable principal
├── RUN_APP.bat                          # Launcher simple pour l'utilisateur
├── config.json                          # Configuration (template)
├── INSTALL.md                           # Guide d'installation
├── README.md                            # Documentation
├── _internal/                           # Dépendances PyInstaller
│   ├── Python DLLs
│   ├── Libraries Python
│   └── ...
├── src/                                 # Code source Python
│   └── web/
│       ├── templates/                   # Templates Jinja2 (backup)
│       └── static/                      # Fichiers statiques (backup)
└── frontend/                            # Frontend React (build)
    └── dist/
        ├── index.html
        ├── assets/
        │   ├── *.js
        │   └── *.css
        └── ...
```

---

## 🔧 Configuration PyInstaller

### Fichier `rfactor_app.spec`

Le fichier `.spec` configure PyInstaller pour :

1. **Point d'entrée** : `src/main.py`
2. **Inclusions de données** :
   - Templates Jinja2
   - Fichiers statiques
   - Frontend React build
   - `config.json`
3. **Modules cachés** :
   - FastAPI
   - Uvicorn
   - Pydantic
   - Jinja2
4. **Mode console** : `True` (pour voir les logs)

### Personnalisation

Pour modifier le build, éditez `rfactor_app.spec` :

```python
# Ajouter un icône
icon='path/to/icon.ico'

# Mode fenêtré (sans console)
console=False

# Exclure des modules
excludes=['module_name']
```

---

## 🧪 Tester le Package

### Test Local

1. **Build le package** :
   ```bash
   build_executable.bat
   ```

2. **Naviguer vers le build** :
   ```bash
   cd dist\rfactor_championship_creator
   ```

3. **Lancer l'exécutable** :
   ```bash
   rfactor_championship_creator.exe
   ```

4. **Vérifier** :
   - Le serveur démarre sur http://localhost:5000
   - Le navigateur s'ouvre automatiquement
   - L'interface React s'affiche correctement
   - Les API fonctionnent

### Test de Distribution

1. **Créer le package complet** :
   ```bash
   create_distribution.bat
   ```

2. **Copier** `dist\rfactor_championship_creator_v1.0\` vers un autre emplacement

3. **Configurer** `config.json` avec un chemin rFactor valide

4. **Lancer** `RUN_APP.bat`

5. **Tester** toutes les fonctionnalités :
   - Navigation dans l'interface
   - Lecture de talents, véhicules, circuits
   - Création d'un championnat custom
   - Vérification des fichiers générés dans rFactor

---

## 📝 Checklist Avant Distribution

- [ ] Frontend React buildé (`frontend/dist/` existe)
- [ ] Exécutable créé sans erreurs
- [ ] `RUN_APP.bat` inclus
- [ ] `config.json` template inclus
- [ ] `INSTALL.md` à jour
- [ ] Version incrémentée dans :
  - [ ] `pyproject.toml`
  - [ ] `src/web/app.py`
  - [ ] `create_distribution.bat` (nom du ZIP)
- [ ] Tests passants (`pytest`)
- [ ] Test du package sur machine propre (si possible)

---

## 🐛 Dépannage du Build

### Erreur : "Module not found"

→ Ajouter le module manquant dans `hiddenimports` du `.spec` :

```python
hiddenimports=['module_manquant']
```

### Le frontend ne s'affiche pas

→ Vérifier que `frontend/dist/` existe et est inclus dans `datas` :

```python
datas += [(frontend_dist, os.path.join('frontend', 'dist'))]
```

### L'exécutable est trop gros

→ Options de réduction :

1. Utiliser UPX (déjà activé) : `upx=True`
2. Exclure modules non utilisés : `excludes=[...]`
3. Mode "onefile" (plus lent au démarrage) :
   ```python
   exe = EXE(..., onefile=True)
   ```

### Erreur au lancement de l'exécutable

→ Lancer avec console activée pour voir les logs :

```python
console=True
```

---

## 🚀 Distribution

### Via GitHub Releases

1. Créer un tag de version :
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

2. Créer une release sur GitHub

3. Uploader le fichier ZIP :
   - `rFactor_Championship_Creator_v1.0.zip`

### Via Partage Direct

1. Compresser `dist\rfactor_championship_creator_v1.0\` en ZIP

2. Partager le ZIP via :
   - Google Drive
   - Dropbox
   - WeTransfer
   - Etc.

---

## 📊 Taille du Package

**Taille estimée :**
- Exécutable : ~80-120 MB
- Frontend : ~5-10 MB
- **Total** : ~100-150 MB (compressé en ZIP : ~40-60 MB)

**Raison de la taille :**
- Python runtime intégré (~50 MB)
- Dépendances FastAPI/Uvicorn (~30 MB)
- Bibliothèques système (~20 MB)
- Frontend React (~10 MB)

---

## 📅 Maintenance

### Mettre à Jour une Dépendance

1. Modifier `pyproject.toml` ou `requirements.txt`
2. Mettre à jour :
   ```bash
   uv sync
   ```
3. Rebuild :
   ```bash
   create_distribution.bat
   ```

### Ajouter une Nouvelle Feature

1. Développer la feature
2. Tester (`pytest`)
3. Rebuild le frontend si nécessaire
4. Rebuild l'exécutable
5. Incrémenter la version

---

## 🎯 Résumé Rapide

**Build complet en une commande :**

```bash
create_distribution.bat
```

**Fichier de sortie :**
- `dist\rFactor_Championship_Creator_v1.0.zip`

**Prêt à distribuer !** 🚀
