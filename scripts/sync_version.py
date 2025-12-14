#!/usr/bin/env python3
"""
Script pour synchroniser le numéro de version dans tous les fichiers du projet.

Ce script lit la version depuis src/__version__.py (source unique de vérité)
et met à jour tous les fichiers qui contiennent des numéros de version.

Usage:
    uv run python scripts/sync_version.py
"""

import re
from pathlib import Path
from datetime import datetime

# Root directory
ROOT_DIR = Path(__file__).parent.parent

# Import version from source
import sys
sys.path.insert(0, str(ROOT_DIR / "src"))
from __version__ import __version__

# Date actuelle
TODAY = datetime.now().strftime("%d %B %Y")
AUJOURD_HUI = datetime.now().strftime("%d %B %Y")

# Mapper mois anglais -> français
MOIS = {
    "January": "Janvier", "February": "Février", "March": "Mars",
    "April": "Avril", "May": "Mai", "June": "Juin",
    "July": "Juillet", "August": "Août", "September": "Septembre",
    "October": "Octobre", "November": "Novembre", "December": "Décembre"
}
for en, fr in MOIS.items():
    AUJOURD_HUI = AUJOURD_HUI.replace(en, fr)

# Fichiers à mettre à jour avec leurs patterns
FILES_TO_UPDATE = {
    "pyproject.toml": [
        (r'version = "[^"]*"', f'version = "{__version__}"'),
    ],
    "frontend/package.json": [
        (r'"version": "[^"]*"', f'"version": "{__version__}"'),
    ],
    "README.md": [
        (r'\*\*Version Actuelle\*\* : [0-9.]+', f'**Version Actuelle** : {__version__}'),
        (r'\*\*Version\*\* : [0-9.]+', f'**Version** : {__version__}'),
    ],
    "CLAUDE.md": [
        (r'\*\*Version\*\* : [0-9.]+', f'**Version** : {__version__}'),
    ],
    "SCRIPTS_GUIDE.md": [
        (r'\*\*Version\*\* : [0-9.]+', f'**Version** : {__version__}'),
        (r'\*\*Date\*\* : .*', f'**Date** : {AUJOURD_HUI}'),
    ],
    "frontend/src/components/Layout.jsx": [
        (r'Creator</span> v[0-9.]+', f'Creator</span> v{__version__}'),
    ],
    "src/web/templates/base.html": [
        (r'Creator</span> v[0-9.]+', f'Creator</span> v{__version__}'),
    ],
}


def update_file(file_path: Path, patterns: list):
    """Mettre à jour un fichier avec les patterns donnés."""
    if not file_path.exists():
        print(f"[!] Fichier ignore (n'existe pas) : {file_path}")
        return

    content = file_path.read_text(encoding="utf-8")
    original_content = content

    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content)

    if content != original_content:
        file_path.write_text(content, encoding="utf-8")
        print(f"[OK] Mis a jour : {file_path.relative_to(ROOT_DIR)}")
    else:
        print(f"[--] Aucun changement : {file_path.relative_to(ROOT_DIR)}")


def main():
    """Synchroniser la version dans tous les fichiers."""
    print(f"\n==> Synchronisation de la version : {__version__}")
    print(f"Date : {AUJOURD_HUI}\n")

    for file_rel, patterns in FILES_TO_UPDATE.items():
        file_path = ROOT_DIR / file_rel
        update_file(file_path, patterns)

    print(f"\n==> Synchronisation terminee ! Version : {__version__}")


if __name__ == "__main__":
    main()
