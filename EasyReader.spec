# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_all

piper_datas, piper_binaries, piper_hidden = collect_all('piper')
pygame_datas, pygame_binaries, pygame_hidden = collect_all('pygame')


a = Analysis(
    ['main.py'],
    pathex=['.'],
    datas=[
        ('config/settings.json', 'config'),
        ('documents', 'documents'),
        ('icon.ico', '.'),
        *piper_datas,
        *pygame_datas,
    ],
    binaries=[
        *piper_binaries,
        *pygame_binaries,
    ],
    hiddenimports=[
        'piper',
        'pystray',
        'pygame',
        'uiautomation',
        'pynput',
        'core.paths',
        'core.logger',
        'core.settings',
        'tts.model_loader',
        'tts.piper_engine',
        'ui.settings_window',
        *piper_hidden,
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
    icon='icon.ico',
)
