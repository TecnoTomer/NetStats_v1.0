
import os
import ctypes
from ctypes import wintypes

def open_properties(file_path):
    try:
        # Verificar que el archivo exista
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"El archivo '{file_path}' no existe.")

        # Configuración para invocar la API de Windows
        ShellExecuteEx = ctypes.windll.shell32.ShellExecuteExW
        SEE_MASK_INVOKEIDLIST = 0xC
        SEE_MASK_NOCLOSEPROCESS = 0x40
        SW_SHOW = 5
        
        class SHELLEXECUTEINFO(ctypes.Structure):
            _fields_ = [
                ('cbSize', ctypes.c_ulong),
                ('fMask', ctypes.c_ulong),
                ('hwnd', wintypes.HWND),
                ('lpVerb', wintypes.LPCWSTR),
                ('lpFile', wintypes.LPCWSTR),
                ('lpParameters', wintypes.LPCWSTR),
                ('lpDirectory', wintypes.LPCWSTR),
                ('nShow', ctypes.c_int),
                ('hInstApp', wintypes.HINSTANCE),
                ('lpIDList', wintypes.LPVOID),
                ('lpClass', wintypes.LPCWSTR),
                ('hkeyClass', wintypes.HKEY),
                ('dwHotKey', ctypes.c_ulong),
                ('hIcon', wintypes.HANDLE),
                ('hProcess', wintypes.HANDLE)
            ]

        sei = SHELLEXECUTEINFO()
        sei.cbSize = ctypes.sizeof(SHELLEXECUTEINFO)
        sei.fMask = SEE_MASK_INVOKEIDLIST | SEE_MASK_NOCLOSEPROCESS
        sei.hwnd = None
        sei.lpVerb = 'properties'
        sei.lpFile = file_path
        sei.lpParameters = None
        sei.lpDirectory = None
        sei.nShow = SW_SHOW
        sei.hInstApp = None
        sei.lpIDList = None
        sei.lpClass = None
        sei.hkeyClass = None
        sei.dwHotKey = 0
        sei.hIcon = None
        sei.hProcess = None

        # Ejecutar la función ShellExecuteEx para abrir las propiedades
        if not ShellExecuteEx(ctypes.byref(sei)):
            raise ctypes.WinError()

        print(f"Propiedades del archivo '{file_path}' abiertas exitosamente.")
    
    except Exception as e:
        print(f"Ocurrió un error al intentar abrir las propiedades: {e}")

# Ejemplo de uso
open_properties("C:\\ruta\\al\\archivo.txt")
"""
