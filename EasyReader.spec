# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_all

piper_datas, piper_binaries, piper_hidden = collect_all('piper')
odf_datas, odf_binaries, odf_hidden = collect_all('odf')
pygame_datas, pygame_binaries, pygame_hidden = collect_all('pygame')


a = Analysis(
    ['main.py'],
    pathex=['.'],
    datas=[
        ('documents', 'documents'),
        *piper_datas,
        *odf_datas,
        *pygame_datas,
    ],
    binaries=[
        *piper_binaries,
        *pygame_binaries,
    ],
    hiddenimports=[
        'piper',
        'odf',
        'odf.opendocument',
        'odf.text',
        'pystray',
        'pygame',
        'uiautomation',
        'pynput',
        'core.model_manager',
        *piper_hidden,
        *odf_hidden,
        *pygame_hidden,
    ],
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    name='EasyReader',
    console=False,
    icon='icon.ico'
)
