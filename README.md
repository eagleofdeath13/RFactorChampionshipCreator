# rFactor Championship Creator

**Éditeur de championnats personnalisés pour rFactor**

## Description

rFactor Championship Creator est une application web Python qui permet de créer, éditer et gérer des championnats personnalisés pour le jeu de simulation automobile rFactor. L'application offre une interface intuitive pour :

- Créer et modifier des championnats
- Gérer les pilotes (talents) et leurs caractéristiques
- Sélectionner et assigner des véhicules
- Configurer les circuits et l'ordre des courses
- Importer des listes de pilotes depuis des fichiers CSV
- Exporter des configurations de championnat

## Statut du Projet

**Version Actuelle** : 1.0.0 (28 Novembre 2025) 🎉

### ✅ Fonctionnalités Complètes

- [x] **Gestion des talents** - CRUD complet, import/export CSV
- [x] **Gestion des championnats** - Lecture, duplication, suppression
- [x] **Création de championnats custom** - Interface complète avec isolation véhicules
- [x] **Gestion des véhicules** - Liste, recherche, filtrage
- [x] **Gestion des circuits** - Liste, recherche
- [x] **Interface web FastAPI** - 20+ endpoints, 15+ pages HTML
- [x] **Import/Export CSV** - Template, validation, rapports d'erreurs
- [x] **Système de configuration** - Détection auto rFactor, validation
- [x] **Système d'isolation véhicules** - Renommage avec préfixe (évite doublons)

**Tests** : 68 tests passants | **API** : 20+ endpoints REST | **Pages** : 15+ HTML

### 🔄 À Venir (v1.1.0)

- [ ] Package PyInstaller (exécutable standalone)
- [ ] Tests in-game rFactor (validation finale)
- [ ] Documentation vidéo
- [ ] Support multi-profils

## Structure du projet

```
RFactorChampionshipCreator/
├── RFactorFiles/              # Fichiers extraits du jeu rFactor
│   ├── GameData/
│   │   ├── Talent/            # Fichiers de pilotes (.rcd)
│   │   ├── Vehicles/          # Fichiers de véhicules (.veh)
│   │   └── Locations/         # Fichiers de circuits (.gdb)
│   └── UserData/
│       └── [Player]/          # Fichiers de championnat (.cch)
├── src/                       # Code source (à venir)
├── docs/                      # Documentation
├── FILE_FORMATS.md            # Documentation détaillée des formats
├── SPECIFICATIONS.md          # Spécifications du projet
├── CLAUDE.md                  # Contexte pour Claude AI
└── README.md                  # Ce fichier
```

## Documentation

### 📚 Guides Principaux

- **[USER_GUIDE.md](USER_GUIDE.md)** - Guide utilisateur complet (installation, utilisation, dépannage)
- **[DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md)** - Guide développeur (architecture, composants, tests)
- **[CHANGELOG.md](CHANGELOG.md)** - Historique des versions et changements

### 📖 Documentation Technique

- **[SPECIFICATIONS.md](SPECIFICATIONS.md)** - Spécifications fonctionnelles et techniques
- **[FILE_FORMATS.md](FILE_FORMATS.md)** - Formats de fichiers rFactor (.cch, .rcd, .veh, .gdb, .rfm)
- **[CLAUDE.md](CLAUDE.md)** - Contexte développement (pour Claude AI)

### 📁 Archives

