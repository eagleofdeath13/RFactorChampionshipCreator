# 🏎️ rFactor Championship Creator - React Frontend

Interface React moderne pour la gestion de championnats rFactor.

## 🚀 Stack Technique

- **React 18** - Framework UI
- **Vite** - Build tool ultra-rapide
- **Tailwind CSS** - Styling moderne
- **React Router v6** - Navigation
- **TanStack Query (React Query)** - Gestion des données API
- **Framer Motion** - Animations fluides
- **Lucide React** - Icônes modernes
- **Axios** - Client HTTP
- **React Hot Toast** - Notifications

## 📦 Installation

Les dépendances sont déjà installées. Si besoin :

```bash
npm install
```

## 🏁 Lancement

### 1. Démarrer le backend FastAPI

Dans le dossier racine du projet :

```bash
python -m uvicorn src.web.app:app --reload --port 5000
```

### 2. Démarrer le frontend React

Dans le dossier `frontend/` :

```bash
npm run dev
```

Le frontend sera accessible sur **http://localhost:3000**

L'API backend sera accessible sur **http://localhost:5000**

## 🎨 Thème Racing

L'interface utilise un thème "Racing Dashboard" custom avec :

- **Couleurs** : Rouge racing (#E31E24), noir carbone, argent chromé
- **Typography** : Orbitron (titres), Rajdhani (corps)
- **Animations** : Framer Motion pour des transitions fluides
- **Design** : Inspiré de F1 TV, iRacing, Gran Turismo

## 📁 Structure

```
frontend/
├── src/
│   ├── components/         # Composants réutilisables
│   │   ├── Layout.jsx      # Layout principal
│   │   └── Navigation.jsx  # Barre de navigation
│   ├── pages/              # Pages/routes
│   │   └── Dashboard.jsx   # Dashboard principal
│   ├── services/           # Services API
│   │   └── api.js          # Client API Axios
│   ├── App.jsx             # Composant racine
│   ├── main.jsx            # Point d'entrée
│   └── index.css           # Styles Tailwind
├── index.html
├── vite.config.js          # Config Vite
├── tailwind.config.js      # Config Tailwind
└── package.json
```

## 🔧 Scripts Disponibles

```bash
npm run dev      # Démarre le serveur de développement
npm run build    # Build de production
npm run preview  # Prévisualise le build de production
npm run lint     # Lint du code
```

## 🌐 Proxy API

Vite est configuré pour proxifier les requêtes `/api/*` vers `http://localhost:5000` en développement.

## 🎯 Fonctionnalités Actuelles

✅ Dashboard avec statistiques animées
✅ Navigation moderne avec indicateurs actifs
✅ Intégration React Query pour les données API
✅ Thème racing complet (Tailwind + CSS custom)
✅ Animations Framer Motion
✅ Toast notifications

## 🚧 À Venir

- [ ] Pages Talents
- [ ] Pages Championships
- [ ] Page de création de championnats (formulaire multi-étapes)
- [ ] Pages Vehicles & Tracks
- [ ] Page Import CSV
- [ ] Page Configuration

## 🏗️ Build Production

```bash
npm run build
```

Les fichiers de production seront dans `dist/`

Pour servir le frontend depuis FastAPI en production, copiez le contenu de `dist/` dans un dossier public et montez-le avec FastAPI.
