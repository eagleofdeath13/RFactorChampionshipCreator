# 🏁 rFactor Championship Creator - Guide de Démarrage

## 🎯 2 Modes de Fonctionnement

### Mode 1 : Développement (2 serveurs) - RECOMMANDÉ POUR DEV
- **React Dev Server** (port 3000) - HMR ultra-rapide
- **FastAPI** (port 5000) - API backend

### Mode 2 : Production (1 seul serveur)
- **FastAPI** (port 5000) - Sert l'API + React build

---

## 🚀 Démarrage Rapide

### Option A : Développement (Mode Rapide)

**1. Double-cliquez sur `start.bat`**

Ou manuellement :

**Terminal 1 - Backend :**
```bash
python -m uvicorn src.web.app:app --reload --port 5000
```

**Terminal 2 - Frontend :**
```bash
cd frontend
npm run dev
```

**Accédez à** : http://localhost:3000

---

### Option B : Production (1 seul serveur)

**1. Build React :**
```bash
cd frontend
npm run build
```

**2. Démarrez FastAPI :**
```bash
python -m uvicorn src.web.app:app --port 5000
```

**Accédez à** : http://localhost:5000

✅ FastAPI sert automatiquement le build React !

---

## ❓ Pourquoi 2 serveurs en dev ?

### Avantages du mode développement (2 serveurs)

| Fonctionnalité | Dev (2 serveurs) | Prod (1 serveur) |
|----------------|------------------|------------------|
| **HMR** (Hot Module Replacement) | ✅ Instantané | ❌ |
| **Rebuild** | ✅ <100ms | ❌ Build manuel |
| **React DevTools** | ✅ | ❌ |
| **Source Maps** | ✅ | ❌ |
| **Simplicité** | Port 3000 pour UI | Port 5000 pour tout |

**En dev** : Vous modifiez un composant → L'écran se met à jour instantanément sans reload !

**En prod** : Vous faites `npm run build` → FastAPI sert les fichiers statiques

---

## 📁 Architecture

```
┌─────────────────────────────────────┐
│  DEVELOPPEMENT (2 serveurs)         │
├─────────────────────────────────────┤
│                                     │
│  Frontend (Vite)      Backend       │
│  http://localhost:3000              │
│         │                │          │
│         │    Proxy /api  │          │
│         └────────────────>          │
│                    FastAPI          │
│                http://localhost:5000│
│                                     │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│  PRODUCTION (1 serveur)              │
├─────────────────────────────────────┤
│                                     │
│         FastAPI                     │
│    http://localhost:5000            │
│         │                           │
│         ├─> /api/* → API            │
│         └─> /* → React build        │
│                                     │
└─────────────────────────────────────┘
```

---

## 🛠️ Workflow Recommandé

### Pendant le développement

1. Utilisez `start.bat` ou 2 terminaux
2. Travaillez sur http://localhost:3000
3. Les changements apparaissent instantanément
4. L'API est accessible via proxy Vite

### Avant de deployer

1. Testez le build :
   ```bash
   cd frontend
   npm run build
   ```

2. Lancez FastAPI seul :
   ```bash
   python -m uvicorn src.web.app:app --port 5000
   ```

3. Vérifiez http://localhost:5000

---

## 🎨 Résumé de la Migration React

| Aspect | Avant | Après |
|--------|-------|-------|
| **Framework** | Jinja2 templates | React 18 SPA |
| **Styling** | Bootstrap générique | Tailwind CSS racing theme |
| **Animations** | CSS basiques | Framer Motion fluides |
| **Navigation** | Rechargement pages | Client-side routing |
| **État** | Vanilla JS | React Query |
| **Build** | Aucun | Vite (ultra-rapide) |
| **HMR** | ❌ | ✅ Instantané |

---

## 📦 Commandes Utiles

### Frontend
```bash
cd frontend
npm run dev      # Dev server
npm run build    # Build production
npm run preview  # Preview du build
```

### Backend
```bash
python -m uvicorn src.web.app:app --reload     # Dev
python -m uvicorn src.web.app:app              # Prod
```

---

## 🎯 Accès Rapide

| Service | DEV | PROD |
|---------|-----|------|
| **Frontend** | http://localhost:3000 | http://localhost:5000 |
| **API** | http://localhost:5000/api | http://localhost:5000/api |
| **API Docs** | http://localhost:5000/api/docs | http://localhost:5000/api/docs |

---

## 💡 Tips

1. **En dev** : Toujours utiliser localhost:3000 (HMR actif)
2. **Build rapide** : Vite build en ~2 secondes
3. **Proxy automatique** : /api/* est automatiquement proxifié vers :5000
4. **CORS** : Déjà configuré pour dev et prod

---

## 🚀 L'outil est maintenant à son PRIME !

✅ Interface React moderne
✅ Design racing professionnel
✅ Animations fluides partout
✅ Architecture scalable
✅ HMR ultra-rapide
✅ Build production optimisé

**Prêt à créer des championnats ! 🏎️**
