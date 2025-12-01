# Guide Développeur - rFactor Championship Creator

## 📖 Table des Matières

1. [Architecture](#architecture)
2. [Structure du Projet](#structure-du-projet)
3. [Composants Principaux](#composants-principaux)
4. [Systèmes Spéciaux](#systèmes-spéciaux)
5. [Développement](#développement)
6. [Tests](#tests)
7. [Conventions de Code](#conventions-de-code)

---

## Architecture

### Vue d'Ensemble

```
┌─────────────────────────────────────────┐
│          Navigateur Web                 │
│  (HTML/CSS/JS + Bootstrap)              │
└──────────────┬──────────────────────────┘
               │ HTTP/REST
┌──────────────▼──────────────────────────┐
│          FastAPI Application            │
│  - Routes (talents, championships, ...) │
│  - Pydantic Schemas (validation)        │
│  - Templates Jinja2                     │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│         Services Layer                  │
│  - TalentService                        │
│  - ChampionshipService                  │
│  - ChampionshipCreatorService           │
│  - VehicleIsolationService              │
│  - ImportService                        │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│      Parsers & Generators               │
│  - RCDParser/Generator (Talents)        │
│  - CCHParser/Generator (Championships)  │
│  - RFMParser/Generator (Mods)           │
│  - VEHParser (Vehicles)                 │
│  - GDBParser (Tracks)                   │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│       Fichiers rFactor                  │
│  - .rcd (talents)                       │
│  - .cch (championnats progression)      │
│  - .rfm (championnats définition)       │
│  - .veh (véhicules)                     │
│  - .gdb (circuits)                      │
└─────────────────────────────────────────┘
```

### Principes de Conception

1. **Séparation des responsabilités**
   - Parsers : Lecture/Écriture fichiers rFactor
   - Models : Représentation des données
   - Services : Logique métier
   - Web : Interface et API

2. **Validation par couches**
   - Pydantic : Validation des données
   - Services : Validation métier
   - RFactorValidator : Validation installation

3. **Immutabilité des originaux**
   - Jamais modifier les fichiers originaux de rFactor
   - Toujours isoler (copier) avant modification

---

## Structure du Projet

```
RFactorChampionshipCreator/
├── src/
│   ├── parsers/              # Lecture fichiers rFactor
│   │   ├── rcd_parser.py     # Talents (.rcd)
│   │   ├── cch_parser.py     # Championships progression (.cch)
│   │   ├── rfm_parser.py     # Mods/Championships définition (.rfm)
│   │   ├── veh_parser.py     # Vehicles (.veh)
│   │   └── gdb_parser.py     # Tracks (.gdb)
│   │
│   ├── generators/           # Écriture fichiers rFactor
│   │   ├── rcd_generator.py  # Génération .rcd
│   │   ├── cch_generator.py  # Génération .cch
│   │   └── rfm_generator.py  # Génération .rfm
│   │
│   ├── models/               # Modèles de données
│   │   ├── talent.py         # Talent, TalentPersonalInfo, TalentStats
│   │   ├── championship.py   # Championship, Season, Player, Opponent
│   │   ├── rfm.py            # RFM, RFMSeason, RFMRace
│   │   ├── vehicle.py        # Vehicle, VehicleTeamInfo, VehicleConfig
│   │   └── track.py          # Track
│   │
│   ├── services/             # Logique métier
│   │   ├── talent_service.py           # CRUD talents
│   │   ├── championship_service.py     # Lecture championnats (.cch)
│   │   ├── championship_creator.py     # Création championnats (.rfm)
│   │   ├── vehicle_isolation_service.py# Isolation + renommage véhicules
│   │   ├── vehicle_service.py          # Gestion véhicules
│   │   ├── track_service.py            # Gestion circuits
│   │   └── import_service.py           # Import/Export CSV
│   │
│   ├── web/                  # Interface web FastAPI
│   │   ├── app.py            # Application principale
│   │   ├── routes/           # Routes API
│   │   │   ├── talents.py
│   │   │   ├── championships.py
│   │   │   ├── vehicles.py
│   │   │   ├── tracks.py
│   │   │   ├── import_export.py
│   │   │   └── config.py
│   │   ├── schemas/          # Schémas Pydantic
│   │   ├── templates/        # Templates Jinja2
│   │   └── static/           # CSS/JS
│   │
│   └── utils/
│       ├── file_utils.py            # Utilitaires fichiers
│       ├── config.py                # Gestion configuration
│       └── rfactor_validator.py     # Validation installation rFactor
│
├── tests/                    # Tests unitaires
├── docs/                     # Documentation
│   └── archive/              # Fichiers de travail archivés
├── demos/                    # Scripts de démonstration
├── config.json               # Configuration (généré)
├── requirements.txt          # Dépendances Python
└── start.bat                 # Script de lancement
```

---

## Composants Principaux

### 1. Parsers

#### RCDParser (`src/parsers/rcd_parser.py`)

Parse les fichiers `.rcd` (talents/pilotes).

**Méthodes** :
```python
# Parser un fichier
talent = RCDParser.parse("GameData/Talent/JohnDoe.rcd")

# Obtenir le contenu brut
content = RCDParser.read_file("path/to/file.rcd")
```

**Format** :
```
PersonalInfo1={
  Name = "John Doe"
  Nationality = "France"
  DateOfBirth = "15-03-1990"
  ...
}
```

**Encodage** : Windows-1252

#### RFMParser (`src/parsers/rfm_parser.py`)

Parse les fichiers `.rfm` (définition de championnat).

**Méthodes** :
```python
# Parser un fichier
rfm = RFMParser.parse("rFm/MyChampionship.rfm")

# Parser du contenu
rfm = RFMParser.parse_content(content)
```

**Format** : Voir `FILE_FORMATS.md`

#### VEHParser (`src/parsers/veh_parser.py`)

Parse les fichiers `.veh` (véhicules).

**Méthodes** :
```python
# Parser un véhicule
vehicle = VEHParser.parse("GameData/Vehicles/.../car.veh")
```

### 2. Générateurs

#### RCDGenerator (`src/generators/rcd_generator.py`)

Génère des fichiers `.rcd` depuis des objets `Talent`.

**Méthodes** :
```python
# Générer un fichier
RCDGenerator.generate(talent, "output/path/JohnDoe.rcd")

# Générer le contenu
content = RCDGenerator.generate_content(talent)
```

**Encodage** : Windows-1252

#### RFMGenerator (`src/generators/rfm_generator.py`)

Génère des fichiers `.rfm`.

**Méthodes** :
```python
# Générer un fichier
RFMGenerator.generate(rfm, "rFm/MyChampionship.rfm")
```

### 3. Models

#### Talent (`src/models/talent.py`)

Représente un pilote.

```python
@dataclass
class Talent:
    name: str
    personal_info: TalentPersonalInfo
    stats: TalentStats
    description: str = ""
    category: str = "Driver"
```

**Validation** :
- Stats entre 0.0 et 100.0
- Personal info >= 0
- Name non vide

#### RFM (`src/models/rfm.py`)

Représente un championnat (.rfm).

```python
@dataclass
class RFM:
    mod_name: str
    vehicle_filter: str
    scenes: List[str]
    seasons: List[RFMSeason]
    ...
```

### 4. Services

#### TalentService (`src/services/talent_service.py`)

CRUD complet pour les talents.

```python
service = TalentService(rfactor_path)

# Lister tous
talents = service.list_all()

# Obtenir un
talent = service.get("John Doe")

# Créer
service.create(talent)

# Mettre à jour
service.update("John Doe", talent)

# Supprimer
service.delete("John Doe")

# Rechercher
results = service.search("john")
```

#### ChampionshipCreatorService (`src/services/championship_creator.py`)

Crée des championnats custom.

**Workflow** :
```python
service = ChampionshipCreatorService(rfactor_path)

# Créer un championnat
championship_info = {
    "name": "MyChampionship2025",
    "full_name": "My Custom Championship",
    "description": "A test championship",
    "vehicle_assignments": [
        {"vehicle_path": "...", "driver_name": "John Doe"},
        ...
    ],
    "tracks": ["Mills_Short", "Toban_Long"],
}

service.create_championship(championship_info)
```

**Génère** :
1. Dossier véhicules isolés : `RFTOOL_MyChampionship2025/`
2. Fichier `.rfm` : `rFm/RFTOOL_MyChampionship2025.rfm`

#### VehicleIsolationService (`src/services/vehicle_isolation_service.py`)

Isole et renomme les véhicules pour un championnat.

**Fonctionnalités** :
- Copie des fichiers `.veh`
- **Renommage avec préfixe** (ex: "TE")
- Renommage des assets (`.dds`, `.txt`, etc.)
- Modification des références dans le `.veh`
- Modification des champs :
  - `Classes`
  - `Driver`
  - `Description` (ajout préfixe)
  - `DefaultLivery`
  - `PitCrewLivery`
  - `TrackLivery`

**Méthode** :
```python
service = VehicleIsolationService(rfactor_path)

assignments = [
    {
        "vehicle_path": "GAMEDATA/VEHICLES/.../car.veh",
        "driver_name": "John Doe"
    }
]

service.isolate_vehicles(
    vehicle_assignments=assignments,
    championship_name="MyChampionship2025",
    output_dir="RFTOOL_MyChampionship2025"
)
```

---

## Systèmes Spéciaux

### Système de Préfixe Véhicules

**Problème** : rFactor détecte les véhicules isolés comme doublons des originaux.

**Solution** : Renommage automatique avec préfixe court.

#### Génération du Préfixe

```python
def _generate_vehicle_prefix(championship_name: str) -> str:
    """
    Génère un préfixe court (2-3 lettres).
    Ex: "TestChampionship2025" → "TE"
    """
    # Séparer par majuscules ou chiffres
    words = re.findall(r'[A-Z][a-z]*|\d+', championship_name)

    # Prendre première lettre de chaque mot
    prefix = ''.join([w[0].upper() for w in words if w])

    # Limiter à 3 caractères
    return prefix[:3]
```

**Exemples** :
| Championship Name | Préfixe |
|-------------------|---------|
| TestChampionship2025 | TE |
| MyAwesomeChampionship | MAC |
| SuperGT | SG |
| F1Season | FS |

#### Application du Préfixe

1. **Nom du fichier** : `GRN_08.veh` → `TE_GRN_08.veh`

2. **Champ Description** :
   ```ini
   Avant : Description="Team Green #08"
   Après : Description="TE Team Green #08"
   ```

3. **Champ DefaultLivery** :
   ```ini
   Avant : DefaultLivery="GRN_08.DDS"
   Après : DefaultLivery="TE_GRN_08.DDS"
   ```

4. **Assets** : `GRN_08.dds` → `TE_GRN_08.dds`

**Fichiers renommés** : `.dds`, `.tga`, `.bmp`, `.txt`
**Fichiers NON renommés** : `.hdv`, `.sfx`, `.gen`, `.gmt`, `.mas` (partagés)

### Système de Configuration

#### Composants

1. **RFactorValidator** (`src/utils/rfactor_validator.py`)
   - Valide qu'un chemin est une installation rFactor valide
   - Vérifie la présence des dossiers critiques
   - Liste les profils joueurs

2. **Config** (`src/utils/config.py`)
   - Gère `config.json`
   - Stocke le chemin rFactor
   - Stocke le profil joueur actuel

#### Utilisation

```python
from src.utils.config import get_config

config = get_config()

if not config.is_configured():
    print("Run setup_config.py first")
    exit(1)

rfactor_path = config.get_rfactor_path()
player = config.get_current_player()
```

### Système d'Isolation

**Principe** : Ne jamais modifier les fichiers originaux de rFactor.

**Workflow** :
1. Copier les fichiers `.veh` dans `RFTOOL_<Name>/`
2. Renommer avec préfixe
3. Modifier les champs (`Classes`, `Driver`, `Description`)
4. Copier et renommer les assets

**Structure générée** :
```
GameData/Vehicles/
├── RHEZ/                     # Originaux (intacts)
│   └── 2005RHEZ/
│       └── GT3/
│           └── TEAM_YELLOW/
│               ├── YEL_09.veh
│               └── YEL_09.dds
│
└── RFTOOL_MyChampionship/    # Isolés + renommés
    └── 2005RHEZ/
        └── GT3/
            └── TEAM_YELLOW/
                ├── MC_YEL_09.veh      # Renommé
                ├── MC_YEL_09.dds      # Renommé
                └── Rhez.hdv           # Partagé (pas renommé)
```

---

## Développement

### Installation de l'Environnement

```bash
# Cloner le projet
git clone <url>
cd RFactorChampionshipCreator

# Installer les dépendances
pip install -r requirements.txt

# Configurer
python setup_config.py
```

### Lancer en Mode Développement

```bash
# Serveur web avec hot-reload
python -m uvicorn src.web.app:app --reload --port 5000

# Ou via le script
start.bat
```

### Ajouter un Nouveau Parser

1. Créer `src/parsers/xxx_parser.py`
2. Hériter de la structure existante
3. Implémenter `parse()` et `parse_content()`
4. Gérer l'encodage Windows-1252
5. Ajouter tests dans `tests/test_parsers/`

**Exemple** :
```python
class XXXParser:
    ENCODING = 'windows-1252'

    @staticmethod
    def parse(file_path: str) -> Model:
        content = XXXParser.read_file(file_path)
        return XXXParser.parse_content(content)

    @staticmethod
    def parse_content(content: str) -> Model:
        # Parsing logic
        ...

    @staticmethod
    def read_file(file_path: str) -> str:
        with open(file_path, 'r', encoding=XXXParser.ENCODING) as f:
            return f.read()
```

### Ajouter un Nouveau Service

1. Créer `src/services/xxx_service.py`
2. Injecter `rfactor_path` dans `__init__`
3. Utiliser les parsers existants
4. Implémenter CRUD si applicable
5. Ajouter tests

**Exemple** :
```python
class XXXService:
    def __init__(self, rfactor_path: str, validate: bool = True):
        if validate:
            RFactorValidator.validate_or_raise(rfactor_path)
        self.rfactor_path = Path(rfactor_path)

    def get_xxx_directory(self) -> Path:
        return self.rfactor_path / 'GameData' / 'XXX'

    def list_all(self) -> List[Model]:
        # Implementation
        ...
```

### Ajouter une Route API

1. Créer/Modifier `src/web/routes/xxx.py`
2. Créer schéma Pydantic dans `src/web/schemas/xxx.py`
3. Enregistrer le router dans `src/web/app.py`
4. Créer template Jinja2 dans `src/web/templates/`

**Exemple** :
```python
from fastapi import APIRouter, HTTPException
from src.services.xxx_service import XXXService
from src.web.schemas.xxx import XXXSchema

router = APIRouter(prefix="/api/xxx", tags=["XXX"])

@router.get("/")
def list_xxx():
    service = XXXService(config.get_rfactor_path())
    return service.list_all()
```

---

## Tests

### Structure

```
tests/
├── test_parsers/
│   ├── test_rcd_parser.py
│   ├── test_rfm_parser.py
│   └── ...
├── test_generators/
│   └── ...
├── test_services/
│   └── ...
└── test_utils/
    ├── test_config.py
    └── test_rfactor_validator.py
```

### Lancer les Tests

```bash
# Tous les tests
pytest

# Avec verbosité
pytest -v

# Un fichier spécifique
pytest tests/test_parsers/test_rcd_parser.py

# Une fonction spécifique
pytest tests/test_parsers/test_rcd_parser.py::test_parse_basic_rcd

# Avec couverture
pytest --cov=src --cov-report=html
```

### Écrire un Test

```python
import pytest
from src.parsers.xxx_parser import XXXParser

def test_parse_basic():
    content = """
    Field1={
        Value=123
    }
    """
    result = XXXParser.parse_content(content)
    assert result.field1 == 123

def test_parse_error():
    with pytest.raises(ValueError):
        XXXParser.parse_content("invalid")
```

### Fixtures

```python
@pytest.fixture
def sample_talent():
    return Talent(
        name="Test Driver",
        personal_info=TalentPersonalInfo(
            nationality="France",
            date_of_birth="15-03-1990"
        ),
        stats=TalentStats()
    )
```

---

## Conventions de Code

### Style Python

- **PEP 8** : Style guide Python
- **Type hints** : Toujours utiliser
- **Docstrings** : Format Google
- **Noms** : snake_case pour fonctions/variables, PascalCase pour classes

### Nommage

- **Variables** : Anglais, explicites
  ```python
  talent_service  # Bon
  ts              # Mauvais
  ```

- **Fonctions** : Verbe + nom
  ```python
  def get_talent(name: str) -> Talent:
      ...

  def list_all_vehicles() -> List[Vehicle]:
      ...
  ```

- **Classes** : Nom au singulier
  ```python
  class TalentService:  # Bon
  class TalentsService: # Mauvais
  ```

### Docstrings

```python
def create_championship(name: str, vehicles: List[Vehicle]) -> Championship:
    """
    Crée un nouveau championnat custom.

    Args:
        name: Nom du championnat (ex: "MyChampionship2025")
        vehicles: Liste des véhicules à inclure

    Returns:
        Championship: Le championnat créé

    Raises:
        ValueError: Si le nom est invalide
        FileExistsError: Si le championnat existe déjà
    """
    ...
```

### Gestion d'Erreurs

- **Lever des exceptions** pour les erreurs critiques
- **Retourner None** ou valeurs par défaut pour les cas normaux
- **Logger** les erreurs avec le module `logging`

```python
import logging

logger = logging.getLogger(__name__)

def parse_file(path: str) -> Optional[Model]:
    if not os.path.exists(path):
        logger.warning(f"File not found: {path}")
        return None

    try:
        return Parser.parse(path)
    except Exception as e:
        logger.error(f"Parse error: {e}")
        raise ValueError(f"Invalid file: {path}")
```

### Encodage

**TOUJOURS** utiliser `windows-1252` pour les fichiers rFactor :

```python
# Lecture
with open(file_path, 'r', encoding='windows-1252') as f:
    content = f.read()

# Écriture
with open(file_path, 'w', encoding='windows-1252') as f:
    f.write(content)
```

### Validation

**Toujours** valider les données :

```python
from pydantic import BaseModel, validator

class TalentStats(BaseModel):
    speed: float = 50.0
    aggression: float = 50.0

    @validator('speed', 'aggression')
    def validate_stat(cls, v):
        if not 0.0 <= v <= 100.0:
            raise ValueError("Stat must be between 0 and 100")
        return v
```

---

## Ressources

### Documentation Externe

- **FastAPI** : https://fastapi.tiangolo.com/
- **Pydantic** : https://docs.pydantic.dev/
- **Pytest** : https://docs.pytest.org/

### Documentation Interne

- **Formats de fichiers** : `FILE_FORMATS.md`
- **Spécifications** : `SPECIFICATIONS.md`
- **Guide utilisateur** : `USER_GUIDE.md`
- **Changelog** : `CHANGELOG.md`

---

**Version** : 1.0 (Novembre 2025)
**Projet** : rFactor Championship Creator
