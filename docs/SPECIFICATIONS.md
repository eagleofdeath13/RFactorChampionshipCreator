# rFactor Championship Creator - Spécifications du Projet

## Vue d'ensemble

Ce projet vise à créer un éditeur de championnats personnalisés pour le jeu rFactor. L'application permettra de gérer, créer et modifier des championnats de manière intuitive via une interface web.

## 🎯 Découvertes Majeures

### Architecture des Championnats rFactor

Un championnat rFactor nécessite **DEUX** types de fichiers :

1. **`.rfm`** (RFactor Mod) - Définit le championnat
   - Localisation : `rFactor/rFm/`
   - Contient : Saisons, circuits, règles, filtres véhicules
   - **Créé manuellement** ou par l'outil

2. **`.cch`** (Career Championship) - Stocke la progression
   - Localisation : `rFactor/UserData/<Player>/`
   - Contient : Points, positions, historique
   - **Généré automatiquement** par rFactor au lancement

### Système d'Isolation des Véhicules

Pour éviter de modifier les fichiers originaux, nous utilisons un système d'isolation :

```
GameData/Vehicles/
├── RHEZ/              # Véhicules originaux (ne pas toucher)
└── RFTOOL_<ChampionshipName>/  # Véhicules isolés pour le championnat
    └── [structure copiée depuis l'original]
```

**Avantages** :
- Pas de modification des fichiers originaux
- Chaque championnat est indépendant
- Facile à supprimer (1 dossier = 1 championnat)
- Évite les conflits entre championnats

## Objectifs principaux

### ✅ Phase 1 : Analyse et compréhension des fichiers rFactor (COMPLÉTÉE)
- [x] Analyser la structure du fichier `.cch`
- [x] Analyser la structure du fichier `.rfm`
- [x] Identifier les différents éléments :
  - [x] Pilotes (Talents - `.rcd`)
  - [x] Voitures (`.veh`)
  - [x] Circuits (`.gdb`)
  - [x] Options de championnat
- [x] Documenter le format et la structure des fichiers
- [x] Identifier les fichiers associés

### ✅ Phase 2 : Moteur de gestion des fichiers de base (COMPLÉTÉE)
- [x] Parser pour les fichiers `.rcd` (Talents)
- [x] Parser pour les fichiers `.cch` (Championship)
- [x] Parser pour les fichiers `.veh` (Vehicles)
- [x] Parser pour les fichiers `.gdb` (Tracks)
- [x] Générateurs pour `.rcd` et `.cch`
- [x] Modèles de données Python
- [x] Validation de la compatibilité avec rFactor

### 🔄 Phase 2bis : Gestion des fichiers `.rfm` (EN COURS)
- [ ] Analyser et documenter complètement le format `.rfm`
- [ ] Créer le modèle de données pour `.rfm`
- [ ] Implémenter le parser `.rfm`
- [ ] Implémenter le générateur `.rfm`
- [ ] Valider la compatibilité avec rFactor

### ✅ Phase 3 : Gestion des éléments du championnat (COMPLÉTÉE)
- [x] Module de gestion des pilotes (Talents)
  - [x] Lecture des talents existants
  - [x] Création de nouveaux talents
  - [x] Modification des talents
- [x] Module de gestion des voitures
  - [x] Liste des voitures disponibles
  - [x] Filtrage par classe, fabricant
- [x] Module de gestion des circuits
  - [x] Liste des circuits disponibles
  - [x] Recherche de circuits
- [x] Module de gestion des championnats
  - [x] Lecture des championnats existants
  - [x] Duplication de championnats

### ✅ Phase 4 : Import/Export de données (COMPLÉTÉE)
- [x] Implémentation de l'import CSV pour les pilotes
- [x] Export CSV des pilotes
- [x] Validation des données importées

### 🔄 Phase 5 : Interface utilisateur web (EN COURS)
- [x] Développement de l'interface web (FastAPI)
- [x] Pages de gestion de base :
  - [x] Liste des championnats
  - [x] Liste des pilotes
  - [x] Liste des véhicules
  - [x] Liste des circuits
  - [x] Import/Export
