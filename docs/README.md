# Documentation — rFactor Championship Creator

Bienvenue dans la documentation du projet. Cette section regroupe tous les guides et références utiles. Pour l’historique, consultez le dossier d’archives.

## Guides principaux

- Guide Utilisateur: `docs/USER_GUIDE.md`
- Guide Développeur: `docs/DEVELOPER_GUIDE.md`
- Guide de démarrage rapide: `docs/QUICK_START.md`
- Roadmap: `docs/ROADMAP.md`

## Références techniques

- Spécifications: `docs/SPECIFICATIONS.md`
- Formats de fichiers rFactor: `docs/FILE_FORMATS.md`

## Démarrage rapide

1) Configurer l’application (premier lancement):
```
python scripts/setup_config.py
```

2) Lancer l’application via script:
```
scripts/start.bat
```

3) Ou lancer manuellement:
```
python -m uvicorn src.web.app:app --host 127.0.0.1 --port 5000 --reload
```

## Archives et notes historiques

- `docs/archive/` — Sprints, notes de migration et documents historiques

