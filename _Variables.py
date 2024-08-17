#WINDOWS#
import tkinter as tk
from tkinter import font

#root
window_root = tk.Tk()
titulo = "NetStatus_v1.0"
icono_bar = 'lib/resources/icons/Imagen1.png'

#ROW VALUES
_port = ""
_pid = ""
_land = ""
_wan = ""
_service = ""
_status = ""


#COLORS#
light_theme = {
    "bg_color": "#ecebeb",  # Fondo blanco
    "fg_color": "#000000",  # Texto negro
    "button_bg": "#e0e0e0",  # Fondo de los botones
    "button_fg": "#000000",  # Texto de los botones
    "highlight_bg": "#f0f0f0",  # Fondo de las áreas resaltadas
    "highlight_fg": "#000000",  # Texto en áreas resaltadas
    "activebackground": "grey",
    "activeforeground": "black",
    "disabledforeground": "#ecebeb",
    "border_color": "#ecebeb",
    "on_enter": "#4444fc", #Color pasar mouse encima botones

    #TrackIP images
    "title_image": "lib/resources/icons/ui/Track_title_light.png",
    "logo": "lib/resources/icons/ui/background.png",
    "search_entry": "lib/resources/icons/ui/bar_search_light.png",
    "bt_start_normal_image": "lib/resources/icons/ui/start_light_normal.png", 
    "bt_start_select_image": "lib/resources/icons/ui/start_light_select.png",
    "entry": "#BFBFBF"

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
    "border_color": "#2e2e2e",
    "on_enter": "#4444fc",   #Color pasar mouse encima botones

    #TrackIP images
    "title_image": "lib/resources/icons/ui/Track_title_dark.png",
    "logo": "lib/resources/icons/ui/background.png",
    "search_entry": "lib/resources/icons/ui/bar_search_dark.png",
    "bt_start_normal_image": "lib/resources/icons/ui/start_dark_normal.png",
    "bt_start_select_image": "lib/resources/icons/ui/start_dark_select.png",
    "entry": "#080B1E"
}

current_language = "en"

languages = {
    "en": {
        "Home": "Home",
        "Track_IP": "Track IP",
        "Running": "Running",
        "Options": "Options",
        "Help": "Help",
        #sub menu theme
        "Theme": "Theme",
        "dark": "Dark",
        "light": "light",
        #submenu languaje
        "lang": "language",
        "eng": "English",
        "spa": "Spanish",
        #treeview columns
        "Port": "Port",
        "Pid": "Pid",
        "Local_IP": "Local IP",
        "Remote_IP": "Remote IP",
        "Service": "Service",
        "Status": "Status",
        #submenu treeview
        "Reboot": "Reboot",
        "Details": "Details",
        "Kill_Task": "Kill Task",
        "Properties": "Properties",
        "Search_Online": "Search Online",
        "Show_in_Folder": "Show in Folder",
        #Alerts text
        "Noti": "Warning!",
        "same_chane": f"The option is already applied",
        "Restart": f"To change the language you need to restart the application",
        "pid": f"\nThe row selected it doesn't have a Remote_IP, Action deny.\n",
        #_Netstast_funtion.py/
        "stop_service": f"\nDenying the service {_service}...\n",
        "done": "Hecho",
        "staring_service": f"\nThe service {_service} has been successfully restarted.\n",
        "error": f"\nThe action could not be\nRun the program as administrator.\n",
        "stop_process": f"The procces with the PID {_pid}, has ended" 
    },
    "es": {
        "Home": "Inicio",
        "Track_IP": "Rastreo IP",
        "Running": "Servicios",
        "Options": "Opciones",
        "Help": "Ayuda",
        #submenu theme
        "Theme": "Tema",
        "dark": "Oscuro",
        "light": "Claro",
        #submenu languaje
        "lang": "Idioma",
        "eng": "Ingles",
        "spa": "Español",
        #treeview columns
        "Port": "Puerto",
        "Pid": "Pid",
        "Local_IP": "IP Local",
        "Remote_IP": "IP Remota",
        "Service": "Servicio",
        "Status": "Estado",
        #submenu treeview
        "Reboot": "Reiniciar servicio",
        "Details": "Detalles",
        "Kill_Task": "Terminar servicio",
        "Properties": "Propiedades",
        "Search_Online": "Buscar Online",
        "Show_in_Folder": "Mostrar carpeta",
        #Alerts text
        "Noti": "¡Aviso!",
        "same_chane": f"La opción ya esta aplicada.",
        "Restart": f"Para cambiar el idioma es necesario reiniciar la aplicación",
        #_Netstast_funtion.py/crear_treeview/execute_Trackip
        "pid": f"\nLa celda seleccionada no tiene una IP Remota.\n",
        #_Netstast_funtion.py/
        "stop_service": f"\nDeteniendo el servicio {_service}...\n",
        "done": "Hecho",
        "staring_service": f"\nEl servicio {_service} se reinicio correctamente.\n",
        "error": f"\nNo se pudo realizar la accion, por falta de permisos.\nEjecute el programa como administrador.\n",
        "stop_process": f"El proceso con el PID {_pid}, ha terminado"
        
    }
}

#column click inf
colum_text_inf = (
        "ESTABLISHED: EST\n"
        "LISTEN: LSN\n"
        "CLOSE_WAIT: CW\n"
        "TIME_WAIT: TW\n"
        "SYN_SENT: SYN\n"
        "SYN_RECEIVED: SYN-R\n"
        "FIN_WAIT1: FW1\n"
        "FIN_WAIT2: FW2\n"
        "CLOSE: CLOSE\n"
        "CLOSING: CLOS\n"
        "LAST_ACK: LA\n"
        "UNKNOWN: UNK"
        )

colum_text_inf_es = (
        "ESTABLECIDA: EST\n"
        "ESCUCHANDO: LSN\n"
        "CERRANDO: CW\n"
        "EN ESPERA: TW\n"
        "SYN ENVIADO: SYN\n"
        "SYN RECIVIDO: SYN-R\n"
        "FIN ESPERA 1: FW1\n"
        "FIN ESPERA 2: FW2\n"
        "CERRAR: CLOSE\n"
        "CERRADO: CLOS\n"
        "ULTIMO ACK: LA\n"
        "DESCONOCIDO: UNK"
        )

#OTHERS#
current_tooltip = None

#FONT#
ruta_fuente = "lib/resources/font/poppins.ttf"
poppins_negrita = font.Font(family="Popins", size=9, weight="bold")
poppins = font.Font(family="Popins", size=9)
poppins_entry = font.Font(family="Popins", size=20, weight="bold")

#DATA#
#local data options
rute_data = "lib/resources/data/data.json" 
theme = ''
inicial_theme = "light"
#local data base networs stats
rute_network_data = "lib/resources/data/network_data.json"
total_ports = 0
open_ports = 0


#TRACK IP data:
map_location = "lib\\resources\\location\\map.html"
global_ruta = ""

#class controler from script _NetStat.py
app_controller = None

#TRACK_IP vars
ip_insert_entry = ""