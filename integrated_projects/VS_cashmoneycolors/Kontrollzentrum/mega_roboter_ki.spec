# PyInstaller-Spezifikationsdatei für das Kontrollzentrum
# Diese Datei kann für komplexere Bundles angepasst werden
# Standardmäßig reicht der --onefile-Parameter, aber hier können Daten, Ressourcen und Hidden Imports ergänzt werden

block_cipher = None


a = Analysis([
    'mega_roboter_ki.py',
],
    pathex=[],
    binaries=[],
    datas=[
        ('modules/*', 'modules'),
        ('core/*', 'core'),
        ('.env', '.'),
    ],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='🤖ROBOTER_KI_APP',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='🤖ROBOTER_KI_APP')