- **docs/archive/** - Documentation de travail et historique sprints

## Formats de fichiers rFactor

### Fichier de championnat (`.cch`)
Fichier texte au format INI étendu contenant :
- Configuration du championnat (nom, règles, options)
- Liste des pilotes participants
- Véhicules assignés
- Statistiques et progression

### Fichier de talent (`.rcd`)
Fichier texte définissant un pilote avec :
- Informations personnelles (nom, nationalité, date de naissance)
- Statistiques (agressivité, vitesse, sang-froid, etc.)
- Palmarès (départs, victoires, poles)

### Fichier de véhicule (`.veh`)
Fichier texte au format INI contenant :
- Références aux fichiers de physique et graphismes
- Informations de l'équipe
- Numéro et livrée
- Pilote par défaut

### Fichier de circuit (`.gdb`)
Fichier texte définissant un circuit avec :
- Informations du circuit (nom, localisation, longueur)
- Configuration de l'environnement (météo, éclairage)
- Paramètres par défaut (nombre de tours, temps)

## Technologies

- **Backend** : Python 3.8+
- **Framework Web** : FastAPI (avec Uvicorn)
- **Frontend** : HTML/CSS/JavaScript + Bootstrap 5
- **Templates** : Jinja2
- **Validation** : Pydantic
- **Tests** : Pytest
- **Packaging** : PyInstaller (à venir)

## Installation

### Prérequis
- Python 3.8 ou supérieur
- Installation de rFactor

### Installation des dépendances
```bash
pip install -r requirements.txt
```

### Configuration
```bash
python setup_config.py
```

Le script de configuration :
- Détecte automatiquement votre installation rFactor
- Configure le profil de joueur à utiliser
- Valide les chemins et dossiers requis

## Utilisation

### Lancer l'Application

#### Méthode 1 : Script de Démarrage (Recommandé)
```bash
start.bat
```

#### Méthode 2 : Lancement Manuel
```bash
python -m uvicorn src.web.app:app --host 127.0.0.1 --port 5000 --reload
```

### Accès à l'Application

- **Interface Web** : http://localhost:5000
- **Documentation API** : http://localhost:5000/api/docs
- **ReDoc** : http://localhost:5000/api/redoc

### Guide d'Utilisation Complet

Consultez le **[USER_GUIDE.md](USER_GUIDE.md)** pour :
- Configuration détaillée
- Utilisation de l'interface web
- Création de championnats custom
- Import/Export CSV
- Dépannage

## Fonctionnalités Principales

### ✅ Gestion des Talents
- CRUD complet (Create, Read, Update, Delete)
- Import/Export CSV avec validation
- Recherche et filtrage
- Interface web intuitive

### ✅ Gestion des Championnats
- Lecture de championnats existants (.cch)
- Détails enrichis (opposants, circuits, statistiques)
- Duplication et suppression
- Interface web complète

### ✅ Création de Championnats Custom
- Formulaire multi-étapes
- Sélection de véhicules originaux
- Association pilotes ↔ véhicules
- Sélection et ordre des circuits
- **Isolation automatique des véhicules** (système de renommage)
- Génération fichiers `.rfm`
- **Évite les doublons** détectés par rFactor

### ✅ Gestion des Véhicules
- Liste complète avec cache
- Filtrage par classe, fabricant
- Recherche
- Interface web

### ✅ Gestion des Circuits
- Liste complète
- Recherche
- Interface web

Pour l'historique complet des versions, voir **[CHANGELOG.md](CHANGELOG.md)**

## Contribuer

Ce projet est en développement actif. Les contributions sont les bienvenues une fois la base du code établie.

## Licence

*À définir*

## Auteur

Loïc

## Notes importantes

- **Compatibilité** : L'application génère des fichiers compatibles avec rFactor
- **Sauvegarde** : Toujours sauvegarder les fichiers originaux avant modification
- **Encodage** : Les fichiers rFactor utilisent l'encodage Windows-1252 ou ASCII
- **Chemins** : Les chemins sont relatifs au dossier `RFactorFiles/`

## Support

- **Guide Utilisateur** : [USER_GUIDE.md](USER_GUIDE.md) - Dépannage et FAQ
- **Guide Développeur** : [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md) - Architecture et développement
- **Documentation API** : http://localhost:5000/api/docs (quand l'app est lancée)

## Liens Rapides

- 📘 [Guide Utilisateur](USER_GUIDE.md) - Installation, utilisation, dépannage
- 💻 [Guide Développeur](DEVELOPER_GUIDE.md) - Architecture, tests, contribution
- 📋 [Changelog](CHANGELOG.md) - Historique des versions
- 📖 [Spécifications](SPECIFICATIONS.md) - Spécifications techniques
- 📝 [Formats de Fichiers](FILE_FORMATS.md) - Documentation formats rFactor

---

**Version** : 1.0.0 (28 Novembre 2025)
**Statut** : ✅ Version complète fonctionnelle | 68 tests passants | 20+ endpoints API | 15+ pages web
