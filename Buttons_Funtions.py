import tkinter as tk

import Variables
import NetStat
import NetStat_Funtions

def B_Home(event, controller):
	controller.cambio_ventana(lambda frame: NetStat.Win_p(frame, controller.current_theme))

def B_Netstat(event, controller):
    #controller.cambio_ventana(NetStat_Funtions.Win_NetStat)
    controller.cambio_ventana(lambda frame: NetStat_Funtions.Win_NetStat(frame, controller.current_theme))

def B_Options(event, controller):
    def show_submenu(event):
        submenu.post(event.x_root, event.y_root)

    # Crear un menú desplegable
    menu = tk.Menu(controller.root, bg=controller.current_theme["bg_color"], fg=controller.current_theme["fg_color"], tearoff=0)
    
    # Añadir opciones al menú principal
    menu.add_command(label="Option 1", command=lambda: print("Option 1 selected"))
    menu.add_command(label="Option 2", command=lambda: print("Option 2 selected"))
    
    # Crear un submenú
    submenu = tk.Menu(menu, bg=controller.current_theme["bg_color"], fg=controller.current_theme["fg_color"], tearoff=0)
    submenu.add_command(label="Dark", command=lambda: controller.switch_theme('dark'))
    submenu.add_command(label="Light", command=lambda: controller.switch_theme('light'))
    # Añadir una opción al menú principal que tiene un submenú
    menu.add_cascade(label="Tema", menu=submenu)

    # Obtener el botón que activó el menú (usando el widget del evento)
    button = event.widget

    # Obtener las coordenadas del botón en la ventana principal
    x = button.winfo_rootx()
    y = button.winfo_rooty() + button.winfo_height()

    # Mostrar el menú en la posición del botón
    menu.post(x, y)
    
    # Asociar el submenú a la opción del menú principal
    menu.entryconfig("Tema", command=lambda e=None: show_submenu(e))
