# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

# Caminhos relativos a partir da pasta build
datas = [('../config.json', '.')]
binaries = []
hiddenimports = ['customtkinter', 'tkinter', 'hashchain', 'hashchain.core', 'hashchain.core.encryption', 'hashchain.core.decryption', 'hashchain.core.compression', 'hashchain.core.key_generator', 'hashchain.tables', 'hashchain.tables.table_generator', 'hashchain.utils', 'hashchain.utils.colors', 'hashchain.utils.handler', 'hashchain.utils.input_collector', 'hashchain.config', 'hashchain.config.config_manager', 'hashchain.interfaces', 'hashchain.interfaces.gui']
tmp_ret = collect_all('customtkinter')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]


a = Analysis(
    ['main_gui.py'],  # main_gui.py está na pasta build
    pathex=['..'],  # Adiciona a raiz do projeto ao path
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
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
    name='HashChain',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
