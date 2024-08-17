import tkinter as tk

import _Variables
import _NetStat
import _NetStat_Funtions
from _TrackIp_Funtions import Win_TrackIp

#top bar buttons
def B_Home(event, controller):
    controller.cambio_ventana(lambda frame: _NetStat.Win_p(frame, controller.current_theme))

def B_TrackIp(event, controller):
    controller.cambio_ventana(lambda frame: Win_TrackIp(frame, controller.current_theme))

def B_Netstat(event, controller):
    controller.cambio_ventana(lambda frame: _NetStat_Funtions.Win_NetStat(frame, controller.current_theme))

def B_Options(event, controller):
    def show_submenu(event):
        submenu_Tema.post(event.x_root, event.y_root)

    # create dropdown menu
    menu = tk.Menu(controller.root, bg=controller.current_theme["bg_color"], fg=controller.current_theme["fg_color"], tearoff=0)
    
    # create submenu theme theme
    submenu_Tema = tk.Menu(menu, bg=controller.current_theme["bg_color"], fg=controller.current_theme["fg_color"], tearoff=0)
    submenu_Tema.add_command(label=_Variables.languages[_Variables.current_language]["dark"], command=lambda: controller.switch_theme('dark'))
    submenu_Tema.add_command(label=_Variables.languages[_Variables.current_language]["light"], command=lambda: controller.switch_theme('light'))
    # add options to the button "theme/tema"
    menu.add_cascade(label=_Variables.languages[_Variables.current_language]["Theme"], menu=submenu_Tema)

    # create submenu the languages option
    submenu_lang = tk.Menu(menu, bg=controller.current_theme["bg_color"], fg=controller.current_theme["fg_color"], tearoff=0)
    submenu_lang.add_command(label=_Variables.languages[_Variables.current_language]["eng"], command=lambda: controller.switch_language('en'))
    submenu_lang.add_command(label=_Variables.languages[_Variables.current_language]["spa"], command=lambda: controller.switch_language('es'))
    # add options to the button "theme/tema"
    menu.add_cascade(label=_Variables.languages[_Variables.current_language]["lang"], menu=submenu_lang)

    # get the button who actived the menu using the event widget
    button = event.widget

    # Get the coordinates of the button in the main window
    x = button.winfo_rootx()
    y = button.winfo_rooty() + button.winfo_height()

    # show the menu in the button position
    menu.post(x, y)
    
    # add the submenu to the button option in the top bar main menu
    menu.entryconfig(_Variables.languages[_Variables.current_language]["Theme"], command=lambda e=None: show_submenu(e))

    # add the submenu to the button option in the top bar main menu
    menu.entryconfig(_Variables.languages[_Variables.current_language]["lang"], command=lambda e=None: show_submenu(e))

#treeview _NetStat_Funtions buttons
def B_details(event):
    _NetStat_Funtions.get_selected_item_data()

    _text = (
        f"{_Variables.languages[_Variables.current_language]['Port']}: {_Variables._port}\n"
        f"{_Variables.languages[_Variables.current_language]['Pid']}: {_Variables._pid}\n"
        f"{_Variables.languages[_Variables.current_language]['Local_IP']}: {_Variables._land}\n"
        f"{_Variables.languages[_Variables.current_language]['Remote_IP']}: {_Variables._wan}\n"
        f"{_Variables.languages[_Variables.current_language]['Service']}: {_Variables._service}\n"
        f"{_Variables.languages[_Variables.current_language]['Status']}: {_Variables._status}"
    )
    
    _NetStat_Funtions.row_click(event, _text, _Variables.inicial_theme)


#TRACK_IP BUTTONS#
#
def start_button(search_entry):
    if search_entry:
        data = search_entry.get()
        print(f"datos de entry: {data}")
    else:
        print("vacido")

#Label buttons styles
def on_enter(event, label, hover_image):
    label.config(image=hover_image)
    label.image = hover_image  # Actualizar la referencia de la imagen para evitar que se recolecte

def on_leave(event, label, normal_image):
    label.config(image=normal_image)
    label.image = normal_image  # Actualizar la referencia de la imagen para evitar que se recolecte
