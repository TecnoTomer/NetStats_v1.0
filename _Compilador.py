import sys
from cx_Freeze import setup, Executable
import _Variables

build_exe_options = {
    "packages": ["tkinter"],
    "includes": [
        "tkinter", "json", "os", "sys", "subprocess", 
        "time", "ctypes", "psutil", "win32serviceutil", "importlib", "threading",
        "folium", "webview", "re", "random", "ping3", "requests"
    ],
    "include_files": [
        ("lib/resources", "lib/resources")
    ]
}

executables = [
    Executable("_NetStat.py", base=None, target_name="tu_aplicacion.exe", icon=_Variables.icono_bar)
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
