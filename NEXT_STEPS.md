# Prochaines étapes - Développement rFactor Championship Creator

## État actuel du projet

### ✅ Sprint 1 : Gestion des talents (Terminé)
- Parser RCD complet avec gestion des erreurs
- Modèles de données Talent avec validation
- Générateur RCD
- TalentService avec CRUD complet
- 16 tests unitaires passants

### ✅ Sprint 2 : Lecture des championnats (Terminé)
- Parser CCH complet pour fichiers complexes
- Modèles Championship (Career, Season, Player, Opponent, TrackStat)
- ChampionshipService pour lecture et listing
- Système de configuration et validation rFactor
- 40 tests unitaires passants

### ✅ Sprint 3 : Création de championnats (Terminé)
- Générateur CCH complet
- CRUD complet pour championnats (create, update, delete, duplicate)
- Round-trip testing validé (parse → generate → parse)
- 49 tests unitaires passants

### ✅ Sprint 4 : Import/Export CSV (Terminé)
- ImportService avec import/export CSV
- Template CSV avec exemples
- Validation avant import (validate_only mode)
- Gestion d'erreurs détaillée avec ImportResult
- Export sélectif ou complet
- Documentation complète (CSV_IMPORT.md)
- 68 tests unitaires passants

### ✅ Sprint 5 : Interface web (Terminé - Consultation complète)
- Application FastAPI complète
- Routes API pour tous les éléments (talents, championnats, véhicules, circuits)
- **Gestion complète des talents** : Liste, Création, Édition, Suppression, Recherche
- **Visualisation complète des championnats** : Liste, Détails enrichis, Suppression, Duplication
- **Gestion des véhicules** : VehicleService, Parser VEH, Liste, Détails, Filtrage
- **Gestion des circuits** : TrackService, Parser GDB, Liste, Détails, Recherche
- Pages web responsive avec Bootstrap
- Notifications toast et overlays de chargement
- 15+ pages HTML complètes
- ~20 endpoints API fonctionnels

**Update 28 Nov 2025** : La création de championnats custom est maintenant COMPLÉTÉE (Sprint 5bis ci-dessous).

## Prochaines étapes

### ✅ Sprint 5bis : Création de Championnats Custom (COMPLÉTÉ - 28 Nov 2025)

**Objectif** : Implémenter la création de championnats via l'interface web

**Status** : ✅ **COMPLÉTÉ** (Code terminé et testé - En attente validation in-game)

**Tâches complétées** :
1. ✅ Modèle RFM (src/models/rfm.py)
2. ✅ Parser RFM (src/parsers/rfm_parser.py)
3. ✅ Générateur RFM (src/generators/rfm_generator.py)
4. ✅ Système d'isolation de véhicules (VehicleIsolationService)
5. ✅ **Système de renommage véhicules avec préfixe** (évite doublons rFactor)
6. ✅ Interface de création (formulaire multi-étapes)
7. ✅ ChampionshipCreatorService
8. ✅ Route API `/api/championships/create`
9. ✅ Tests de génération (championnat "TestChampionship2025")

**Nouvelle fonctionnalité - Renommage Véhicules** :
- Génération préfixe automatique (ex: "TestChampionship" → "TE")
- Renommage fichiers `.veh` (ex: `GRN_08.veh` → `TE_GRN_08.veh`)
- Renommage assets (`.dds`, `.txt`, etc.)
- Modification références (`DefaultLivery`, `Description`, `PitCrewLivery`, `TrackLivery`)
- Les véhicules sont maintenant **uniques** pour rFactor (plus de doublons)

**Documentation** :
- `UPDATE_28NOV2025_VEHICLE_RENAMING.md` - Récapitulatif complet du jour
- `VEHICLE_RENAMING_NOTES.md` - Notes techniques détaillées
- `CLAUDE.md` - Contexte projet mis à jour

**Prochaine étape** :
- [ ] **Test in-game dans rFactor** pour validation finale

---

