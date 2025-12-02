# Guide des Scripts de Démarrage

## 📍 Emplacement des Scripts

Les scripts de démarrage sont situés à **deux endroits** :

### 1. **Racine du projet** (Recommandé pour l'utilisation)
```
RFactorChampionshipCreator/
├── start.bat          ← Script complet avec vérifications
└── start_dev.bat      ← Script rapide sans vérifications
```

### 2. **Dossier scripts/** (Scripts de développement)
```
RFactorChampionshipCreator/
└── scripts/
    ├── start.bat           ← Version dans scripts/
    ├── start_dev.bat       ← Version dans scripts/
    ├── kill_ports.bat      ← Outil pour libérer les ports
    └── setup_config.py     ← Configuration initiale
```

## 🚀 Utilisation

### Option 1 : `start.bat` (Production)

**Utilisation** : Double-clic sur `start.bat` à la racine du projet

**Ce qu'il fait** :
1. ✅ Vérifie Python est installé
2. ✅ Vérifie Node.js/npm est installé
3. ✅ Libère les ports 3000, 5000 si occupés
4. ✅ Installe les dépendances Python (via `uv sync`)
5. ✅ Installe les dépendances npm (si nécessaire)
6. ✅ Vérifie/crée `config.json` (via `scripts\setup_config.py`)
7. 🚀 Lance le backend FastAPI (port 5000)
8. 🚀 Lance le frontend React (port 3000)

**Avantages** :
- Tout est vérifié automatiquement
- Prêt à l'emploi même après un `git clone`
- Idéal pour les nouveaux utilisateurs

**Inconvénient** :
- Prend ~10-15 secondes de vérifications

### Option 2 : `start_dev.bat` (Développement)

**Utilisation** : Double-clic sur `start_dev.bat` à la racine du projet

**Ce qu'il fait** :
1. 🚀 Lance directement le backend FastAPI (port 5000)
2. 🚀 Lance directement le frontend React (port 3000)

**Avantages** :
- Démarrage ultra-rapide (~2 secondes)
- Idéal pour le développement (restart fréquent)

**Inconvénient** :
- Assume que tout est installé et configuré
- Peut échouer si dépendances manquantes

## 🔧 Cas d'Utilisation

### Première Installation
```bash
# Utilisez start.bat
start.bat
```

### Développement Quotidien
```bash
# Utilisez start_dev.bat pour gagner du temps
start_dev.bat
```

### Problèmes de Ports Occupés
```bash
# 1. Tuez les processus
scripts\kill_ports.bat

# 2. Relancez
start_dev.bat
```

### Problèmes de Configuration
```bash
# Reconfigurez manuellement
python scripts\setup_config.py

# Puis relancez
start_dev.bat
```

## 🌐 URLs de l'Application

Une fois les scripts lancés :

- **Frontend React** : http://localhost:3000
- **Backend API** : http://localhost:5000
- **Documentation API** : http://localhost:5000/api/docs
- **ReDoc** : http://localhost:5000/api/redoc

## ⚙️ Architecture

```
┌─────────────────────┐
│   Frontend React    │  Port 3000
│   (Vite dev server) │
└──────────┬──────────┘
           │ Proxy /api/*
           ▼
┌─────────────────────┐
│  Backend FastAPI    │  Port 5000
│  (Uvicorn server)   │
└─────────────────────┘
```

Le frontend React fait des requêtes au backend via un proxy configuré dans `vite.config.js`.

## 🛠️ Scripts Utilitaires

### `kill_ports.bat`
Libère les ports 3000 et 5000 :
```bash
scripts\kill_ports.bat
```

### `setup_config.py`
Configure l'application (chemins rFactor, profil joueur) :
```bash
python scripts\setup_config.py
```

## 📝 Notes Importantes

1. **Ordre de démarrage** : Le backend DOIT démarrer avant le frontend (pour le proxy)
2. **Windows uniquement** : Les scripts `.bat` sont pour Windows. Pour Linux/Mac, utilisez la commande manuelle
3. **Chemins relatifs** : Les scripts doivent être exécutés depuis la racine du projet
4. **Encoding** : Les scripts utilisent l'encodage Windows (CP850/1252)

## 🔍 Dépannage

### "Python n'est pas installé"
- Installez Python 3.8+ depuis python.org
- Ajoutez Python au PATH

### "Node.js/NPM n'est pas installé"
- Installez Node.js depuis nodejs.org
- Redémarrez le terminal

### "Port déjà utilisé"
```bash
# Solution 1 : Utilisez kill_ports.bat
scripts\kill_ports.bat

# Solution 2 : Trouvez et tuez manuellement
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

### "Module not found" (Python)
```bash
# Réinstallez les dépendances
uv sync

# Ou avec pip
pip install -r requirements.txt
```

### "Cannot find module" (npm)
```bash
# Réinstallez les dépendances
cd frontend
npm install
```

## 📦 Commandes Manuelles

Si vous préférez lancer manuellement :

```bash
# Terminal 1 : Backend
python -m uvicorn src.web.app:app --reload --port 5000

# Terminal 2 : Frontend
cd frontend
npm run dev
```

---

**Version** : 1.0.0
**Date** : 2 Décembre 2025
