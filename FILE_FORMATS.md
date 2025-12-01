# Documentation des formats de fichiers rFactor

## Vue d'ensemble

rFactor utilise plusieurs types de fichiers texte pour configurer les championnats, pilotes, véhicules et circuits. Cette documentation détaille la structure de chaque type de fichier.

---

## 1. Fichier de championnat (`.cch`)

### Localisation
`RFactorFiles/UserData/[PlayerName]/[ChampionshipName].cch`

### Format
Fichier texte avec structure INI étendue

### Structure complète

#### En-tête
```
//[[gMa1.002f (c)2007    ]] [[            ]]
```

#### Section [CAREER]
Statistiques globales de carrière du joueur

```ini
[CAREER]
Experience=0                    # Expérience totale
Money=500                       # Argent disponible
CurSeasIndex=0                  # Index de la saison actuelle
SinglePlayerVehicle="GAMEDATA\VEHICLES\..."  # Véhicule pour course solo
SinglePlayerFilter="GT3"        # Filtre de classe pour solo
MultiPlayerFilter="|..."        # Filtre pour multi (pipe-separated)
AIRealism=0.2500                # Niveau de réalisme IA (0.0-1.0)
SinglePlayerAIStrength=95       # Force IA en solo (0-100)
MultiPlayerAIStrength=95        # Force IA en multi (0-100)
AbortedSeasons=0                # Nombre de saisons abandonnées
TotalLaps=0                     # Total de tours effectués
TotalRaces=0                    # Total de courses
TotalRacesWithAI=0              # Courses contre IA
TotalPointsScored=0             # Points totaux
TotalChampionships=0            # Championnats gagnés
TotalWins=0                     # Victoires
TotalPoles=0                    # Pole positions
TotalLapRecords=0               # Records de tour
AvgStartPosition=0.000000       # Position de départ moyenne
AvgFinishPosition=0.000000      # Position d'arrivée moyenne
AvgRaceDistance=0.000000        # Distance moyenne de course
AvgOpponentStrength=0.000000    # Force moyenne des adversaires
```

#### Sections [VEHICLE]
Liste des véhicules possédés par le joueur (peut y avoir plusieurs sections)

```ini
[VEHICLE]
ID=0                                    # Identifiant unique du véhicule
File="GAMEDATA\VEHICLES\..."            # Chemin vers le fichier .veh
Skin=""                                 # Skin personnalisé (vide = défaut)
MetersDriven=0                          # Distance parcourue avec ce véhicule
MoneySpent=0                            # Argent dépensé sur ce véhicule
FreeVehicle=1                           # 1=gratuit, 0=acheté
Seat=(10.000,10.000)                    # Position du siège
Mirror=(10.000,10.000)                  # Position du miroir
UpgradeList:                            # Liste des améliorations (vide si aucune)
```

#### Section [CAREERSEASON]
Configuration du championnat en cours

```ini
[CAREERSEASON]
Name="Rhez Amateur Derby"               # Nom du championnat
SeasonStatus=2                          # 0=non commencé, 1=inconnu/non utilisé, 2=en cours
                                        # Note: Basé sur l'analyse des fichiers .cch réels
RaceSession=1                           # Session actuelle
RaceOver=0                              # 1=course terminée, 0=en cours
CurrentRace=0                           # Index de la course actuelle
PlayerVehicleID=1                       # ID du véhicule utilisé (ref [VEHICLE])

# Paramètres mécaniques
MECHFAIL_rate=2                         # Taux de panne mécanique
GAMEOPT_damagemultiplier=50             # Multiplicateur de dégâts (%)
GAMEOPT_fuel_mult=1                     # Multiplicateur consommation carburant
GAMEOPT_tire_mult=1                     # Multiplicateur usure pneus

# Paramètres de déroulement de course
RACECOND_reconnaissance=0               # Tours de reconnaissance (0=aucun)
RACECOND_walkthrough=1                  # Pit walk (0-2)
RACECOND_formation=3                    # Tour de formation (0-3)
RACECOND_safetycarcollision=1           # Safety car en cas de collision
RACECOND_safetycar_thresh=1.000000      # Seuil de déclenchement safety car
RACECOND_flag_rules=2                   # Règles des drapeaux (0-2)
RACECOND_blue_flags=7                   # Gestion drapeaux bleus

# Météo et temps
RACECOND_weather=0                      # Type de météo (0-4)
RACECOND_timescaled_weather=1           # Météo temps réel ou accélérée
RACECOND_race_starting_time=840         # Heure de départ (minutes depuis minuit)
RACECOND_race_timescale=1               # Échelle de temps (1=réel)

# Qualification et parc fermé
RACECOND_private_qual=2                 # Qualification privée (0-2)
RACECOND_parc_ferme=3                   # Règles parc fermé (0-3)

# Paramètres de course
GAMEOPT_ai_driverstrength=95            # Force des pilotes IA (0-120)
GAMEOPT_free_settings=-1                # Réglages libres (-1=défaut)
GAMEOPT_race_finish_criteria=1          # Critère de fin (0=temps, 1=tours)
GAMEOPT_race_laps=5                     # Nombre de tours (si critère=tours)
GAMEOPT_race_time=120                   # Durée en minutes (si critère=temps)
GAMEOPT_race_length=0.100000            # Longueur relative (0.0-1.0)
GAMEOPT_opponents=9                     # Nombre d'adversaires
GAMEOPT_speed_comp=0                    # Compensation de vitesse IA
GAMEOPT_crash_recovery=3                # Récupération après crash (0-3)
```

