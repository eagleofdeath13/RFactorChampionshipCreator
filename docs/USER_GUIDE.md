# Guide Utilisateur - rFactor Championship Creator

## 📖 Table des Matières

1. [Installation et Configuration](#installation-et-configuration)
2. [Démarrage de l'Application](#démarrage-de-lapplication)
3. [Interface Web](#interface-web)
4. [Gestion des Talents (Pilotes)](#gestion-des-talents-pilotes)
5. [Gestion des Championnats](#gestion-des-championnats)
6. [Import/Export CSV](#importexport-csv)
7. [Création de Championnats Custom](#création-de-championnats-custom)
8. [Dépannage](#dépannage)

---

## Installation et Configuration

### Prérequis

- **Python 3.8 ou supérieur**
- **rFactor** installé sur votre ordinateur
- Espace disque : ~50 MB pour l'application

### Installation

1. Télécharger ou cloner le projet
2. Installer les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

### Configuration Initiale

Lors du premier lancement, vous devez configurer l'application :

```bash
python scripts/setup_config.py
```

#### Étapes de Configuration

1. **Détection automatique de rFactor**
   - Le script recherche automatiquement rFactor dans les emplacements courants :
     - `C:/Program Files (x86)/rFactor`
     - `C:/Program Files/rFactor`
     - Steam : `C:/Program Files (x86)/Steam/steamapps/common/rFactor`
   - Vous pouvez aussi entrer un chemin personnalisé

2. **Validation de l'installation**
   - Vérifie que rFactor est correctement installé
   - Compte les talents, véhicules et circuits disponibles

3. **Sélection du profil joueur**
   - Liste les profils existants dans `UserData/`
   - Permet d'en créer un nouveau

4. **Sauvegarde**
   - Crée le fichier `config.json` avec vos paramètres

#### Exemple de Configuration

```
============================================================
rFactor Championship Creator - Configuration Setup
============================================================

Found 1 potential rFactor installation:
  1. C:\Steam\steamapps\common\rFactor
  2. Enter custom path

Select installation (1-2): 1

[OK] Valid rFactor installation found!

Installation details:
  - Talents available: 232
  - Vehicles available: 272
  - Locations available: 39

Found 2 player profiles:
  1. Loic
  2. Player2

Select player profile: 1
[OK] Player profile set to: Loic

Configuration Complete!
```

---

## Démarrage de l'Application

### Méthode 1 : Script de Démarrage (Recommandé)

Double-cliquez sur `scripts/start.bat` ou exécutez :

```bash
scripts/start.bat
```

Le script va :
- Vérifier que Python est installé
- Vérifier la configuration (lance scripts/setup_config.py si nécessaire)
- Démarrer le serveur web

### Méthode 2 : Démarrage Manuel

```bash
python -m uvicorn src.web.app:app --host 127.0.0.1 --port 5000 --reload
```

### Accès à l'Application

Une fois démarré, l'application est accessible à :

- **Interface Web** : http://localhost:5000
- **Documentation API** : http://localhost:5000/api/docs
- **API Alternative** : http://localhost:5000/api/redoc

---

## Interface Web

### Dashboard (`/`)

Page d'accueil avec vue d'ensemble :
- Nombre de talents disponibles
- Nombre de championnats
- État de la configuration
- Accès rapide aux fonctionnalités principales

### Pages Disponibles

| Page | URL | Description |
|------|-----|-------------|
| Dashboard | `/` | Vue d'ensemble |
| Talents | `/talents` | Liste et gestion des pilotes |
| Détails Talent | `/talents/{name}` | Informations d'un pilote |
| Créer Talent | `/talents/form` | Formulaire de création |
| Championnats | `/championships` | Liste des championnats |
| Détails Championnat | `/championships/{name}` | Détails d'un championnat |
| Créer Championnat | `/championships/create` | Créateur de championnat |
| Véhicules | `/vehicles` | Liste des véhicules |
| Circuits | `/tracks` | Liste des circuits |
| Import CSV | `/import` | Import de pilotes |
| Configuration | `/config` | Paramètres de l'application |

---

## Gestion des Talents (Pilotes)

### Lister les Talents

**Page** : `/talents`

Fonctionnalités :
- Recherche en temps réel par nom
- Visualisation des statistiques (vitesse, agressivité, etc.)
- Filtrage et tri
- Export CSV
- Suppression

### Voir un Talent

**Page** : `/talents/{nom}`

Affiche :
- **Informations personnelles** : Nom, nationalité, date de naissance
- **Palmarès** : Départs, poles, victoires, championnats
- **Statistiques** : Barres de progression colorées
  - Vitesse (Speed)
  - Agressivité (Aggression)
  - Sang-froid (Composure)
  - Réputation (Reputation)
  - Courtoisie (Courtesy)
  - Récupération (Recovery)
  - Accidents (Crash - plus bas = mieux)

### Créer un Talent

**Page** : `/talents/form`

Formulaire avec :
1. **Informations de base**
   - Nom complet (requis)
   - Nationalité (requis)
   - Date de naissance (format : JJ-MM-AAAA)

2. **Palmarès** (optionnel)
   - Nombre de départs
   - Pole positions
   - Victoires
   - Championnats remportés

3. **Statistiques** (0-100, défaut : 50)
   - Speed (Vitesse)
   - Aggression (Agressivité)
   - Composure (Sang-froid)
   - Reputation (Réputation)
   - Courtesy (Courtoisie)
   - Recovery (Récupération)
   - Crash (Accidents - plus bas = mieux)
   - Completed Laps (% tours complétés)
   - Min Racing Skill (Compétence minimale)

### Modifier un Talent

**Page** : `/talents/{nom}/edit`

Même formulaire que la création, pré-rempli avec les données existantes.

### Supprimer un Talent

**Bouton** : Sur la page de liste ou de détails

⚠️ **Attention** : La suppression est définitive !

---

## Gestion des Championnats

### Lister les Championnats

**Page** : `/championships`

Affiche pour chaque championnat :
- **Nom** et statut (Non démarré, En cours, Terminé)
- **Points** du joueur et position
- **Nombre d'opposants**
- **Dernière course**
- Actions : Voir détails, Dupliquer, Supprimer

### Voir un Championnat

**Page** : `/championships/{nom}`

Sections détaillées :

1. **Informations générales**
   - Nom du championnat
   - Statut et progression
   - Points et classement

2. **Options de jeu** (19+ paramètres)
   - Difficulté IA
   - Aides de conduite
   - Dégâts
   - Météo, etc.

3. **Conditions de course** (13+ paramètres)
   - Nombre de tours
   - Durée des séances
   - Règles de qualification

4. **Liste des opposants**
   - Noms cliquables (lien vers talent)
   - Statistiques de chaque pilote
   - Points actuels

5. **Circuits**
   - Liste ordonnée des circuits
   - Statut : Terminée / En cours / À venir
   - Résultats (si disponible)

6. **Statistiques carrière**
   - Total de courses
   - Victoires, poles, podiums
   - Meilleur tour, etc.

### Dupliquer un Championnat

**Bouton** : "Dupliquer" sur la page de liste

Permet de :
- Créer une copie avec un nouveau nom
- Garder tous les paramètres
- Réinitialiser la progression

### Supprimer un Championnat

**Bouton** : "Supprimer" sur la page de liste ou détails

⚠️ **Attention** : Supprime uniquement les championnats dans `UserData/` (pas les originaux)

---

## Import/Export CSV

### Format CSV

#### Colonnes Requises

| Colonne | Format | Exemple |
|---------|--------|---------|
| `name` | Texte | "Jean Dupont" |
| `nationality` | Texte | "France" |
| `date_of_birth` | JJ-MM-AAAA | "15-03-1990" |

#### Colonnes Optionnelles

**Palmarès** :
- `starts` - Nombre de départs (entier)
- `poles` - Pole positions (entier)
- `wins` - Victoires (entier)
- `drivers_championships` - Championnats (entier)

**Statistiques** (0.0-100.0) :
- `speed` - Vitesse
- `aggression` - Agressivité
- `composure` - Sang-froid
- `reputation` - Réputation
- `courtesy` - Courtoisie
- `recovery` - Récupération
- `crash` - Accidents (plus bas = mieux)
- `completed_laps` - % tours complétés
- `min_racing_skill` - Compétence minimale

#### Exemple CSV

```csv
name,nationality,date_of_birth,starts,poles,wins,speed,aggression,composure
Jean Dupont,France,15-03-1985,100,10,5,90.0,75.0,85.0
Hans Mueller,Germany,22-07-1990,50,3,1,75.0,60.0,70.0
Mario Rossi,Italy,10-12-1988,75,8,4,85.0,80.0,78.0
```

### Télécharger un Template

**Page** : `/import`
**Bouton** : "Télécharger le template CSV"

Télécharge un fichier avec :
- Tous les en-têtes de colonnes
- 2 exemples de pilotes
- Format correct

### Importer des Talents

**Page** : `/import`

#### Étapes

1. **Préparer le CSV**
   - Utiliser le template ou créer votre propre fichier
   - Encoder en UTF-8
   - Respecter le format des colonnes

2. **Valider (Optionnel)**
   - Cocher "Valider uniquement (ne pas importer)"
   - Upload le fichier
   - Vérifier les erreurs

3. **Importer**
   - Upload le fichier CSV
   - Choisir l'option :
     - ☑ "Ignorer les talents existants" : Ne pas écraser
     - ☐ "Écraser les talents existants"
   - Cliquer "Importer"

4. **Rapport**
   - Nombre de talents importés
   - Erreurs détaillées (ligne + raison)
   - Talents ignorés/écrasés

#### Erreurs Courantes

1. **Colonnes manquantes**
   ```
   Missing required columns: date_of_birth
   ```
   → Ajouter la colonne manquante

2. **Valeur hors limites**
   ```
   Row 8: speed must be between 0.0 and 100.0, got 150.0
   ```
   → Corriger la valeur

3. **Nom vide**
   ```
   Row 5: Name is required
   ```
   → Remplir la colonne name

4. **Talent existant**
   ```
   Row 3: Talent already exists (skipped)
   ```
   → Normal si "Ignorer existants" est coché

### Exporter des Talents

**Page** : `/talents`
**Bouton** : "Exporter tous les talents"

Télécharge un CSV avec :
- Tous les talents actuels
- Toutes les colonnes
- Format compatible pour réimport

**Usage** : Backup, partage, édition en masse dans Excel

---

## Création de Championnats Custom

### Vue d'ensemble

Créez vos propres championnats avec véhicules et pilotes personnalisés !

**Page** : `/championships/create`

### Étapes de Création

#### Étape 1 : Informations de Base

- **Nom du championnat** (requis)
  - Exemple : "MyChampionship2025"
  - Générera automatiquement `RFTOOL_MyChampionship2025`

- **Nom complet** (optionnel)
  - Exemple : "My Custom Championship 2025"

- **Description** (optionnel)

#### Étape 2 : Sélection des Véhicules

- **Liste des véhicules disponibles**
  - Filtrage par classe, équipe
  - Recherche par nom
  - Sélection multiple

- **Aperçu**
  - Nombre de véhicules sélectionnés
  - Classes représentées

#### Étape 3 : Association Pilotes ↔ Véhicules

Pour chaque véhicule sélectionné :
- **Sélectionner un pilote** depuis la liste des talents
- **Recherche** de pilote
- **Aperçu** : Nom pilote, véhicule, équipe

#### Étape 4 : Sélection et Ordre des Circuits

- **Liste des circuits disponibles**
  - Recherche par nom
  - Sélection multiple

- **Ordre des courses**
  - Glisser-déposer pour réorganiser
  - Numérotation automatique

#### Étape 5 : Options du Championnat

**Difficulté** :
- Niveau IA (0-100%)
- Agressivité IA

**Conditions de course** :
- Nombre de tours
- Durée qualification/warmup/practice
- Météo
- Dégâts
- Règlement

**Système de points** :
- 1ère place : X points
- 2ème place : Y points
- Etc.

#### Étape 6 : Validation et Création

- **Récapitulatif** complet
- **Vérification** des paramètres
- **Création** du championnat

### Résultat

L'outil génère :

1. **Dossier véhicules isolés**
   ```
   GameData/Vehicles/RFTOOL_MyChampionship2025/
   ```
   - Copies des véhicules sélectionnés
   - **Renommés avec préfixe** (ex: `MC_YEL_09.veh`)
   - Classes modifiées
   - Pilotes assignés
   - Assets renommés (`.dds`, `.txt`, etc.)

2. **Fichier .rfm**
   ```
   rFm/RFTOOL_MyChampionship2025.rfm
   ```
   - Définition du championnat
   - Liste des circuits
   - Filtres de véhicules
   - Options de jeu

### Lancer le Championnat dans rFactor

1. Ouvrir rFactor
2. Aller dans **Race → Championship**
3. Sélectionner votre championnat (ex: "My Championship 2025")
4. **Vérifier** que les véhicules sont disponibles et uniques
5. Démarrer la saison !

rFactor générera automatiquement le fichier `.cch` dans `UserData/{Player}/`

### Système de Préfixe Véhicules

Pour éviter les doublons détectés par rFactor, chaque championnat génère un **préfixe court** :

| Nom Championnat | Préfixe | Exemple Fichier |
|----------------|---------|-----------------|
| TestChampionship | TE | TE_GRN_08.veh |
| MyAwesomeChampionship | MAC | MAC_GRN_08.veh |
| SuperGT | SG | SG_GRN_08.veh |

Le préfixe est appliqué à :
- Nom du fichier `.veh`
- Champ `Description` dans le .veh
- Assets (`.dds`, `.txt`, etc.)
- Références (`DefaultLivery`, `PitCrewLivery`, `TrackLivery`)

**Avantage** : Les véhicules sont détectés comme uniques par rFactor !

---

## Dépannage

### Problèmes de Configuration

#### "Application not configured"

**Solution** :
```bash
python scripts/setup_config.py
```

#### "Invalid rFactor path"

**Vérifier** :
- rFactor est bien installé au chemin indiqué
- Le dossier contient `rFactor.exe`
- Les dossiers `GameData/` et `UserData/` existent

**Réinitialiser** :
```bash
python scripts/setup_config.py
```

### Problèmes de Serveur

#### Port 5000 déjà utilisé

**Modifier le port** dans `scripts/start.bat` :
```batch
python -m uvicorn src.web.app:app --host 127.0.0.1 --port 8000 --reload
```

Puis accéder à : http://localhost:8000

#### Erreur 404 sur les fichiers statiques

**Vérifier** que les dossiers existent :
```
src/web/static/css/
src/web/static/js/
```

### Problèmes de Données

#### Erreur de chargement des talents

**Vérifier** :
1. rFactor est installé au bon chemin
2. Le dossier `GameData/Talent/` existe
3. Le profil joueur est correct dans `config.json`

#### Erreur lors de l'import CSV

**Causes courantes** :
- Encodage du fichier (doit être UTF-8)
- Colonnes manquantes (name, nationality, date_of_birth)
- Format date incorrect (doit être JJ-MM-AAAA)
- Valeurs hors limites (stats entre 0-100)

**Solution** : Télécharger et utiliser le template officiel

#### Championnat créé non visible dans rFactor

**Vérifier** :
1. Le fichier `.rfm` existe dans `rFactor/rFm/`
2. Le nom commence par `RFTOOL_`
3. Les véhicules isolés existent dans `GameData/Vehicles/RFTOOL_XXX/`
4. Redémarrer rFactor

#### Véhicules détectés comme doublons

**Solution** : Le système de renommage avec préfixe doit résoudre ce problème.
Si le problème persiste, vérifier que :
- Les fichiers `.veh` ont bien le préfixe (ex: `TE_XXX.veh`)
- Le champ `Description` contient le préfixe
- Les assets (`.dds`) sont renommés avec le préfixe

### Problèmes de Performance

#### Chargement lent de la liste des véhicules

**Normal** : rFactor peut avoir des centaines de véhicules.
Le premier chargement peut prendre 5-10 secondes.

#### Interface Web lente

**Solutions** :
- Fermer les autres applications
- Vider le cache du navigateur
- Redémarrer le serveur

---

## Support et Aide

### Documentation Technique

- **Formats de fichiers** : Voir `FILE_FORMATS.md`
- **Spécifications** : Voir `SPECIFICATIONS.md`
- **Guide développeur** : Voir `DEVELOPER_GUIDE.md`

### Documentation API

Accéder à la documentation interactive :
- **Swagger UI** : http://localhost:5000/api/docs
- **ReDoc** : http://localhost:5000/api/redoc

### Fichiers de Logs

En cas de problème, vérifier :
- `srv.log` - Logs du serveur web
- Console Python - Messages d'erreur détaillés

---

## Bonnes Pratiques

### Avant de Créer un Championnat

1. **Créer tous les pilotes** nécessaires d'abord
2. **Vérifier** que les véhicules souhaités existent
3. **Tester** avec peu de courses d'abord
4. **Backup** : Exporter les talents en CSV

### Gestion des Talents

1. **Utiliser le CSV** pour import en masse
2. **Exporter régulièrement** pour backup
3. **Nommer clairement** les pilotes (éviter caractères spéciaux)

### Organisation

1. **Préfixer** vos championnats custom (automatique avec `RFTOOL_`)
2. **Documenter** : Utiliser les descriptions
3. **Tester in-game** après chaque création

---

**Version** : 1.0 (Novembre 2025)
**Projet** : rFactor Championship Creator
