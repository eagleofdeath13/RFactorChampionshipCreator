# 🚀 Guide de Démarrage Rapide

## Prérequis

✅ Python 3.12+ installé
✅ Node.js 18+ et npm installés
✅ `uv` installé (gestionnaire de packages Python)

## Première Installation

### 1. Installer les dépendances Python

```bash
uv sync
```

Cette commande installe automatiquement toutes les dépendances Python listées dans `pyproject.toml`.

### 2. Installer les dépendances Frontend

```bash
cd frontend
npm install
cd ..
```

## Lancement de l'Application

### Option 1 : Script Automatique (Recommandé)

Double-cliquez sur `start.bat` ou lancez depuis un terminal :

```bash
start.bat
```

Ce script :
- ✅ Vérifie automatiquement les dépendances Python et npm
- ✅ Installe les dépendances manquantes
- ✅ Lance le backend FastAPI (port 5000) dans une fenêtre séparée
- ✅ Lance le frontend React/Vite (port 3000) dans une fenêtre séparée

**Les deux serveurs s'ouvrent dans des fenêtres cmd séparées** avec les titres :
- "Backend - FastAPI"
- "Frontend - React"

### Option 2 : Lancement Manuel

**Terminal 1 - Backend :**
```bash
python -m uvicorn src.web.app:app --reload --port 5000
```

**Terminal 2 - Frontend :**
```bash
cd frontend
npm run dev
```

## Accès à l'Application

Une fois les serveurs lancés :

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend React** | http://localhost:3000 | Interface utilisateur principale |
| **API Backend** | http://localhost:5000/api | API REST FastAPI |
| **Documentation API** | http://localhost:5000/api/docs | Documentation Swagger interactive |

## Vérification

Pour vérifier que tout fonctionne :

```bash
# Vérifier le backend
curl http://localhost:5000/health

# Devrait retourner:
# {"status":"ok","service":"rFactor Championship Creator"}
```

Ouvrez http://localhost:3000 dans votre navigateur pour accéder à l'interface React.

## Architecture Dev vs Prod

### Mode Développement (2 serveurs)

- **Frontend** : Vite dev server (http://localhost:3000)
  - Hot Module Replacement (HMR) instantané
  - React DevTools actif
  - Source maps complets

- **Backend** : FastAPI (http://localhost:5000)
  - Auto-reload sur changements
  - CORS configuré pour localhost:3000

Le frontend Vite proxifie automatiquement les requêtes `/api/*` vers le backend FastAPI.

### Mode Production (1 serveur)

```bash
# 1. Build le frontend React
cd frontend
npm run build
cd ..

# 2. Lance FastAPI (sert React + API)
python -m uvicorn src.web.app:app --port 5000
```

FastAPI sert automatiquement le build React depuis `/frontend/dist/` et répond aux requêtes API sur `/api/*`.

Accès : http://localhost:5000

## Résolution de Problèmes

### "No module named uvicorn"

**Cause** : Dépendances Python non installées dans le venv.

**Solution** :
```bash
uv sync
```

### "npm: command not found" ou "node_modules manquant"

**Cause** : Node.js pas installé ou dépendances npm manquantes.

**Solution** :
```bash
cd frontend
npm install
cd ..
```

### Port déjà utilisé

Si les ports 3000 ou 5000 sont déjà utilisés :

**Windows** :
```bash
# Trouver le processus utilisant le port
netstat -ano | findstr :3000
netstat -ano | findstr :5000

# Tuer le processus (remplacer PID)
taskkill /PID <PID> /F
```

### Les fenêtres cmd se ferment immédiatement

**Cause** : Erreur au démarrage (dépendances manquantes, config invalide).

**Solution** :
1. Vérifier que `uv sync` a été exécuté
2. Vérifier que `config.json` existe (le script le crée automatiquement)
3. Lancer manuellement pour voir les erreurs

## Structure du Projet

```
RFactorChampionshipCreator/
├── frontend/              # Application React
│   ├── src/
│   │   ├── components/    # Composants réutilisables
│   │   ├── pages/         # Pages de l'application
│   │   ├── services/      # Client API Axios
│   │   └── App.jsx
│   ├── package.json
│   └── vite.config.js
│
├── src/                   # Backend Python FastAPI
│   ├── web/
│   │   ├── app.py         # Application FastAPI
│   │   └── routes/        # Routes API
│   ├── services/          # Logique métier
│   ├── models/            # Modèles de données
│   └── parsers/           # Parsers rFactor
│
├── start.bat              # Script de lancement automatique
├── pyproject.toml         # Dépendances Python (uv)
├── config.json            # Configuration rFactor
└── README.md
```

## Commandes Utiles

### Frontend
```bash
cd frontend
npm run dev      # Dev server (HMR)
npm run build    # Build production
npm run preview  # Preview du build
npm run lint     # Linter ESLint
```

### Backend
```bash
python -m uvicorn src.web.app:app --reload  # Dev avec auto-reload
python -m uvicorn src.web.app:app           # Prod
python -m pytest                             # Tests unitaires
```

### Gestion des dépendances
```bash
uv add <package>       # Ajouter une dépendance Python
uv sync                # Synchroniser les dépendances
uv lock                # Mettre à jour le lockfile
```

## Documentation Complète

- 📖 [START_HERE.md](START_HERE.md) - Guide détaillé dev/prod
- 📖 [MIGRATION_SUMMARY.md](frontend/MIGRATION_SUMMARY.md) - Détails de la migration React
- 📖 [CLAUDE.md](CLAUDE.md) - Contexte projet pour développement

---

**Prêt à créer des championnats rFactor ! 🏎️**
