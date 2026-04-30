# -*- mode: python ; coding: utf-8 -*-
import os

_root = os.path.abspath(os.path.join(SPECPATH, '..'))

a = Analysis(
    [os.path.join(_root, 'main.py')],
    pathex=[_root],
    binaries=[],
    datas=[
        (os.path.join(_root, 'y4rb/defaults'), 'y4rb/defaults'),
        (os.path.join(_root, 'y4rb/templates'), 'y4rb/templates'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='y4rb',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
