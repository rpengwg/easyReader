# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    datas=[
        ('models', 'models'),
        ('documents', 'documents')
    ],
    hiddenimports=[
        'piper',
        'odf',
        'odf.opendocument',
        'odf.text',
        'pystray',
        'pygame',
        'uiautomation',
        'pynput'
    ]
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    name='EasyReader',
    console=False,
    icon='icon.ico'
)
