# Changelog

Toutes les modifications notables de ce projet seront documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/lang/fr/).

---

## [1.3.3] - 2025-12-14

### 🎯 Amélioration Majeure du Randomizer

#### Import CSV avec Gestion des Doublons et Auto-Fill
- **Gestion intelligente des doublons** :
  - Par défaut (`overwrite_existing=True`), les talents existants sont **écrasés** avec les données du CSV
  - Les talents écrasés génèrent un **warning** (pas une erreur)
  - Nouveau compteur `overwrite_count` dans les résultats d'import
- **Auto-completion des champs manquants** :
  - Paramètre `fill_missing=True` (par défaut) utilise le randomizer modulaire
  - Permet d'importer un CSV avec **seulement les noms** des pilotes
  - Tous les champs vides sont générés automatiquement de façon cohérente
  - Exemple : CSV avec `name,nationality` → Les stats, date, carrière sont générées automatiquement
- **Structure du résultat d'import** :
  - `success_count` : Nombre de talents importés avec succès
  - `overwrite_count` : Nombre de talents existants écrasés
  - `error_count` : Nombre d'erreurs fatales
  - `errors` : Liste des erreurs (ligne, nom, message)
  - `warnings` : Liste des avertissements (ligne, nom, message)

### 🎯 Amélioration Majeure du Randomizer

#### Randomizer d'Interface (Bouton "Régénérer")
- **Ne randomise PLUS que les statistiques de course** (9 stats)
  - speed, crash, aggression, reputation, courtesy, composure, recovery, completed_laps, min_racing_skill
  - **Préserve TOUT le reste** : nom, nationalité, date de naissance, départs, poles, victoires, championnats
- **Comportement corrigé** :
  - Créer un talent : randomise les stats au chargement
  - Bouton "Régénérer" : ne change QUE les stats de course
  - Plus de perte de données lors de la régénération

#### Randomizer Modulaire (pour CSV Import - futur)
- **Nouvelle fonction `random_field(field_name)`** - Randomise un champ spécifique
  - Supporte tous les champs : nationality, date_of_birth, starts, poles, wins, drivers_championships, + 9 stats
  - Utilise le contexte pour cohérence (ex: poles basés sur starts)
- **Nouvelle fonction `fill_missing_fields(data)`** - Remplit les champs manquants
  - Parfait pour l'import CSV : laisse seulement le nom, tout le reste est généré intelligemment
  - Génère des valeurs cohérentes entre elles

#### API
- **Endpoint modifié** : `GET /api/talents/random-stats/`
  - Retourne maintenant `{"stats": {...}}` au lieu de `{"personal_info": {...}, "stats": {...}}`
  - Ne génère plus les infos personnelles

#### Frontend
- **TalentCreate.jsx** et **TalentEdit.jsx** mis à jour
  - Ne mettent à jour que les stats de course lors de la régénération
  - Préservent toutes les informations personnelles et de carrière

### 📚 Documentation
- Docstrings complètes dans `talent_randomizer.py`
- Commentaires explicites sur le comportement de chaque fonction

---

## [1.3.2] - 2025-12-14

### 🐛 Corrections Critiques

#### ChampionshipService
- **Correction du crash au chargement des championnats** quand `current_player` n'est pas configuré
  - `TypeError: unsupported operand type(s) for /: 'WindowsPath' and 'NoneType'` corrigé
  - Le service détecte maintenant automatiquement le premier joueur disponible
  - Si aucun joueur n'existe, crée automatiquement un profil "DefaultPlayer"
  - Permet à l'application de fonctionner immédiatement après installation

#### Fichier de Configuration
- **`config.template.json` corrigé** pour inclure tous les champs nécessaires
  - Ajout de `current_player: null` (sera auto-détecté)
  - Ajout de `last_championship: null`
  - Ajout de `recent_championships: []`
  - Instructions d'utilisation clarifiées dans le fichier
  - Évite les erreurs au premier lancement de la distribution

### 🔧 Améliorations

#### Robustesse
- Le paramètre `player_name` de `ChampionshipService.__init__()` est maintenant optionnel
- Méthode `_get_or_create_default_player()` ajoutée pour fallback automatique
- L'application fonctionne même sans configuration de joueur explicite
- Template de configuration complet et cohérent avec le code

---

## [1.3.1] - 2025-12-14

### 🐛 Corrections de Bugs

#### Formulaires Talents
- **Préservation de la date de naissance** lors de la régénération des statistiques
  - Le bouton "🎲 Régénérer" conserve maintenant la date existante
  - Évite la perte de données lors de la régénération
