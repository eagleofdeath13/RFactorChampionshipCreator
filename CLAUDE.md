# CLAUDE.md - Contexte du projet rFactor Championship Creator

## Objectif du projet

Créer un éditeur de championnats personnalisés pour le jeu de simulation automobile **rFactor**. L'application permettra de gérer, créer et modifier des championnats via une interface web Python.

## 🎯 Découverte Majeure - Architecture des Championnats

### Deux Types de Fichiers Nécessaires

Un championnat rFactor fonctionne avec **DEUX** fichiers distincts :

1. **`.rfm`** (RFactor Mod) - **Définition du championnat**
   - Localisation : `rFactor/rFm/`
   - Rôle : Définit les règles, saisons, circuits, filtres de véhicules
   - **Créé MANUELLEMENT** (ou par notre outil)
   - Format : Fichier texte structuré

2. **`.cch`** (Career Championship) - **Progression du joueur**
   - Localisation : `rFactor/UserData/<Player>/`
   - Rôle : Stocke les points, positions, historique de course
   - **Généré AUTOMATIQUEMENT** par rFactor quand le joueur lance le championnat
   - Ne doit PAS être créé manuellement

### Workflow de Création

```
1. Créer un fichier .rfm dans rFm/
2. Le joueur lance rFactor et sélectionne le championnat
3. rFactor génère automatiquement le .cch correspondant
```

## Contexte du jeu rFactor

rFactor est un simulateur de course automobile qui utilise des fichiers de configuration pour gérer les championnats, pilotes, voitures et circuits.

### Types de fichiers rFactor

| Extension | Nom | Localisation | Rôle | Encodage |
|-----------|-----|--------------|------|----------|
| `.rfm` | RFactor Mod | `rFactor/rFm/` | Définition du championnat | Windows-1252 |
| `.cch` | Career Championship | `UserData/<Player>/` | Progression du joueur | Windows-1252 |
| `.rcd` | Talent (Driver) | `GameData/Talent/` | Pilote avec stats | Windows-1252 |
| `.veh` | Vehicle | `GameData/Vehicles/` | Voiture avec config | Windows-1252 |
| `.gdb` | Track Database | `GameData/Locations/` | Circuit | Windows-1252 |

## Structure du projet

```
RFactorChampionshipCreator/
├── src/
│   ├── parsers/              # Parsers pour fichiers rFactor
│   │   ├── rcd_parser.py     # ✅ Talents
│   │   ├── cch_parser.py     # ✅ Championships
│   │   ├── veh_parser.py     # ✅ Vehicles
│   │   ├── gdb_parser.py     # ✅ Tracks
│   │   └── rfm_parser.py     # ✅ RFactor Mods
│   ├── generators/
│   │   ├── rcd_generator.py  # ✅ Talents
│   │   ├── cch_generator.py  # ✅ Championships
│   │   └── rfm_generator.py  # ✅ RFactor Mods
│   ├── models/
│   │   ├── talent.py         # ✅ Talent, TalentPersonalInfo, TalentStats
│   │   ├── championship.py   # ✅ Championship, Season, Player, Opponent
│   │   ├── vehicle.py        # ✅ Vehicle, VehicleTeamInfo, VehicleConfig
│   │   ├── track.py          # ✅ Track
│   │   └── rfm.py            # ✅ RFM models
│   ├── services/
│   │   ├── talent_service.py         # ✅ Gestion talents
│   │   ├── championship_service.py   # ✅ Gestion championnats (.cch)
│   │   ├── vehicle_service.py        # ✅ Gestion véhicules
│   │   ├── track_service.py          # ✅ Gestion circuits
│   │   ├── import_service.py         # ✅ Import/Export CSV
│   │   ├── championship_creator.py   # ✅ Création championnats custom
│   │   └── vehicle_isolation_service.py  # ✅ Isolation et renommage véhicules
│   ├── web/                  # Interface web FastAPI
│   │   ├── app.py
│   │   ├── routes/
│   │   ├── schemas/
│   │   ├── templates/
│   │   └── static/
│   └── utils/
│       ├── file_utils.py
│       ├── config.py
│       └── rfactor_validator.py
├── tests/                    # Tests unitaires
├── SPECIFICATIONS.md         # Spécifications détaillées
├── CLAUDE.md                 # Ce fichier
└── README.md                 # Documentation utilisateur
```

