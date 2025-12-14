#!/usr/bin/env python3
"""
Script simple pour obtenir le numéro de version.
Utilisé par les scripts batch pour avoir la version dynamique.
"""

import sys
from pathlib import Path

# Add src to path
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR / "src"))

from __version__ import __version__

# Print version without newline
print(__version__, end='')
