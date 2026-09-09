# -*- mode: python ; coding: utf-8 -*-


a = Analysis(

    [
        "main.py"
    ],


    datas=[

        (
            "models",
            "models"
        )

    ],


    hiddenimports=[

        "piper",
        "odf"

    ]

)



pyz = PYZ(a.pure)


exe = EXE(

    pyz,

    a.scripts,

    name="EasyReader",

    console=False,

    icon="icon.ico"

)