- **Lisibilité du champ nationalité** corrigée
  - Ajout de la couleur `dark-secondary` (#1A1A1A) dans Tailwind config
  - Meilleur contraste texte blanc sur fond sombre

#### Assets et Ressources
- **Création du favicon** `trophy.svg` (404 corrigé)
  - Design de trophée avec gradients thème racing
  - Couleurs: jaune fluo (#FFE700) et rouge racing (#E31E24)

### 🔧 Améliorations Techniques

#### Gestion des Versions
- **Centralisation du numéro de version** dans `src/__version__.py`
  - Source unique de vérité pour toute l'application
  - Import dynamique dans `src/web/app.py`
- **Script de synchronisation** `scripts/sync_version.py`
  - Synchronise automatiquement la version dans tous les fichiers
  - Met à jour: `pyproject.toml`, `package.json`, `README.md`, `CLAUDE.md`, `SCRIPTS_GUIDE.md`
  - Usage: `uv run python scripts/sync_version.py`
- **Mise à jour de tous les fichiers** à version 1.3.1

### 📚 Documentation
- Mise à jour des numéros de version dans toute la documentation
- Date mise à jour: 14 Décembre 2025

---

## [1.3.0] - 2025-12-13

### 🎉 Améliorations Majeures UX et Recherche

Cette version apporte des améliorations significatives à l'expérience utilisateur et aux fonctionnalités de recherche.

### ✨ Ajouté

#### Randomisation des Talents
- **Module TalentRandomizer** pour génération aléatoire de statistiques cohérentes
- Endpoint API `/api/talents/random-stats/` pour obtenir des valeurs aléatoires
- Génération intelligente avec relations entre stats :
  - Speed et composure corrélés avec niveau global
  - Crash inversement proportionnel à la compétence
  - Réputation basée sur victoires et championnats
  - Historique de carrière réaliste (départs, poles, victoires)
- **22 nationalités** disponibles
- **Bouton "🎲 Régénérer"** dans le formulaire de création/édition
- **Chargement automatique** de valeurs aléatoires à la création d'un talent
- **Pop-up de confirmation** en mode édition pour éviter pertes de données

#### Améliorations Formulaire Talents
- **Input de type date** avec date picker natif (au lieu de texte)
- **Conversion automatique** entre formats :
  - rFactor : `DD-MM-YYYY` (ex: `15-3-1990`)
  - HTML5 : `YYYY-MM-DD` (ex: `1990-03-15`)
- **Liste déroulante nationalités** avec autocomplétion (`<datalist>`)
- Endpoint `/api/talents/nationalities/` pour obtenir les nationalités
- Option `?from_existing=true` pour utiliser les nationalités des talents existants
- Placeholder et indication améliorés pour meilleure UX

#### Recherche Multi-Champs Avancée

##### Talents (`/api/talents/search/`)
- **Recherche textuelle configurables** :
  - `search_name` - Recherche dans le nom (défaut: true)
  - `search_nationality` - Recherche dans la nationalité (défaut: true)
- **Filtres numériques** :
  - `min_speed` / `max_speed` - Filtrage par vitesse
  - `min_aggression` / `max_aggression` - Filtrage par agressivité
- Exemple : `/api/talents/search/?q=american&min_speed=75&max_speed=95`

##### Véhicules (`/api/vehicles/`)
- **Recherche multi-champs** :
  - `search_driver` - Dans nom du pilote (défaut: true)
  - `search_team` - Dans nom de l'équipe (défaut: true)
  - `search_description` - Dans description (défaut: true)
- Tous les champs activables individuellement
- Exemple : `/api/vehicles/?search=yellow&search_driver=true&search_team=false`

##### Circuits (`/api/tracks/`)
- **Recherche multi-champs** :
  - `search_track_name` - Dans nom du circuit (défaut: true)
  - `search_venue_name` - Dans nom du lieu (défaut: true)
  - `search_layout` - Dans variante (défaut: true)
  - `search_file_name` - Dans nom de fichier (défaut: true)
- Tous les champs activables individuellement
- Exemple : `/api/tracks/?search=long&search_layout=true&search_file_name=false`

#### Sauvegarde de Session pour Création de Championnat
- **Module ChampionshipSessionManager** (`championship-session.js`)
- **Sauvegarde automatique** dans `localStorage` du navigateur
- Tracking complet de l'état :
  - Nom et nom complet du championnat
  - Véhicules sélectionnés
  - Assignations pilotes ↔ véhicules
  - Circuits sélectionnés et ordre
  - Étape actuelle (1-5)
  - Timestamp de dernière modification
- **Restauration automatique** avec dialogue de confirmation :
  - Pop-up informative au chargement
  - Affiche : nom, âge du brouillon, étape, véhicules, circuits
  - Options : "Reprendre" ou "Recommencer"
- **Navigation améliorée** :
  - Boutons "Précédent" sur toutes les étapes (2-5)
  - Bouton "Abandonner" sur toutes les étapes avec confirmation
  - Impossible de perdre ses données en cours de création
- **Effacement automatique** quand le championnat est créé avec succès

#### Widget de Reprise sur Dashboard
- **Affichage conditionnel** : visible uniquement si brouillon existe
- **Informations complètes** :
  - Nom du championnat en cours
  - Âge du brouillon formaté ("Il y a 2 heures", "Il y a 15 minutes")
  - Étape actuelle (ex: "Étape 3/5")
  - Nombre de véhicules sélectionnés
  - Nombre de circuits sélectionnés
- **Actions rapides** :
  - Bouton "Reprendre" → Retour au formulaire avec toutes les données
  - Bouton "Abandonner" → Suppression avec confirmation
- Design cohérent avec le thème racing

### 🔧 Modifié

#### Backend
- **TalentService** : Recherche multi-champs avec filtres numériques
- **VehicleService** : Support recherche configurables par champ
- **TrackService** : Support recherche configurables par champ
- **GDBParser** : Méthode `search()` étendue avec paramètres de champs

#### Frontend
- **Formulaire création talents** : UX considérablement améliorée
- **Formulaire création championnat** : Navigation bidirectionnelle complète
- **Dashboard** : Widget de reprise de championnat

### 🚀 Workflow Utilisateur Amélioré

#### Scénario 1 : Création de championnat normale
1. Commence la création → Rempli étape 1
2. Passe à l'étape 2 → **Sauvegarde auto**
3. Continue normalement → **Sauvegarde à chaque étape**
4. Finalise → **Brouillon effacé automatiquement**

#### Scénario 2 : Interruption puis reprise
1. Commence la création → Arrive à l'étape 3
2. Ferme le navigateur / quitte la page
3. Revient plus tard → **Pop-up de confirmation au chargement**
4. Choisit "Reprendre" → **Retour direct à l'étape 3 avec toutes les données**

#### Scénario 3 : Visualisation depuis le dashboard
1. Va sur le dashboard
2. Voit le widget avec toutes les infos du brouillon
3. Clique sur "Reprendre" → **Reprend là où il s'était arrêté**

### 📦 Fichiers Modifiés

#### Backend
- `src/web/routes/talents.py` - Recherche avancée + nationalités + random stats
- `src/web/routes/vehicles.py` - Recherche multi-champs
- `src/web/routes/tracks.py` - Recherche multi-champs
- `src/parsers/gdb_parser.py` - Support multi-champs
- `src/services/track_service.py` - Support multi-champs
- `src/utils/talent_randomizer.py` - **NOUVEAU** - Générateur aléatoire

#### Frontend
- `src/web/static/js/championship-session.js` - **NOUVEAU** - Gestionnaire de session
- `src/web/templates/talents/form.html` - Randomisation + date + nationalités
- `src/web/templates/championships/create.html` - Intégration session + navigation
- `src/web/templates/dashboard.html` - Widget de reprise

### 📚 Documentation
- `CHANGELOG.md` - Cette version

### 🎯 Impact

Ces améliorations transforment l'expérience utilisateur :
- **Création de talents** : Plus rapide et plus intuitive (randomisation)
- **Recherche** : Plus puissante et flexible (multi-champs)
- **Création de championnats** : Sans risque de perte de données (sauvegarde session)
- **Navigation** : Fluide avec retours possibles
- **Dashboard** : Vue d'ensemble avec reprise facile

---

## [1.0.0] - 2025-11-28

### 🎉 Version Initiale Complète

Première version fonctionnelle complète de rFactor Championship Creator avec toutes les fonctionnalités de base.

### ✨ Ajouté

#### Gestion des Talents
- Parser et générateur pour fichiers `.rcd`
- CRUD complet (Create, Read, Update, Delete)
- Recherche de talents par nom
- Validation des statistiques (0-100)
- Interface web complète

#### Gestion des Championnats
- Parser pour fichiers `.cch` (progression joueur)
- Parser et générateur pour fichiers `.rfm` (définition championnat)
- Lecture de championnats existants
- Duplication de championnats
- Suppression de championnats
- Détails enrichis (opposants, circuits, statistiques)
- Interface web complète

#### Création de Championnats Custom
- **Service ChampionshipCreatorService**
- **Service VehicleIsolationService**
- **Système de renommage véhicules avec préfixe** (résout problème doublons rFactor)
- Sélection de véhicules originaux
- Association pilotes ↔ véhicules
- Sélection et ordre des circuits
- Génération automatique `.rfm`
- Isolation complète des véhicules dans `RFTOOL_<Name>/`
- Interface web formulaire multi-étapes

#### Gestion des Véhicules
- Parser pour fichiers `.veh`
- VehicleService avec cache
- Liste, filtrage par classe/fabricant
- Recherche de véhicules
- Interface web complète

#### Gestion des Circuits
- Parser pour fichiers `.gdb`
- TrackService
- Liste et recherche de circuits
- Interface web complète

#### Import/Export CSV
- Template CSV avec exemples
- Import avec validation
- Option "skip existing" ou "overwrite"
- Export complet ou sélectif
- Rapport d'erreurs détaillé
- Interface web d'import

#### Système de Configuration
- RFactorValidator (validation installation)
- Config Manager (gestion `config.json`)
- Script de configuration guidé (`setup_config.py`)
- Détection automatique de rFactor
- Gestion des profils joueurs

#### Interface Web (FastAPI)
- Dashboard avec statistiques
- Pages de gestion talents
- Pages de gestion championnats
- Pages de gestion véhicules
- Pages de gestion circuits
- Page d'import CSV
- Page de configuration
- Formulaire de création de championnats
- **20+ endpoints API** RESTful
- **15+ pages HTML** avec Bootstrap
- Documentation API automatique (Swagger/ReDoc)

#### Tests
- **68 tests unitaires** passants
- Tests parsers (RCD, CCH, RFM, VEH, GDB)
- Tests générateurs (RCD, CCH, RFM)
- Tests services
- Tests utilities (Config, RFactorValidator)
- Couverture complète des fonctionnalités critiques

### 🔧 Détails Techniques

#### Parsers
- `RCDParser` - Talents (.rcd)
- `CCHParser` - Championships progression (.cch)
- `RFMParser` - Championships définition (.rfm)
- `VEHParser` - Vehicles (.veh)
- `GDBParser` - Tracks (.gdb)
- Encodage Windows-1252 pour tous

#### Générateurs
- `RCDGenerator` - Génération .rcd
- `CCHGenerator` - Génération .cch
- `RFMGenerator` - Génération .rfm
- Validation complète avant génération

#### Services
- `TalentService` - CRUD talents
- `ChampionshipService` - Lecture championnats
- `ChampionshipCreatorService` - Création championnats custom
- `VehicleIsolationService` - Isolation + renommage véhicules
- `VehicleService` - Gestion véhicules avec cache
- `TrackService` - Gestion circuits
- `ImportService` - Import/Export CSV

#### Modèles (Pydantic)
- `Talent`, `TalentPersonalInfo`, `TalentStats`
- `Championship`, `Season`, `Player`, `Opponent`, `TrackStat`
- `RFM`, `RFMSeason`, `RFMRace`
- `Vehicle`, `VehicleTeamInfo`, `VehicleConfig`
- `Track`

### 🚀 Système de Renommage Véhicules

**Problème résolu** : rFactor détectait les véhicules isolés comme doublons des originaux.

**Solution** :
- Génération automatique de préfixe court (2-3 lettres)
  - Ex: "TestChampionship2025" → "TE"
- Renommage fichiers `.veh` : `GRN_08.veh` → `TE_GRN_08.veh`
- Renommage assets : `.dds`, `.tga`, `.bmp`, `.txt`
- Modification références dans le `.veh` :
  - `Description` - Ajout préfixe
  - `DefaultLivery` - Nouveau nom avec préfixe
  - `PitCrewLivery` - Nouveau nom avec préfixe
  - `TrackLivery` - Nouveau nom avec préfixe (multi-lignes)
  - `Classes` - Nom du championnat
  - `Driver` - Nom du pilote assigné

**Résultat** : Les véhicules sont maintenant détectés comme uniques par rFactor.

### 📦 Structure du Projet

```
RFactorChampionshipCreator/
├── src/
│   ├── parsers/       # 5 parsers
│   ├── generators/    # 3 générateurs
│   ├── models/        # 5 modèles
│   ├── services/      # 7 services
│   ├── web/          # Application FastAPI
│   └── utils/        # Utilitaires
├── tests/            # 68 tests
├── docs/             # Documentation
├── config.json       # Configuration
├── requirements.txt
└── start.bat
```

### 📚 Documentation

- `README.md` - Présentation générale
- `USER_GUIDE.md` - Guide utilisateur complet
- `DEVELOPER_GUIDE.md` - Guide développeur
- `SPECIFICATIONS.md` - Spécifications techniques
- `FILE_FORMATS.md` - Formats fichiers rFactor
- `CHANGELOG.md` - Ce fichier
- `CLAUDE.md` - Contexte développement

### 🎯 Conventions

- Code en **anglais**
- Commentaires en **français** si nécessaire
- Type hints Python systématiques
- Validation Pydantic partout
- Tests unitaires pour fonctions critiques
- Encodage **Windows-1252** pour fichiers rFactor
- **JAMAIS** modifier les fichiers originaux rFactor

### ⚠️ Points d'Attention

- Les fichiers `.cch` sont générés par rFactor, pas par l'outil
- Les fichiers `.rfm` sont créés par l'outil
- Système de préfixe `RFTOOL_` pour tous les championnats custom
- Isolation complète des véhicules par championnat
- Validation de l'installation rFactor avant utilisation

---

## [0.5.0] - 2025-11-26 (Sprint 5)

### ✨ Ajouté

- Interface web FastAPI complète
- Routes API pour talents, championnats, véhicules, circuits
- Pages HTML avec Bootstrap
- Formulaires de création/édition talents
- Import/Export CSV via interface web
- Documentation API automatique

### 🔧 Modifié

- Services adaptés pour utilisation web
- Ajout de schémas Pydantic pour validation API

---

## [0.4.0] - 2025-11-26 (Sprint 4)

### ✨ Ajouté

- ImportService pour import/export CSV
- Template CSV avec exemples
- Validation avant import
- Rapport d'erreurs détaillé
- Options skip_existing et validate_only
- Export sélectif ou complet

### 📝 Documentation

- `CSV_IMPORT.md` - Documentation complète import/export

---

## [0.3.0] - 2025-11-26 (Sprint 3)

### ✨ Ajouté

- CCHGenerator pour génération championnats
- CRUD complet pour championnats
- Duplication de championnats
- Round-trip testing (parse → generate → parse)

### 🔧 Modifié

- ChampionshipService étendu avec create/update/delete

---

## [0.2.0] - 2025-11-26 (Sprint 2)

### ✨ Ajouté

- CCHParser pour lecture championnats
- Modèles Championship (Career, Season, Player, Opponent, TrackStat)
- ChampionshipService pour lecture et listing
- Système de configuration (Config, RFactorValidator)
- Script setup_config.py

### 📝 Documentation

- `CONFIGURATION.md` - Documentation système configuration

---

## [0.1.0] - 2025-11-26 (Sprint 1)

### ✨ Ajouté - Première Version

- RCDParser pour lecture talents
- RCDGenerator pour génération talents
- Modèles Talent (Talent, TalentPersonalInfo, TalentStats)
- TalentService avec CRUD complet
- 16 tests unitaires

### 📝 Documentation

- `SPECIFICATIONS.md` - Spécifications initiales
- `FILE_FORMATS.md` - Documentation formats fichiers
- `ANALYSIS_SUMMARY.md` - Analyse initiale

---

## Types de Changements

- ✨ **Ajouté** : Nouvelles fonctionnalités
- 🔧 **Modifié** : Changements de fonctionnalités existantes
- 🐛 **Corrigé** : Corrections de bugs
- 🗑️ **Supprimé** : Fonctionnalités retirées
- 🔒 **Sécurité** : Corrections de vulnérabilités
- 📝 **Documentation** : Changements de documentation
- 🚀 **Performance** : Améliorations de performance

---

## Prochaines Versions

### [1.1.0] - À venir

#### Planifié

- Package PyInstaller (exécutable standalone)
- Script de lancement `.bat` amélioré
- Tests in-game rFactor (validation complète)
- Gestion des conflits de préfixe véhicules
- Option préfixe personnalisé

#### En Réflexion

- Support multi-joueurs
- Statistiques avancées avec graphiques
- Export PDF des championnats
- Backup/Restore automatique
- Mode sombre (dark mode)

---

**Projet** : rFactor Championship Creator
**Mainteneur** : @vallloic
**Licence** : À définir
