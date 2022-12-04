# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('dialog_companysave.ui','.'),
    ('dialog_customer.ui','.'),
    ('dialog_newproject.ui','.'),
    ('ui_calendar.ui','.'),
    ('ui_customer.ui','.'),
    ('ui_mainframe.ui','.'),
    ('ui_po.ui','.'),
    ('ui_polist.ui','.'),
    ('ui_temp.ui','.'),
    ('ui_upload_dialog.ui','.'),
    ('ui_upload_po.ui','.'),
    ('ui_worklist.ui','.'),
    ('ui_works.ui','.'),
    ('ui_projectlist.ui','.'),
    ('untitled.ui','.'),
    ('poform.xlsx','.'),
    ('tsc-erp-firebase-adminsdk-apb5k-f725d83303.json','.'),
    ('logo.png','.'),
    ('refresh_1.png','.'),
    ('refresh.png','.'),
    ('calender.png','.')
    ],
    hiddenimports=[],
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
    name='TSC ERP',
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
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)
