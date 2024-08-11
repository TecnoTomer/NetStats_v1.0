import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["tkinter"],
    "includes": [
        "tkinter", "json", "os", "sys", "subprocess", 
        "time", "ctypes", "psutil"
    ],
    "include_files": [
        ("lib/resources", "lib/resources")
    ]
}

executables = [
    Executable("NetStat.py", base=None, icon="lib/resources/icons/icono.ico")
]

setup(
    name="NetStat",
    version="1.0",
    description="Descubre nuestra maravillosa aplicación para gestionar redes, ofreciendo control de puertos, gestión de procesos y rastreo de IP. La herramienta multifuncional ideal para mantener tus sistemas seguros y optimizados.",
    author="Emerson Granda",
    author_email="Emerson199818@outlook.com",
    url="https://github.com/emerson199818",
    options={"build_exe": build_exe_options},
    executables=executables
)