### Sprint 6 : Packaging et Documentation Utilisateur (PROCHAINE PRIORITÉ)

**Objectif** : Rendre l'application facilement utilisable par les utilisateurs finaux

**Status** : À DÉMARRER

**Tâches prioritaires** :
1. [ ] Script de lancement `.bat` (Windows)
2. [ ] Configuration assistant (premier lancement)
3. [ ] Documentation utilisateur (`USER_GUIDE.md`)
   - Installation
   - Configuration rFactor
   - Création de championnats
   - Dépannage
4. [ ] Tests de compatibilité rFactor
5. [ ] Package PyInstaller (optionnel)

**Estimation** : 3-5h pour version de base

---

### ~~Sprint 5 : Interface web~~ (OBSOLÈTE - Voir ci-dessous)

**Note** : Cette section est conservée pour référence historique. Sprint 5 est maintenant terminé (voir état actuel ci-dessus).

<details>
<summary>Cliquer pour voir les détails historiques du Sprint 5</summary>

#### 5.1 Backend API (FastAPI) ✅ TERMINÉ

**Choix de framework** :
- Option A : **FastAPI** (recommandé)
  - Moderne, rapide, documentation automatique
  - Validation automatique avec Pydantic
  - Support async natif

- Option B : **Flask**
  - Plus simple, bien connu
  - Nombreuses extensions disponibles

**API à implémenter** :

```
Talents:
  GET    /api/talents           - Liste tous les talents
  GET    /api/talents/:name     - Détails d'un talent
  POST   /api/talents           - Créer un talent
  PUT    /api/talents/:name     - Modifier un talent
  DELETE /api/talents/:name     - Supprimer un talent
  GET    /api/talents/search    - Rechercher des talents

Championships:
  GET    /api/championships                - Liste tous les championnats
  GET    /api/championships/:name          - Détails d'un championnat
  POST   /api/championships                - Créer un championnat
  PUT    /api/championships/:name          - Modifier un championnat
  DELETE /api/championships/:name          - Supprimer un championnat
  POST   /api/championships/:name/duplicate - Dupliquer un championnat

Import/Export:
  POST   /api/import/talents    - Importer talents depuis CSV
  GET    /api/export/talents    - Exporter talents vers CSV
  POST   /api/import/validate   - Valider un CSV sans importer
  GET    /api/template/talents  - Télécharger template CSV

Configuration:
  GET    /api/config            - Configuration actuelle
  PUT    /api/config            - Modifier configuration
```

**Structure suggérée** :
```
src/web/
├── __init__.py
├── app.py                  # Application principale
├── routes/
│   ├── __init__.py
│   ├── talents.py          # Routes talents
│   ├── championships.py    # Routes championnats
│   ├── import_export.py    # Routes import/export
│   └── config.py           # Routes configuration
├── schemas/
│   ├── __init__.py
│   ├── talent.py           # Schémas Pydantic pour talents
│   └── championship.py     # Schémas Pydantic pour championnats
└── static/                 # Fichiers statiques (CSS, JS)
    └── uploads/            # Upload temporaire pour CSV
```

#### 5.2 Frontend

**Option A : HTML/CSS/JavaScript vanilla**
- Plus simple, pas de build
- jQuery pour DOM manipulation
- Bootstrap pour UI responsive

**Option B : Framework moderne (Vue.js/React)**
- Meilleure expérience utilisateur
- Nécessite build step

**Pages à créer** :

1. **Dashboard** (`/`)
   - Vue d'ensemble : nombre de championnats, talents
   - Championnats récents
   - Accès rapide aux fonctionnalités

2. **Liste des talents** (`/talents`)
   - Tableau avec recherche/filtres
   - Tri par colonnes
   - Actions : voir, éditer, supprimer
   - Bouton "Nouveau talent"
   - Bouton "Importer CSV"

3. **Détails/Édition talent** (`/talents/:name`)
   - Formulaire avec tous les champs
   - Validation côté client
   - Sauvegarde/Annulation

