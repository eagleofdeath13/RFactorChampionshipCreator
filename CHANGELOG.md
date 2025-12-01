# Changelog

Toutes les modifications notables de ce projet seront documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/lang/fr/).

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
