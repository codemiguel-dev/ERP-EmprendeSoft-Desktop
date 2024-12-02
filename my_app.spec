# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Recopila datos y módulos ocultos automáticamente
datas = collect_data_files('PyQt5')  # Incluye los recursos de PyQt5
hiddenimports = collect_submodules('PyQt5')  # Importa todos los submódulos necesarios

a = Analysis(
    ['main.py'],  # Cambia 'main.py' al nombre de tu archivo principal
    pathex=[],
    binaries=[],
    datas=datas,  # Agrega los datos recolectados
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
    name='my_app',  # Cambia 'my_app' por el nombre de tu aplicación
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Cambia a False para que no muestre consola
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

# Si tu aplicación tiene recursos adicionales (como imágenes o archivos .ui),
# asegúrate de incluirlos manualmente si no los maneja `collect_data_files`.
