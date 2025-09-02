# Coin_Collector_game.spec

block_cipher = None

a = Analysis(
    ['Coin_Collector_game.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('background.mp3', '.'),
        ('game_over.mp3', '.'),
        ('coin.wav', '.'),
        ('coin_pick.wav', '.'),
        ('ball.png', '.'),
        ('coin.png', '.'),
        ('object.png', '.'),
        ('walk_down.png', '.'),
        ('walk_left.png', '.'),
        ('walk_right.png', '.'),
        ('walk_up.png', '.'),
        ('icon.png', '.'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
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
    name='Coin_Collector_game',
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
    name='Coin_Collector_game'
)

