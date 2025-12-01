# Sprint 5 - État Actuel et Tâches Restantes

**Dernière mise à jour** : 28 novembre 2025

---

## ✅ Sprint 5 - Corrections Complétées

### 1. Bouton "Créer un nouveau talent" ✅ CORRIGÉ
**Status** : Fonctionnel

- ✅ Route `/talents/new` implémentée (app.py:56-59)
- ✅ Formulaire complet avec tous les champs (talents/form.html)
- ✅ API POST `/api/talents/` fonctionnelle
- ✅ Validation côté client et serveur
- ✅ Sliders interactifs pour les statistiques
- ✅ Redirection après création

### 2. Cliquer sur un talent ✅ CORRIGÉ
**Status** : Fonctionnel

- ✅ Route `/talents/{name}` implémentée (app.py:68-77)
- ✅ Page de détails complète (talents/detail.html)
- ✅ Utilise `encodeURIComponent()` pour gérer les espaces
- ✅ Bouton "Éditer" présent
- ✅ Affichage des statistiques avec barres de progression colorées

### 3. Formulaire d'édition de talent ✅ CORRIGÉ
**Status** : Fonctionnel

- ✅ Route `/talents/{name}/edit` implémentée (app.py:62-65)
- ✅ Même formulaire que création, mode "edit"
- ✅ Pré-remplissage des données existantes
- ✅ Nom du talent en lecture seule (non modifiable)
- ✅ API PUT `/api/talents/{name}` fonctionnelle

### 4. Statut des championnats ✅ CORRIGÉ
**Status** : Correct

- ✅ Mapping confirmé : 0=Non démarré, 1=Inconnu, 2=En cours
- ✅ Commentaire explicite dans le code (championships/detail.html:35-36)
- ✅ Affichage avec badges colorés

### 5. Informations des championnats ✅ ENRICHI
**Status** : Très complet

L'API `/api/championships/{name}` retourne maintenant **TOUTES** les données :

- ✅ **Informations générales** : statut, course actuelle
- ✅ **Joueur** : nom, véhicule, points, position, poles
- ✅ **Options de jeu** (19+ paramètres) :
  - Tours, durée, critère de fin
  - Force IA, nombre d'opposants
  - Dégâts, usure pneus, consommation carburant
  - Taux de pannes mécaniques
  - Récupération après crash, réglages libres
- ✅ **Conditions de course** (13+ paramètres) :
  - Météo, échelle de temps
  - Reconnaissance, formation, walkthrough
  - Heure de départ, échelle temps
  - Drapeaux, safety car, parc fermé
- ✅ **Opposants** : liste complète avec liens vers talents/véhicules
- ✅ **Entrées véhicules** : détails de tous les véhicules du championnat
- ✅ **Statistiques circuits** : avec badges (Terminée/En cours/À venir)
- ✅ **Statistiques carrière** : expérience, argent, courses, victoires, poles, etc.

### 6. Gestion des véhicules ✅ IMPLÉMENTÉ
**Status** : Fonctionnel

- ✅ VehicleService existe (src/services/vehicle_service.py)
- ✅ Parser VEH complet (src/parsers/veh_parser.py)
- ✅ Modèle Vehicle (src/models/vehicle.py)
- ✅ API `/api/vehicles/` complète (routes/vehicles.py)
- ✅ Page de liste véhicules (vehicles/list.html)
- ✅ Page de détails véhicule (vehicles/detail.html)
- ✅ Filtrage par classe, fabricant, recherche

### 7. Gestion des circuits ✅ IMPLÉMENTÉ
**Status** : Fonctionnel

- ✅ TrackService existe (src/services/track_service.py)
- ✅ Parser GDB complet (src/parsers/gdb_parser.py)
- ✅ Modèle Track (src/models/track.py)
- ✅ API `/api/tracks/` complète (routes/tracks.py)
- ✅ Page de liste circuits (tracks/list.html)
- ✅ Page de détails circuit (tracks/detail.html)
- ✅ Recherche de circuits

---

## ❌ Fonctionnalités NON Implémentées

### 1. Création de Championnats Custom via Interface ❌ BLOQUANT

**Status** : ❌ NON IMPLÉMENTÉ

**Ce qui manque** :

1. **Page de création** : Pas de `/championships/new`
2. **API de création** : Route POST existe mais retourne `501 NOT_IMPLEMENTED`
   ```python
   # championships.py:210-213
   raise HTTPException(
       status_code=status.HTTP_501_NOT_IMPLEMENTED,
       detail="Championship creation via API not yet fully implemented."
   )
   ```

3. **Parser/Générateur RFM** : ❌ Non implémenté
   - `src/parsers/rfm_parser.py` n'existe pas
   - `src/generators/rfm_generator.py` n'existe pas
   - `src/models/rfm.py` n'existe pas

4. **Système d'isolation de véhicules** : ❌ Non implémenté
   - Pas de copie automatique dans `RFTOOL_<Name>/`
   - Pas de modification des champs `Classes` et `Driver`

**Dépendances** :
- Modèle de données RFM
- Parser RFM (lecture de fichiers .rfm existants)
- Générateur RFM (création de nouveaux fichiers .rfm)
- Service de création de championnats (championship_creator.py)
- Système d'isolation de véhicules

**Impact** : Objectif principal du projet NON atteint

---

## 📋 Plan d'Action - Prochaines Étapes

### Option A : Implémentation Complète de la Création de Championnats

**Temps estimé** : 15-20h