4. **Liste des championnats** (`/championships`)
   - Tableau avec statut, nombre d'opposants
   - Actions : voir, éditer, supprimer, dupliquer
   - Bouton "Nouveau championnat"

5. **Détails/Édition championnat** (`/championships/:name`)
   - Informations générales
   - Sélection des opposants (depuis liste talents)
   - Configuration des paramètres de course
   - Sauvegarde/Annulation

6. **Import CSV** (`/import`)
   - Upload de fichier
   - Prévisualisation
   - Validation
   - Import avec rapport d'erreurs

7. **Configuration** (`/config`)
   - Chemin rFactor
   - Profil de joueur
   - Validation

**Templates suggérés** (avec Jinja2 si Flask) :
```
templates/
├── base.html               # Template de base
├── dashboard.html
├── talents/
│   ├── list.html
│   └── detail.html
├── championships/
│   ├── list.html
│   └── detail.html
├── import.html
└── config.html
```

#### 5.3 Intégration avec les services existants

Les services existants peuvent être utilisés directement :
```python
# Dans les routes
from src.services.talent_service import TalentService
from src.services.championship_service import ChampionshipService
from src.services.import_service import ImportService
from src.utils.config import get_config

config = get_config()
talent_service = TalentService(config.get_rfactor_path())
championship_service = ChampionshipService(
    config.get_rfactor_path(),
    config.get_current_player()
)
import_service = ImportService(talent_service)
```

#### 5.4 Tâches Sprint 5

- [ ] Choisir framework (FastAPI recommandé)
- [ ] Créer structure `src/web/`
- [ ] Implémenter API REST pour talents
- [ ] Implémenter API REST pour championnats
- [ ] Implémenter API REST pour import/export
- [ ] Créer templates HTML de base
- [ ] Créer page Dashboard
- [ ] Créer pages Talents (liste + détail)
- [ ] Créer pages Championships (liste + détail)
- [ ] Créer page Import CSV
- [ ] Créer page Configuration
- [ ] CSS responsive (Bootstrap)
- [ ] JavaScript pour interactions
- [x] Tests d'intégration API
- [x] Documentation API (auto-générée avec FastAPI)

</details>

---

### Sprint 6 : Déploiement et packaging

**Objectif** : Rendre l'application facilement utilisable

#### 6.1 Script de lancement

**`start.bat` (Windows)** :
```batch
@echo off
title rFactor Championship Creator

echo ============================================
echo rFactor Championship Creator
echo ============================================
echo.

:: Vérifier que Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installe ou n'est pas dans le PATH
    pause
    exit /b 1
)

:: Vérifier la configuration
if not exist config.json (
    echo Configuration initiale...
    python setup_config.py
    if errorlevel 1 (
        echo [ERREUR] Echec de la configuration
        pause
        exit /b 1
    )
)

:: Lancer l'application
echo Demarrage de l'application...
echo.
echo L'application sera accessible a l'adresse:
echo http://localhost:5000
echo.
echo Appuyez sur Ctrl+C pour arreter le serveur
echo.

python -m src.web.app

pause
```

**`start.sh` (Linux/Mac)** :
```bash
#!/bin/bash

echo "============================================"
echo "rFactor Championship Creator"
echo "============================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed"
    exit 1
fi

# Check configuration
if [ ! -f config.json ]; then
    echo "Initial configuration..."
    python3 setup_config.py
fi

# Start application
echo "Starting application..."
echo ""
echo "Application will be accessible at:"
echo "http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python3 -m src.web.app
```

#### 6.2 Package PyInstaller

**Objectif** : Créer un exécutable standalone sans besoin de Python

**`build.py`** :
```python
import PyInstaller.__main__
import sys

# Configuration PyInstaller
PyInstaller.__main__.run([
    'src/web/app.py',
    '--name=RFactorChampionshipCreator',
    '--onefile',
    '--windowed',  # Pas de console
    '--add-data=src/web/templates;templates',
    '--add-data=src/web/static;static',
    '--icon=icon.ico',
    '--clean',
])
```

