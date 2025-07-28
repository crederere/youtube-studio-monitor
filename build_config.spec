# -*- mode: python ; coding: utf-8 -*-

import sys
import os

block_cipher = None

# 현재 디렉토리에서 once.py 파일 경로 설정
main_script = 'once.py'

a = Analysis(
    [main_script],
    pathex=[],
    binaries=[],
    datas=[
        # 필요한 데이터 파일이 있다면 여기에 추가
    ],
    hiddenimports=[
        'pandas',
        'numpy',
        'numpy.core',
        'numpy.core._dtype_ctypes',
        'openpyxl',
        'openpyxl.styles',
        'openpyxl.drawing.image',
        'openpyxl.utils.dataframe',
        'websocket',
        'psutil',
        'requests',
        'urllib3',
        'PIL',
        'PIL.Image',
        'platform',
        'shutil',
        'threading',
        'json',
        'datetime',
        'time',
        're',
        'os',
        'subprocess',
        'webbrowser',
        'pathlib',
        'io',
        'tempfile',
        'urllib.request'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # 불필요한 패키지 제외
        'tkinter',
        'matplotlib',
        'test',
        'unittest',
        'pydoc',
        'doctest',
        'scipy',
        'IPython',
        'jupyter'
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# numpy/pandas 바이너리 호환성 문제 해결을 위한 추가 설정
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='YouTubeStudioMonitor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # upx 비활성화로 호환성 개선
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # 콘솔 창 표시 (로그 확인용)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # 아이콘 파일이 있다면 경로 설정
) 