#### Section [PLAYER]
Configuration du joueur

```ini
[PLAYER]
Name="Loic"                             # Nom du joueur
VehFile="GAMEDATA\VEHICLES\..."         # Fichier véhicule assigné
RCDFile=""                              # Fichier talent (vide = utiliser info joueur)
SeasonPoints=0                          # Points dans le championnat
PointsPosition=0                        # Position au classement
PolesTaken=0                            # Poles obtenues dans ce championnat
OriginalGridPosition=9                  # Position de départ originale
CurrentGridPosition=9                   # Position de départ actuelle
ControlType=0                           # 0=joueur, 1=IA
Active=1                                # 1=actif, 0=inactif
```

#### Sections [OPPONENTxx]
Configuration des adversaires (xx = 00, 01, 02, ..., 08, etc.)

```ini
[OPPONENT00]
Name="Brandon Lang"                     # Nom du pilote
VehFile="GAMEDATA\VEHICLES\..."         # Fichier véhicule assigné
RCDFile=""                              # Fichier talent (vide = chercher dans Talent/)
SeasonPoints=0                          # Points dans le championnat
PointsPosition=0                        # Position au classement
PolesTaken=0                            # Poles obtenues
OriginalGridPosition=0                  # Position de départ originale
CurrentGridPosition=0                   # Position de départ actuelle
ControlType=1                           # 0=joueur, 1=IA
Active=1                                # 1=actif, 0=inactif
```

#### Sections [PLAYERTRACKSTAT]
Statistiques par circuit (peut y avoir plusieurs sections)

```ini
[PLAYERTRACKSTAT]
TrackName=Mills_Short                   # Nom du circuit
TrackFile=GAMEDATA\LOCATIONS\Mills\Mills_Short\Mills_Short
ClassRecord="*",0,-1.0000,-1.0000,-1.0000       # Record toutes classes
ClassRecord="GT3",0,-1.0000,-1.0000,-1.0000     # Record par classe
```

### Encodage
Windows-1252 ou ASCII

---

## 2. Fichiers de talents/pilotes (`.rcd`)

### Localisation
`RFactorFiles/GameData/Talent/[PilotName].rcd`

### Format
Fichier texte avec structure type dictionnaire

### Structure

```
Nom du pilote
{
  //Driver Info
  Nationality=American                  # Nationalité
  DateofBirth=28-11-1984                # Date de naissance (JJ-MM-AAAA)
  Starts=9                              # Nombre de départs en carrière
  Poles=2                               # Pole positions
  Wins=0                                # Victoires
  DriversChampionships=0                # Championnats pilotes

  //Driver Stats (valeurs décimales 0-100)
  Aggression=74.73                      # Agressivité en course
  Reputation=57.89                      # Réputation
  Courtesy=61.88                        # Courtoisie/Fair-play
  Composure=88.35                       # Sang-froid
  Speed=95.13                           # Vitesse pure
  Crash=4.87                            # Tendance aux accidents (inverse)
  Recovery=83.62                        # Capacité de récupération
  CompletedLaps=91.71                   # % de tours complétés
  MinRacingSkill=89.00                  # Compétence minimum de course
}
```