## Système d'Isolation des Véhicules

### Problématique
Pour créer des championnats personnalisés, nous devons modifier les fichiers `.veh` (champs `Classes` et `Driver`).
**Mais** : nous ne voulons PAS modifier les fichiers originaux !

### Solution : Isolation + Renommage par Championnat
Chaque championnat créé par l'outil aura ses propres copies de véhicules **renommées avec préfixe** :

```
GameData/Vehicles/
├── RHEZ/                           # Véhicules ORIGINAUX (ne jamais toucher)
│   └── 2005RHEZ/
│       └── GT3/
│           └── TEAM_YELLOW/
│               ├── YEL_09.veh
│               └── YEL_09.dds
│
└── M_MyChampionship2025/      # Véhicules ISOLÉS pour le championnat
    └── 2005RHEZ/                   # Structure copiée
        └── GT3/
            └── TEAM_YELLOW/
                ├── MC_YEL_09.veh      # RENOMMÉ avec préfixe "MC"
                ├── MC_YEL_09.dds      # Assets renommés aussi
                └── MC_YEL_09.txt
                # Modifié : Classes="MyChampionship2025"
                #           Driver="John Doe"
                #           Description="MC Team Yellow #09"
                #           DefaultLivery="MC_YEL_09.dds"
```

### Système de Préfixe (Évite les Doublons)
- **Génération automatique** : Premières lettres du nom du championnat
- **Exemples** :
  - "MyChampionship2025" → "MC"
  - "TestChampionship" → "TE"
  - "SuperGT" → "SG"
- **Appliqué à** :
  - Nom du fichier `.veh` (ex: `MC_YEL_09.veh`)
  - Champ `Description` (ex: "MC Team Yellow #09")
  - Assets spécifiques (`.dds`, `.tga`, `.bmp`, `.txt`)
  - Références dans le `.veh` (`DefaultLivery`, `PitCrewLivery`, `TrackLivery`)

### Avantages
- ✅ Pas de modification des fichiers originaux
- ✅ Chaque championnat est complètement indépendant
- ✅ **Véhicules détectés comme uniques par rFactor** (pas de doublons)
- ✅ Facile à supprimer (1 dossier = 1 championnat)
- ✅ Évite les conflits entre championnats
- ✅ Permet d'assigner des pilotes différents aux mêmes voitures
- ✅ Préfixe visible facilite l'identification dans le jeu

## Système de Préfixe

