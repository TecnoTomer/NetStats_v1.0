#WINDOWS#
import tkinter as tk
from tkinter import font

#root
window_root = tk.Tk()
titulo = "NetStatus_v1.0"
icono = 'lib/resources/icons/icono.ico'

#COLORS#

light_theme = {
    "bg_color": "#ffffff",  # Fondo blanco
    "fg_color": "#000000",  # Texto negro
    "button_bg": "#e0e0e0",  # Fondo de los botones
    "button_fg": "#000000",  # Texto de los botones
    "highlight_bg": "#f0f0f0",  # Fondo de las áreas resaltadas
    "highlight_fg": "#000000",  # Texto en áreas resaltadas
    "activebackground": "grey",
    "activeforeground": "black",
    "disabledforeground": "#ffffff",
    "on_enter": "#4444fc" #Color pasar mouse encima botones
}

dark_theme = {
    "bg_color": "#2e2e2e",  # Fondo oscuro
    "fg_color": "#ffffff",  # Texto blanco
    "button_bg": "#4d4d4d",  # Fondo de los botones
    "button_fg": "#ffffff",  # Texto de los botones
    "highlight_bg": "#3e3e3e",  # Fondo de las áreas resaltadas
    "highlight_fg": "#ffffff",  # Texto en áreas resaltadas
    "activebackground": "darkgrey",
    "activeforeground": "white",
    "disabledforeground": "#2e2e2e",
    "on_enter": "#4444fc"   #Color pasar mouse encima botones
}

#FONT#
ruta_fuente = "lib/resources/font/poppins.ttf"
poppins_negrita = font.Font(family="Popins", size=9, weight="bold")
poppins = font.Font(family="Popins", size=9)

#DATA#
rute_data = "lib/resources/data/data.json" #ruta data de variables locales
theme = 'light'
Actual_teme = ""
rute_network_data = "lib/resources/data/network_data.json"
open_ports = 0