#### Étape 1 : Modèle RFM (3-4h)
- [ ] Créer `src/models/rfm.py`
- [ ] Modèles pour : RFMod, Season, SceneOrder, Scoring
- [ ] Validation Pydantic

#### Étape 2 : Parser RFM (3-4h)
- [ ] Créer `src/parsers/rfm_parser.py`
- [ ] Parser pour structure RFM complexe
- [ ] Gestion des sections imbriquées
- [ ] Tests unitaires

#### Étape 3 : Générateur RFM (3-4h)
- [ ] Créer `src/generators/rfm_generator.py`
- [ ] Génération de fichiers .rfm valides
- [ ] Respect du format rFactor
- [ ] Tests de round-trip (parse → generate → parse)

#### Étape 4 : Système d'Isolation de Véhicules (3-4h)
- [ ] Service de copie de véhicules vers `RFTOOL_<Name>/`
- [ ] Modification du champ `Classes`
- [ ] Modification du champ `Driver`
- [ ] Copie des assets (textures DDS, etc.)
- [ ] Préservation de la structure des dossiers

#### Étape 5 : Interface de Création (4-6h)
- [ ] Page `/championships/new` (formulaire multi-étapes)
  - Étape 1 : Nom et paramètres de base
  - Étape 2 : Sélection des opposants (talents)
  - Étape 3 : Association pilote-véhicule
  - Étape 4 : Sélection et ordre des circuits
  - Étape 5 : Configuration avancée (options de jeu, conditions)
- [ ] API POST `/api/championships/` fonctionnelle
- [ ] Validation complète
- [ ] Service `ChampionshipCreatorService`

### Option B : Interface de Consultation + Scripts Python

**Temps estimé** : 2-3h

- [x] Interface web pour consultation (DÉJÀ FAIT)
- [x] Scripts Python pour création (DÉJÀ EXISTANTS dans demos)
- [ ] Documentation utilisateur pour scripts
- [ ] Amélioration des scripts de démo

### Option C : Approche Hybride

**Temps estimé** : 8-12h

- [ ] Parser RFM (lecture seulement)
- [ ] Interface basique de création (paramètres simples)
- [ ] Export des paramètres en JSON
- [ ] Script Python qui lit le JSON et génère le .rfm
- [ ] Meilleure intégration scripts ↔ interface

---

## 📊 Résumé de l'État Actuel

### ✅ Fonctionnalités Complètes

| Fonctionnalité | Status | Routes API | Interface Web |
|----------------|--------|------------|---------------|
| **Gestion Talents** | ✅ Complet | GET, POST, PUT, DELETE | Liste, Détails, Création, Édition |
| **Visualisation Championnats** | ✅ Complet | GET, DELETE, POST (duplicate) | Liste, Détails complets |
| **Gestion Véhicules** | ✅ Complet | GET (list, detail) | Liste, Détails, Filtrage |
| **Gestion Circuits** | ✅ Complet | GET (list, detail) | Liste, Détails, Recherche |
| **Import/Export CSV** | ✅ Complet | POST (import), GET (export) | Page import avec validation |

### ❌ Fonctionnalités Manquantes

| Fonctionnalité | Status | Blocage |
|----------------|--------|---------|
| **Création Championnats** | ❌ Non implémenté | Parser/Générateur RFM manquants |
| **Isolation Véhicules** | ❌ Non implémenté | Service de copie manquant |
| **Édition Championnats** | ❌ Non implémenté | Dépend de la création |

### 📈 Statistiques

- **Tests unitaires** : 68 passants
- **Routes API** : ~20 endpoints fonctionnels
- **Pages web** : ~15 pages complètes
- **Services** : 5/6 implémentés (ChampionshipCreator manquant)
- **Parsers** : 4/5 implémentés (RFM manquant)
- **Générateurs** : 2/3 implémentés (RFM manquant)

---

## 🎯 Recommandation

**Pour l'utilisateur** :

1. **Court terme** : Utiliser l'interface web pour gérer les talents et consulter les championnats
2. **Création de championnats** : Utiliser les scripts Python existants (demos)
3. **Long terme** : Décider si l'implémentation complète de la création via web vaut l'investissement (15-20h)

**Approche suggérée** : Option B ou C
- L'interface web actuelle est déjà très complète pour la consultation
- Les scripts Python fonctionnent bien pour la création
- Option B = documenter les scripts existants
- Option C = créer un pont interface ↔ scripts

---

## 📝 Notes Techniques

### Fichiers à créer pour Option A

```
src/models/rfm.py              # Modèles de données RFM
src/parsers/rfm_parser.py      # Parser fichiers .rfm
src/generators/rfm_generator.py # Générateur fichiers .rfm
src/services/championship_creator.py # Service création championnats
tests/test_rfm_parser.py       # Tests parser
tests/test_rfm_generator.py    # Tests générateur
```

### Format RFM - Points Clés

```rfm
// Structure minimale d'un .rfm
Mod Name = Championship Name
Vehicle Filter = RFTOOL_ChampName
Track Filter = *
Max Opponents = 19

Season = Season Name
{
  Vehicle Filter = RFTOOL_ChampName
  SceneOrder
  {
    Track1_Name
    Track2_Name
  }
}

DefaultScoring { ... }
```

### Système de Préfixe

- **Préfixe global** : `RFTOOL_`
- **Nom complet** : `RFTOOL_<ChampionshipName>`
- **Utilisation** :
  - Nom du fichier .rfm
  - Dossier des véhicules isolés
  - Valeur de `Vehicle Filter`
  - Valeur de `Classes` dans les .veh modifiés