**Tâches** :
- [ ] Créer `start.bat` et `start.sh`
- [ ] Tester les scripts de lancement
- [ ] Configurer PyInstaller
- [ ] Créer icône application
- [ ] Générer exécutable Windows
- [ ] Générer exécutable Linux (optionnel)
- [ ] Tester exécutable sur machine vierge

#### 6.3 Documentation utilisateur

**`USER_GUIDE.md`** :
- Installation
- Premier lancement
- Configuration rFactor
- Gestion des talents
- Création de championnats
- Import CSV
- Dépannage

**`INSTALL.md`** :
- Prérequis système
- Installation Python (si nécessaire)
- Installation des dépendances
- Configuration initiale

#### 6.4 Package de distribution

**Structure finale** :
```
RFactorChampionshipCreator-v1.0/
├── RFactorChampionshipCreator.exe  # Exécutable (Windows)
├── start.bat                        # Script de lancement (version Python)
├── setup_config.py
├── config.json.example
├── README.md
├── USER_GUIDE.md
├── INSTALL.md
├── LICENSE
└── requirements.txt                 # Si version Python
```

**Tâches** :
- [ ] Rédiger USER_GUIDE.md
- [ ] Rédiger INSTALL.md
- [ ] Créer README.md utilisateur (différent du README développeur)
- [ ] Choisir licence
- [ ] Créer archive ZIP pour distribution
- [ ] Créer releases GitHub

## Fonctionnalités optionnelles futures

### Post-v1.0

1. **Gestion des véhicules**
   - Parser VEH
   - VehicleService
   - Interface web pour véhicules

2. **Gestion des circuits**
   - Parser GDB
   - TrackService
   - Interface web pour circuits

3. **Calendrier de championnat**
   - Sélection et ordre des circuits
   - Configuration par course

4. **Statistiques avancées**
   - Graphiques de performance
   - Historique des championnats
   - Comparaison de talents

5. **Multi-joueurs**
   - Gestion de plusieurs profils joueurs
   - Switch rapide entre profils

6. **Thèmes**
   - Dark mode
   - Personnalisation UI

7. **Export avancé**
   - Export PDF des championnats
   - Export Excel des statistiques

8. **Backup/Restore**
   - Sauvegarde automatique
   - Restauration de championnats

## Tests requis

### Tests unitaires
- [x] Parsers (68 tests actuels)
- [x] Générateurs
- [x] Services
- [ ] Routes API (Sprint 5)

### Tests d'intégration
- [ ] API endpoints
- [ ] Import/Export workflow complet
- [ ] CRUD complet championnats

### Tests end-to-end
- [ ] Parcours utilisateur complet
- [ ] Création championnat from scratch
- [ ] Import CSV → Création championnat

### Tests de compatibilité
- [ ] Tester avec différentes versions rFactor
- [ ] Tester sur Windows 10/11
- [ ] Tester fichiers de différents mods

## Priorités

**Haute priorité** :
1. Sprint 5 - Interface web (fonctionnalités de base)
2. Sprint 6 - Script de lancement et documentation

**Moyenne priorité** :
1. Package PyInstaller
2. Tests d'intégration

**Basse priorité** :
1. Fonctionnalités optionnelles post-v1.0
2. Support Linux/Mac

## Notes techniques

### Performances
- Les services actuels chargent les fichiers à chaque appel
- Pour la web app, considérer :
  - Cache en mémoire pour talents fréquemment accédés
  - Pagination pour listes longues
  - Lazy loading des détails

### Sécurité
- Valider tous les inputs utilisateur
- Sanitizer les noms de fichiers
- Limiter taille des uploads CSV
- CSRF protection pour formulaires

### UX
- Loading indicators pour opérations longues
- Messages de confirmation avant suppression
- Toast notifications pour succès/erreurs
- Breadcrumbs pour navigation

---

**Prêt pour Sprint 5 !** L'infrastructure backend est solide, il est temps de créer l'interface utilisateur.