- [ ] Pages de création de championnat
  - [ ] Informations de base
  - [ ] Sélection des véhicules
  - [ ] Association pilotes-véhicules
  - [ ] Sélection et ordre des circuits
  - [ ] Configuration des options
- [ ] Interface responsive et intuitive

### 📋 Phase 5bis : Création de Championnats Custom (NOUVEAU)
- [ ] Système de préfixe pour championnats custom
  - [ ] Préfixe global : `RFTOOL_`
  - [ ] Génération de catégorie unique par championnat
- [ ] Isolation et copie de véhicules
  - [ ] Copie de fichiers `.veh` + assets
  - [ ] Modification des classes de véhicules
  - [ ] Préservation de la structure des dossiers
- [ ] Association pilote-véhicule
  - [ ] Interface de sélection pilote/voiture
  - [ ] Modification du champ `Driver` dans `.veh`
  - [ ] Gestion des RCDFile
- [ ] Génération du fichier `.rfm` complet
  - [ ] Définition des saisons
  - [ ] Configuration des filtres
  - [ ] Liste ordonnée des circuits (SceneOrder)
  - [ ] Système de points personnalisable

### Phase 6 : Portabilité et déploiement
- [ ] Création d'un fichier `.bat` pour le lancement
- [ ] Package auto-exécutable (PyInstaller)
- [ ] Documentation utilisateur

## Architecture technique

### Stack technologique
- **Backend** : Python 3.x
- **Framework web** : FastAPI
- **Frontend** : HTML/CSS/JavaScript + Jinja2 templates
- **Validation** : Pydantic
- **Testing** : Pytest
- **Packaging** : PyInstaller (futur)

### Structure du projet
```
RFactorChampionshipCreator/
├── src/
│   ├── parsers/              # Parsers pour fichiers rFactor
│   │   ├── rcd_parser.py     # ✅ Talents
│   │   ├── cch_parser.py     # ✅ Championships
│   │   ├── veh_parser.py     # ✅ Vehicles
│   │   ├── gdb_parser.py     # ✅ Tracks
│   │   └── rfm_parser.py     # 🔄 RFactor Mods (TODO)
│   ├── generators/           # Générateurs de fichiers
│   │   ├── rcd_generator.py  # ✅ Talents
│   │   ├── cch_generator.py  # ✅ Championships
│   │   └── rfm_generator.py  # 🔄 RFactor Mods (TODO)
│   ├── models/               # Modèles de données
│   │   ├── talent.py         # ✅ Talent, TalentPersonalInfo, TalentStats
│   │   ├── championship.py   # ✅ Championship, Season, Player, Opponent
│   │   ├── vehicle.py        # ✅ Vehicle, VehicleTeamInfo, VehicleConfig
│   │   ├── track.py          # ✅ Track
│   │   └── rfm.py            # 🔄 RFM models (TODO)
│   ├── services/             # Logique métier
│   │   ├── talent_service.py         # ✅ Gestion talents
│   │   ├── championship_service.py   # ✅ Gestion championnats
│   │   ├── vehicle_service.py        # ✅ Gestion véhicules
│   │   ├── track_service.py          # ✅ Gestion circuits
│   │   ├── import_service.py         # ✅ Import/Export CSV
│   │   └── championship_creator.py   # 🔄 Création championnats (TODO)
│   ├── web/                  # Interface web
│   │   ├── app.py            # ✅ Application FastAPI
│   │   ├── routes/           # ✅ Routes API
│   │   ├── schemas/          # ✅ Schémas Pydantic
│   │   ├── templates/        # Templates HTML
│   │   └── static/           # CSS, JS
│   └── utils/                # Utilitaires
│       ├── file_utils.py     # ✅ Gestion fichiers
│       ├── config.py         # ✅ Configuration
│       └── rfactor_validator.py  # ✅ Validation rFactor
├── tests/                    # Tests unitaires
├── RFactorFiles/             # Fichiers de référence
├── requirements.txt          # ✅ Dépendances
├── SPECIFICATIONS.md         # Ce fichier
├── CLAUDE.md                 # Contexte pour Claude
└── README.md                 # Documentation utilisateur
```

