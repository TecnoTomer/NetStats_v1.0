import sys
from cx_Freeze import setup, Executable
import _Variables

build_exe_options = {
    "packages": ["tkinter"],
    "includes": [
        "json",
        "os",
        "sys",
        "subprocess",
        "time",
        "tkinter",
        "psutil",
        "importlib",
        "win32serviceutil",
        "threading",
        "PIL",  # PIL es un módulo, aunque las clases 'Image' y 'ImageTk' son parte de este módulo.
        "folium",
        "webview",
        "re",
        "random",
        "ping3",
        "requests",
        "csv",
        "ipaddress",
        "shutil",
        "tempfile",
        "webbrowser",
        "ctypes"
    ],
    "include_files": [
        ("lib/resources", "lib/resources")
    ]
}

executables = [
    Executable("_NetStat.py", base=None, target_name="NetStatus_v1.0.exe", icon=_Variables.icono_exe)
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
