# SubScribe.spec  —  PyInstaller build spec
# Run:  pyinstaller SubScribe.spec

import sys
from pathlib import Path

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[
        ('ffmpeg/ffmpeg.exe', 'ffmpeg'),
    ],
    datas=[
        (str(Path(__import__('customtkinter').__file__).parent), 'customtkinter'),
    ],
    hiddenimports=[
        'whisper',
        'whisper.audio',
        'whisper.decoding',
        'whisper.model',
        'whisper.tokenizer',
        'whisper.transcribe',
        'whisper.utils',
        'torch',
        'torch.nn',
        'torch.nn.functional',
        'tqdm',
        'tiktoken',
        'tiktoken.registry',
        'tiktoken_ext',
        'tiktoken_ext.openai_public',
        'regex',
        'numba',
        'scipy',
        'scipy.signal',
        'customtkinter',
        'packaging',
        'packaging.version',
        'packaging.specifiers',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='SubScribe',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='SubScribe',
)