## Fichiers rFactor - Format documenté

### 1. Fichiers `.rfm` (RFactor Mod)
**Localisation** : `rFactor/rFm/`
**Encodage** : UTF-8 ou Windows-1252

**Structure** :
```rfm
// Game/Season Info
Mod Name = My Championship
Track Filter = *
Vehicle Filter = CustomCategory
SafetyCar = car.veh

Max Opponents = 19
Min Championship Opponents = 3

// Season Definition
Season = Season Name
{
  Vehicle Filter = CustomCategory
  Min Championship Opponents = 5
  MinExperience = 0        // Optionnel
  EntryFee = 0            // Optionnel

  SceneOrder              // OBLIGATOIRE : Liste des circuits
  {
    Track1_Name
    Track2_Name
  }
}

// Scoring
DefaultScoring { ... }
SeasonScoringInfo { ... }
SceneOrder { ... }        // Ordre global par défaut
PitGroupOrder { ... }
```

### 2. Fichiers `.cch` (Career Championship)
**Localisation** : `rFactor/UserData/<Player>/`
**Encodage** : Windows-1252
**Généré automatiquement** par rFactor

### 3. Fichiers `.rcd` (Talent/Driver)
**Localisation** : `rFactor/GameData/Talent/`
**Encodage** : Windows-1252

### 4. Fichiers `.veh` (Vehicle)
**Localisation** : `rFactor/GameData/Vehicles/`
**Encodage** : Windows-1252

**Champs modifiables pour isolation** :
- `Classes` : Liste des catégories (pour filtrage)
- `Driver` : Nom du pilote assigné

### 5. Fichiers `.gdb` (Track)
**Localisation** : `rFactor/GameData/Locations/`
**Encodage** : Windows-1252

## Workflow de Création de Championnat

### 1. Informations de Base
```python
championship = {
    "name": "MyChampionship2025",          # Nom unique
    "full_name": "My Custom Championship",  # Nom complet
    "description": "...",
    "prefix": "RFTOOL_MyChampionship2025",  # Auto-généré
}
```

### 2. Sélection et Isolation des Véhicules
Pour chaque véhicule sélectionné :
1. **Copier** le `.veh` + assets dans `RFTOOL_<Name>/`
2. **Modifier** `Classes="MyChampionship2025 ..."`
3. **Assigner** un pilote : `Driver="John Doe"`

### 3. Génération du `.rfm`
```python
# Créer rFactor/rFm/RFTOOL_MyChampionship2025.rfm
rfm_content = {
    "mod_name": "MyChampionship2025",
    "vehicle_filter": "MyChampionship2025",  # Filtre unique
    "seasons": [
        {
            "name": "Season 1",
            "vehicle_filter": "MyChampionship2025",
            "tracks": ["Mills_Short", "Toban_Long"],  # SceneOrder
        }
    ],
    "scoring": {...},
}
```

### 4. Le joueur lance rFactor
→ Le fichier `.cch` est créé automatiquement

## Système de Préfixe pour Championnats Custom