### Convention de Nommage
- **Préfixe global** : `M_` (M pour Manuel - identifie tous les championnats créés par l'outil)
  - Limite : 19 caractères max pour le nom du fichier .rfm (incluant préfixe)
  - Avec `M_` (2 caractères), on peut avoir des noms de championnat jusqu'à 17 caractères
  - Exemple : `M_MyLongChampName` = 18 caractères (OK)
- **Préfixe véhicules** : 2-3 lettres générées depuis le nom du championnat (évite doublons)
- **Catégorie unique** : Nom du championnat (utilisé pour filtrer les véhicules)

Exemples :
- Dossier : `M_MyChampionship2025`
- Préfixe véhicule : `MC`
- Fichier véhicule : `MC_YEL_09.veh`

### Fichiers Générés
```
rFactor/
├── rFm/
│   └── M_MyChampionship2025.rfm      # Définition du championnat
│
├── GameData/Vehicles/
│   └── M_MyChampionship2025/         # Véhicules isolés
│       └── [copies modifiées]
│
└── UserData/Loic/
    └── M_MyChampionship2025.cch      # Généré par rFactor
```

### Filtrage dans l'Interface
- **Véhicules originaux** : Tous SAUF ceux dans `M_*`
- **Véhicules custom** : Ceux dans `M_*`
- **Par championnat** : Ceux dans `M_<ChampionshipName>`

## Phases du projet

### ✅ Phase 1 : Analyse (COMPLÉTÉE)
- [x] Analyser la structure des fichiers `.cch`, `.rcd`, `.veh`, `.gdb`, `.rfm`
- [x] Identifier les fichiers importants dans rFactor
- [x] Documenter les formats de fichiers
- [x] Comprendre les relations entre fichiers

### ✅ Phase 2 : Parsers et Générateurs de Base (COMPLÉTÉE)
- [x] Parser/Générateur pour `.rcd` (Talents)
- [x] Parser/Générateur pour `.cch` (Championships)
- [x] Parser pour `.veh` (Vehicles)
- [x] Parser pour `.gdb` (Tracks)

### ✅ Phase 2bis : Gestion des `.rfm` (COMPLÉTÉE)
- [x] Modèle de données pour `.rfm`
- [x] Parser `.rfm`
- [x] Générateur `.rfm`

### ✅ Phase 3 : Gestion des Éléments (COMPLÉTÉE)
- [x] Service de gestion des pilotes
- [x] Service de gestion des voitures
- [x] Service de gestion des circuits
- [x] Service de gestion des championnats (.cch)

### ✅ Phase 4 : Import/Export CSV (COMPLÉTÉE)
- [x] Import CSV pour pilotes
- [x] Export CSV pour pilotes

### ✅ Phase 5 : Interface Web (COMPLÉTÉE - Consultation)
- [x] Application FastAPI complète
- [x] Routes API pour tous les éléments (20+ endpoints)
- [x] Pages de liste (pilotes, voitures, circuits, championnats)
- [x] Pages de détails enrichies pour tous les éléments
- [x] Création/Édition de talents via formulaire web
- [x] Gestion complète véhicules et circuits
- [x] Interface de création de championnats (voir Phase 5bis ci-dessous)

### ✅ Phase 5bis : Création de Championnats Custom (COMPLÉTÉE - 28 Nov 2025)
1. **Système de préfixe**
   - [x] Validation des noms de championnats
   - [x] Génération du préfixe `M_<Name>`
   - [x] **Génération préfixe véhicule** (2-3 lettres, ex: "TE")

2. **Isolation de véhicules**
   - [x] Copie de fichiers `.veh` + assets (DDS, txt, etc.)
   - [x] **Renommage fichiers** `.veh` avec préfixe (ex: `TE_GRN_08.veh`)
   - [x] **Renommage assets** spécifiques (`.dds`, `.tga`, `.bmp`, `.txt`)
   - [x] Modification du champ `Classes`
   - [x] Modification du champ `Driver`
   - [x] **Modification `Description`** (ajout préfixe)
   - [x] **Modification `DefaultLivery`** (nouveau nom avec préfixe)
   - [x] **Modification `PitCrewLivery`** et `TrackLivery`
   - [x] Préservation de la structure des dossiers

3. **Génération `.rfm`**
   - [x] Définition des saisons
   - [x] Configuration des filtres véhicules
   - [x] Liste ordonnée des circuits (SceneOrder)
   - [x] Système de points

4. **Interface de création**
   - [x] Formulaire multi-étapes : Informations de base
   - [x] Sélection des véhicules originaux
   - [x] Association pilote ↔ véhicule
   - [x] Sélection et ordre des circuits
   - [x] Configuration des options

5. **Validation**
   - [x] Tests de génération de championnat
   - [x] Vérification fichiers générés (.rfm, .veh, assets)
   - [ ] **Test in-game dans rFactor** (en attente utilisateur)

### Phase 6 : Portabilité (FUTUR)
- [ ] Script `.bat` pour lancement
- [ ] Package PyInstaller
- [ ] Documentation utilisateur

## Technologies

- **Backend** : Python 3.x
- **Framework web** : FastAPI ✅
- **Frontend** : HTML/CSS/JavaScript + Jinja2
- **Validation** : Pydantic
- **Testing** : Pytest
- **Packaging** : PyInstaller (futur)

## Fonctionnalités principales

### 1. Gestion des championnats
- ✅ Lister les championnats existants (.cch)
- ✅ Lire un championnat
- ✅ Dupliquer un championnat
- ✅ **Créer un nouveau championnat custom (.rfm)**
- ✅ Supprimer un championnat custom

### 2. Gestion des pilotes (Talents)
- ✅ Lister les pilotes existants
- ✅ Créer de nouveaux pilotes
- ✅ Modifier les pilotes
- ✅ Import/Export CSV
- ✅ Assigner des pilotes à des véhicules (via création championnat)

### 3. Gestion des voitures
- ✅ Lister les voitures disponibles
- ✅ Filtrer par classe, fabricant
- ✅ Recherche
- ✅ Isoler des voitures pour un championnat (avec renommage)
- ✅ Modifier les classes d'un véhicule
- ✅ Assigner un pilote à un véhicule (via création championnat)

### 4. Gestion des circuits
- ✅ Lister les circuits disponibles
- ✅ Recherche de circuits
- ✅ Sélectionner et ordonner les circuits (via création championnat)

### 5. Interface web
- ✅ Interface de base
- ✅ Interface de création de championnats (formulaire multi-étapes)
- ✅ Interface responsive

## Conventions de code

- ✅ Noms de variables explicites en **anglais**
- ✅ Commentaires en français si nécessaire
- ✅ Structure modulaire (parsers, generators, models, services, web)
- ✅ Séparation des responsabilités
- ✅ Tests unitaires pour fonctions critiques
- ✅ Docstrings complètes
- ✅ Type hints Python

## Points d'attention

- ✅ **Compatibilité** : Fichiers générés compatibles avec rFactor
- ✅ **Encodage** : Windows-1252 pour tous les fichiers rFactor
- ✅ **Validation** : Valider toutes les données avant génération
- ✅ **Sauvegarde** : JAMAIS modifier les fichiers originaux
- ✅ **Système d'isolation** : Copie + renommage des véhicules pour éviter les doublons
- ✅ **Préfixe véhicules** : Génération automatique (ex: "TestChampionship" → "TE")
- ✅ Ne PAS créer de `.cch` manuellement (rFactor le génère)

## Glossaire

- **Championship (Championnat)** : Une saison complète avec plusieurs courses
- **Talent (Pilote)** : Un pilote avec ses caractéristiques (compétences, équipe)
- **Season (Saison)** : Une partie d'un championnat avec ses circuits
- **`.rfm`** : RFactor Mod - Définit un championnat
- **`.cch`** : Career Championship - Stocke la progression
- **`.rcd`** : Talent file - Fichier pilote
- **`.veh`** : Vehicle file - Fichier voiture
- **`.gdb`** : Track database - Fichier circuit
- **Isolation** : Copie de véhicules dans un dossier dédié au championnat
- **M_** : Préfixe pour championnats créés par l'outil

## Historique des décisions

- ✅ **Choix de Python** : Polyvalent, bon support parsing et web
- ✅ **FastAPI** : Plus moderne et performant que Flask
- ✅ **Interface web** : Plus portable qu'une interface desktop
- ✅ **Pydantic** : Validation robuste des données
- ✅ **Windows-1252** : Encodage confirmé pour fichiers rFactor
- ✅ **Isolation de véhicules** : Évite modification des originaux
- ✅ **Système de préfixe** : `M_` pour dossiers (Manuel), préfixe court pour véhicules
  - Changé de `RFTOOL_` (7 chars) à `M_` (2 chars) le 2 Déc 2025 pour permettre des noms plus longs
  - Limite noms championnats : 12 chars → 17 chars
- ✅ **Renommage véhicules** : Évite doublons détectés par rFactor (28 Nov 2025)

## Workflow de Création de Championnat

### Étape 1 : Informations de Base
```python
championship_info = {
    "name": "MyChampionship2025",          # Nom unique (max 17 chars)
    "full_name": "My Custom Championship",  # Nom complet
    "description": "A custom championship",
}
# → Génère automatiquement "M_MyChampionship2025" (20 chars, dépasse limite!)
# → Mieux : "MyChamp2025" → "M_MyChamp2025" (14 chars, OK)
```

### Étape 2 : Sélection des Véhicules
```python
# L'utilisateur sélectionne des véhicules ORIGINAUX
selected_vehicles = [
    "GAMEDATA/VEHICLES/RHEZ/2005RHEZ/GT3/TEAM_YELLOW/YEL_09.veh",
    "GAMEDATA/VEHICLES/RHEZ/2005RHEZ/GT3/TEAM_BLUE/BLU_07.veh",
]
```

### Étape 3 : Association Pilotes ↔ Véhicules
```python
assignments = {
    "YEL_09.veh": "John Doe",    # Pilote assigné
    "BLU_07.veh": "Jane Smith",
}
```

### Étape 4 : Isolation des Véhicules
Pour chaque véhicule :
1. Copier le `.veh` + assets dans `M_MyChampionship2025/`
2. Modifier `Classes="MyChampionship2025 GT3"`
3. Modifier `Driver="John Doe"`

### Étape 5 : Sélection des Circuits
```python
tracks = [
    "Mills_Short",
    "Joesville_Speedway",
    "Toban_Long",
]
```

### Étape 6 : Génération du `.rfm`
```python
# Créer rFactor/rFm/M_MyChampionship2025.rfm
rfm = {
    "mod_name": "MyChampionship2025",
    "vehicle_filter": "MyChampionship2025",  # Filtre unique
    "seasons": [{
        "name": "Season 1",
        "tracks": tracks,
    }],
}
```

### Étape 7 : Le Joueur Lance rFactor
→ rFactor génère automatiquement le `.cch`

## Ressources

- Fichiers du jeu : Configuration dans `config.json`
- Spécifications détaillées : `SPECIFICATIONS.md`
- Fichiers de référence : `RFactorFiles/` (optionnel)

## Statut actuel

### ✅ Complété (Sprint 1-5)
- [x] Spécifications initiales
- [x] Analyse complète des formats de fichiers
- [x] Parsers pour .rcd, .cch, .veh, .gdb (4/5)
- [x] Générateurs pour .rcd, .cch (2/3)
- [x] Services de gestion (talents, véhicules, circuits, championnats)
- [x] Import/Export CSV
- [x] Interface web complète (FastAPI)
- [x] Routes API (20+ endpoints fonctionnels)
- [x] Système de configuration
- [x] 68 tests unitaires passants
- [x] Gestion complète talents via interface web
- [x] Visualisation complète championnats via interface web
- [x] Gestion véhicules et circuits via interface web

### ✅ Sprint 5bis : Création de Championnats Custom (Complété - 28 Nov 2025)
- [x] Modèle de données `.rfm`
- [x] Parser `.rfm`
- [x] Générateur `.rfm`
- [x] Service de création de championnats (ChampionshipCreatorService)
- [x] Système d'isolation de véhicules (VehicleIsolationService)
- [x] **Système de renommage des véhicules avec préfixe** (évite doublons rFactor)
- [x] Interface web de création de championnats (formulaire multi-étapes)
- [x] Route API `/api/championships/create` fonctionnelle

**Nouveau** : Système complet de **renommage des véhicules isolés** implémenté et testé :
- Génération de préfixe automatique (ex: "TestChampionship" → "TE")
- Renommage fichiers `.veh` et assets (`.dds`, `.txt`, etc.)
- Modification des références (`DefaultLivery`, `Description`, `PitCrewLivery`, `TrackLivery`)
- Les véhicules sont maintenant détectés comme **uniques** par rFactor (plus de doublons)

**À faire** : Test in-game dans rFactor pour validation finale

**Documentation** : Voir `UPDATE_28NOV2025_VEHICLE_RENAMING.md` et `VEHICLE_RENAMING_NOTES.md`

### ⏳ À Venir (Sprint 6+)
- [ ] Package PyInstaller
- [ ] Documentation utilisateur complète
- [ ] Scripts de lancement (.bat/.sh)

## Notes pour Claude

Lorsque vous travaillez sur ce projet :

1. **Toujours préserver les originaux**
   - JAMAIS modifier les fichiers dans les dossiers originaux
   - Utiliser le système d'isolation (`M_<Name>`)

2. **Respecter les formats rFactor**
   - Encodage : Windows-1252
   - Format des fichiers documenté dans SPECIFICATIONS.md

3. **Architecture modulaire**
   - Parsers → Modèles → Services → Web
   - Séparation claire des responsabilités

4. **Validation robuste**
   - Valider TOUTES les données avant génération
   - Gestion d'erreurs complète

5. **Points clés à retenir**
   - `.rfm` = définition (créé par l'outil)
   - `.cch` = progression (créé par rFactor)
   - Ne JAMAIS créer de `.cch` manuellement
   - Utiliser le préfixe `M_` pour tous les championnats custom

6. **Prochaines étapes**
   - **Validation in-game** : Tester le championnat généré dans rFactor
   - **Sprint 6** : Packaging et portabilité (PyInstaller, scripts .bat)
   - **Documentation utilisateur** : Guide d'utilisation complet
