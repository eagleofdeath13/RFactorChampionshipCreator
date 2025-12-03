# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for rFactor Championship Creator

This spec file configures the build process to create a standalone executable
that includes all Python dependencies, templates, static files, and the built React frontend.
"""

from PyInstaller.utils.hooks import collect_data_files, collect_submodules
import os

# Get the project root directory
project_root = os.path.abspath(SPECPATH)

# Collect all data files from various packages
datas = []

# Add templates directory
datas += [(os.path.join(project_root, 'src', 'web', 'templates'), os.path.join('src', 'web', 'templates'))]

# Add static directory (old templates static files)
datas += [(os.path.join(project_root, 'src', 'web', 'static'), os.path.join('src', 'web', 'static'))]

# Add React frontend build (dist directory)
frontend_dist = os.path.join(project_root, 'frontend', 'dist')
if os.path.exists(frontend_dist):
    datas += [(frontend_dist, os.path.join('frontend', 'dist'))]

# Add config.json if exists
config_file = os.path.join(project_root, 'config.json')
if os.path.exists(config_file):
    datas += [(config_file, '.')]

# Collect all submodules for key packages
hiddenimports = []
hiddenimports += collect_submodules('fastapi')
hiddenimports += collect_submodules('uvicorn')
hiddenimports += collect_submodules('pydantic')
hiddenimports += collect_submodules('jinja2')
hiddenimports += collect_submodules('starlette')
hiddenimports += ['uvicorn.logging', 'uvicorn.loops', 'uvicorn.loops.auto', 'uvicorn.protocols', 'uvicorn.protocols.http', 'uvicorn.protocols.http.auto', 'uvicorn.protocols.websockets', 'uvicorn.protocols.websockets.auto', 'uvicorn.lifespan', 'uvicorn.lifespan.on']

# Add data files from packages
datas += collect_data_files('fastapi')
datas += collect_data_files('uvicorn')

a = Analysis(
    ['src/main.py'],
    pathex=[project_root],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='rfactor_championship_creator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  # Keep console for debugging/logs
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # You can add an icon file here later
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='rfactor_championship_creator',
)