### Convention de nommage
- **Préfixe global** : `RFTOOL_` (identifie les championnats de l'outil)
- **Nom du championnat** : Choisi par l'utilisateur
- **Nom complet** : `RFTOOL_<ChampionshipName>`

### Structure des fichiers
```
rFactor/
├── rFm/
│   └── RFTOOL_MyChampionship2025.rfm
└── GameData/Vehicles/
    └── RFTOOL_MyChampionship2025/
        ├── [Structure copiée des originaux]
        └── *.veh (avec Classes modifiées)
```

### Filtrage des véhicules
- **Originaux** : Tous sauf ceux commençant par `RFTOOL_`
- **Custom** : Ceux commençant par `RFTOOL_`
- **Par championnat** : `RFTOOL_<ChampionshipName>`

## Fonctionnalités détaillées

### Gestion des championnats
- ✅ Lister les championnats existants
- ✅ Lire un championnat (.cch)
- ✅ Dupliquer un championnat
- 🔄 **Créer un nouveau championnat custom (.rfm)**
- 🔄 Éditer un championnat custom
- 🔄 Supprimer un championnat custom

### Gestion des pilotes (Talents)
- ✅ Lister tous les pilotes disponibles
- ✅ Créer un nouveau pilote
- ✅ Modifier un pilote existant
- ✅ Importer une liste de pilotes depuis CSV
- ✅ Exporter des pilotes en CSV
- 🔄 Assigner des pilotes à des véhicules

### Gestion des voitures
- ✅ Lister toutes les voitures disponibles
- ✅ Filtrer par classe, fabricant
- ✅ Recherche de véhicules
- 🔄 Copier/Isoler des véhicules pour un championnat
- 🔄 Modifier les classes d'un véhicule
- 🔄 Assigner un pilote à un véhicule

### Gestion des circuits
- ✅ Lister tous les circuits disponibles
- ✅ Recherche de circuits
- 🔄 Sélectionner et ordonner les circuits pour un championnat

### Options de championnat
- 🔄 Nombre de courses
- 🔄 Système de points personnalisable
- 🔄 Difficulté IA
- 🔄 Conditions météo
- 🔄 Durée des courses
- 🔄 Règles spécifiques

## Format CSV pour l'import

### Import de pilotes
```csv
name,nationality,date_of_birth,starts,poles,wins,drivers_championships,aggression,reputation,courtesy,composure,speed,crash,recovery,completed_laps,min_racing_skill
John Doe,France,15-03-1985,100,10,5,1,75.0,80.0,70.0,85.0,90.0,30.0,75.0,95.0,80.0
```

## Exigences non fonctionnelles

- **Performance** : Chargement rapide des fichiers, cache des véhicules/circuits
- **Fiabilité** : Validation des données avant génération
- **Utilisabilité** : Interface intuitive et claire
- **Portabilité** : Exécution sans installation Python (futur)
- **Maintenabilité** : Code modulaire et documenté
- **Sécurité** : Pas de modification des fichiers originaux

## Jalons du projet

1. ✅ **Jalon 1** : Compréhension et documentation des formats de fichiers
2. ✅ **Jalon 2** : Parsers et générateurs fonctionnels (.rcd, .cch, .veh, .gdb)
3. ✅ **Jalon 3** : Gestion complète des éléments (pilotes, voitures, circuits)
4. ✅ **Jalon 4** : Interface web de base
5. ✅ **Jalon 5** : Import/Export CSV
6. 🔄 **Jalon 6** : Parser/Générateur .rfm
7. 🔄 **Jalon 7** : Système d'isolation de véhicules
8. 🔄 **Jalon 8** : Création complète de championnats custom
9. ⏳ **Jalon 9** : Version packageée et portable

## Notes importantes

- ✅ Préserver la compatibilité avec rFactor
- ✅ Sauvegarder les fichiers originaux avant modification
- ✅ Valider toutes les modifications avant écriture
- ✅ Gestion des erreurs robuste
- **NOUVEAU** : Isolation des véhicules pour chaque championnat
- **NOUVEAU** : Pas de modification manuelle des .cch (générés par rFactor)

## Questions résolues

- ✅ Format exact des fichiers de talents → `.rcd` avec structure documentée
- ✅ Localisation des différents types de fichiers
- ✅ Encodage des fichiers rFactor → Windows-1252
- ✅ **Différence .rfm vs .cch** → .rfm = définition, .cch = progression
- ✅ **Comment créer un championnat** → Créer un .rfm, rFactor génère le .cch
- ✅ **Isolation des véhicules** → Copier dans dossier RFTOOL_<Name>

## Prochaines étapes

1. Créer le modèle de données pour `.rfm`
2. Implémenter le parser `.rfm`
3. Implémenter le générateur `.rfm`
4. Créer le service `ChampionshipCreatorService`
5. Implémenter la copie/isolation de véhicules
6. Créer l'interface de création de championnats