### Notes importantes
- Le nom du fichier doit correspondre au nom dans le fichier (sans espaces dans le nom de fichier)
- Si `RCDFile=""` dans le `.cch`, rFactor cherche automatiquement `[Name].rcd` dans `GameData/Talent/`
- Les statistiques sont des valeurs décimales précises (pas d'entiers)

### Fichier supplémentaire : Dialog.ini
Contient les phrases prononcées par les pilotes IA dans différentes situations

```ini
DialogType="ANGRY"
[Phrases séparées par des guillemets pour situations de colère]

DialogType="SORRY"
[Phrases d'excuse]

DialogType="TAUNT"
[Phrases de provocation]

DialogType="WHINE"
[Phrases de plainte]
```

---

## 3. Fichiers de véhicules (`.veh`)

### Localisation
`RFactorFiles/GameData/Vehicles/[Marque]/[Modèle]/[Catégorie]/[Équipe]/[Car]_[Num].veh`

### Format
Fichier texte avec structure INI commentée

### Structure

```ini
// Commentaires d'en-tête expliquant le système de livrée

DefaultLivery="Rd_01.DDS"               # Texture de livrée par défaut
PitCrewLivery="..."                     # Livrée équipe au stand (optionnel)
TrackLivery="TrackName, PREFIX"         # Livrée spécifique par circuit (multiple)

# Fichiers de référence pour les caractéristiques
HDVehicle=Rhez.hdv                      # Fichier physique du véhicule
Graphics=Rhez_upgrades.gen              # Modèle 3D et textures
Spinner=Rhez_Spinner.gen                # Modèle 3D pour sélection
GenString=                              # Génération noms GMT (optionnel)
Sounds=Rhez.sfx                         # Fichier sons moteur/freins/etc
Cameras=Rhez_cams.cam                   # Configuration caméras
Upgrades=Rhez_Upgrades.ini              # Améliorations disponibles
HeadPhysics=headphysics.ini             # Physique point de vue pilote
Cockpit=Rhez_cockpitinfo.ini            # Configuration cockpit
AIUpgradeClass=GT3                      # Classe pour upgrades IA

# Informations du véhicule
Number=01                               # Numéro de course
Team="Rhez Team RED Racing"             # Nom de l'équipe
PitGroup="Group1"                       # Groupe de stands
Driver="Roy Mandrake"                   # Pilote par défaut
Description="Team Red #1"               # Description
Engine="VL TEK"                         # Nom du moteur
Manufacturer="Vayline"                  # Constructeur
Classes="SRGP 2005 Rhez GT3"            # Classes de compétition (multiple)

# Historique de l'équipe
FullTeamName="Team Red"
TeamFounded=1998
TeamHeadquarters="Greenwood, Wisconsin"
TeamStarts=200
TeamPoles=55
TeamWins=20
TeamWorldChampionships=1

# Catégories de filtrage
Category="Vayline,2005 Rhez"            # Pour filtres de sélection
```

### Notes importantes
- Le pilote spécifié dans le `.veh` est le pilote par défaut
- Dans un championnat (`.cch`), le pilote assigné dans `[PLAYER]` ou `[OPPONENTxx]` remplace le pilote par défaut
- Les `Classes` définissent dans quelles catégories la voiture peut courir
- Les `Category` sont utilisées pour les filtres de sélection

---

## 4. Fichiers de circuits (`.gdb`)

### Localisation
`RFactorFiles/GameData/Locations/[CircuitName]/[Variante]/[Name].gdb`

### Format
Fichier texte avec structure type dictionnaire

### Structure

```
Nom_du_circuit
{
  Filter Properties = RoadCourse 2005 SRGrandPrix    # Propriétés de filtrage

  # Informations générales
  TrackName = Mills Metropark Short                  # Nom complet du circuit
  EventName = Sprint at Mills Metropark              # Nom de l'événement
  GrandPrixName = Sprint at Mills Metropark          # Nom du GP (doit = EventName)
  VenueName = Mills Metropark                        # Nom du lieu
  Location = Mills City, VA, USA                     # Localisation géographique
  Length = 1.846 km / 1.2 miles                      # Longueur du circuit
  TrackType = Permanent Road Course                  # Type de circuit
  Track Record = Brad Shuber, 53.669                 # Record du circuit
  Attrition = 30                                     # Facteur d'usure/attrition
  GarageDepth = 1.0                                  # Profondeur du garage

  # Configuration par défaut de course
  RaceLaps = 90                                      # Nombre de tours par défaut
  RaceTime = 120                                     # Durée en minutes par défaut

  # Configuration environnement et temps
  Latitude = 0                                       # Latitude (-90 à 90)
  NorthDirection = 245                               # Direction du nord (0-359 degrés)
  RaceDate = March 21                                # Date par défaut

  # Éclairage selon moment de la journée
  SkyBlendSunAngles=(-20.5, -1.0, 11.5, 25.5)       # Angles du soleil
  ShadowMinSunAngle=15.0                             # Angle minimum pour ombres

  # Couleurs d'éclairage ambiant (RGB)
  SunriseAmbientRGB = (120,120,110)
  SunriseDirectionalRGB = (255,248,198)
  SunriseFogRGB = (204,174,240)

  DayAmbientRGB = (80,89,126)
  DayDirectionalRGB = (255,255,255)
  DayFogRGB = (203,214,236)

  SunsetAmbientRGB = (130,130,120)
  SunsetDirectionalRGB = (255,248,198)
  SunsetFogRGB = (204,196,122)

  NightAmbientRGB = (10,10,10)
  NightDirectionalRGB = (15,15,15)
  NightFogRGB = (0,0,0)

  # Configuration IA
  SettingsFolder = Mills Short                       # Dossier de paramètres
  SettingsCopy = Grip.svm                            # Fichiers de config à copier
  SettingsCopy = Mills_Short.svm
  SettingsAI = Mills_Short.svm                       # Config spécifique IA
  Qualify Laptime = 55.669                           # Temps de référence quali
  Race Laptime = 55.869                              # Temps de référence course
}
```

### Notes importantes
- `GrandPrixName` doit être identique à `EventName` pour un tri correct
- Les fichiers `.svm` contiennent les réglages de setup pour l'IA
- Les paramètres d'éclairage sont essentiels pour les courses à différents moments de la journée

---

## Architecture complète des fichiers rFactor

```
RFactorFiles/
├── GameData/
│   ├── Talent/                              # ~230 pilotes disponibles
│   │   ├── [PilotName].rcd                  # Un fichier par pilote
│   │   └── Dialog.ini                       # Dialogues des pilotes
│   │
│   ├── Vehicles/                            # Véhicules par constructeur
│   │   ├── Rhez/
│   │   │   └── 2005Rhez/
│   │   │       ├── GT1/                     # Par catégorie
│   │   │       ├── GT2/
│   │   │       ├── GT3/
│   │   │       └── SRGP/
│   │   │           ├── TEAM RED/            # Par équipe
│   │   │           │   ├── RD_01.VEH
│   │   │           │   ├── RD_02.VEH
│   │   │           │   └── ...
│   │   │           └── TEAM BLUE/
│   │   ├── Hammer/
│   │   ├── Howston/
│   │   └── [autres constructeurs]/
│   │
│   └── Locations/                           # ~18 circuits
│       ├── Mills/
│       │   ├── Mills_Short/
│       │   │   ├── Mills_Short.gdb
│       │   │   └── [autres fichiers circuit]
│       │   ├── Mills_Long/
│       │   └── Mills_Long_Rev/
│       ├── Barcelona/
│       ├── Nuerburg/
│       └── [autres circuits]/
│
└── UserData/
    └── [PlayerName]/                        # Dossier par joueur
        ├── [ChampionshipName].cch           # Championnats du joueur
        └── [autres fichiers utilisateur]
```

---

## Relations entre les fichiers

### Championnat → Pilotes
1. Le fichier `.cch` contient des sections `[PLAYER]` et `[OPPONENTxx]`
2. Chaque section a un champ `Name` (ex: "Brandon Lang")
3. Si `RCDFile=""`, rFactor cherche `BrandonLang.rcd` dans `GameData/Talent/`
4. Si `RCDFile="chemin"`, utilise le fichier spécifié

### Championnat → Véhicules → Pilotes par défaut
1. Le fichier `.cch` assigne un `VehFile` à chaque pilote
2. Le fichier `.veh` spécifié a un champ `Driver` avec un pilote par défaut
3. Le `Name` dans le `.cch` remplace le `Driver` du `.veh` pour ce championnat

### Championnat → Circuits
1. Les statistiques `[PLAYERTRACKSTAT]` référencent des circuits via `TrackFile`
2. Le chemin pointe vers le fichier `.gdb` du circuit
3. Le circuit peut être référencé dans les événements du championnat

---

## Encodage et formats

- **Encodage** : Windows-1252 (ANSI) ou ASCII pour la compatibilité
- **Fin de ligne** : CRLF (Windows style `\r\n`)
- **Commentaires** : `//` pour les commentaires (style C++)
- **Chaînes** : Avec ou sans guillemets selon le contexte
- **Chemins** : Séparateur backslash `\` (Windows), insensible à la casse
- **Nombres** : Décimaux avec point `.` comme séparateur

---

## Points d'attention pour le parser

1. **Sections multiples** : Certaines sections peuvent apparaître plusieurs fois (`[VEHICLE]`, `[OPPONENTxx]`, `[PLAYERTRACKSTAT]`)
2. **Index dynamiques** : Les opponents sont numérotés `00`, `01`, etc. (format avec zéros initiaux)
3. **Chemins relatifs** : Les chemins sont relatifs à `RFactorFiles/`
4. **Valeurs vides** : Certains champs peuvent être vides (ex: `RCDFile=""`, `Skin=""`)
5. **Format flexible** : Espaces autour du `=` peuvent varier
6. **Commentaires** : Peuvent apparaître sur des lignes dédiées ou en fin de ligne
7. **Structures imbriquées** : `.rcd` et `.gdb` utilisent des accolades `{}`
8. **Listes** : Certains champs acceptent plusieurs valeurs séparées (Classes, Category)
