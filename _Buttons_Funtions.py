import tkinter as tk

import _Variables
import _NetStat
import _NetStat_Funtions

def B_Home(event, controller):
	controller.cambio_ventana(lambda frame: _NetStat.Win_p(frame, controller.current_theme))

def B_Netstat(event, controller):
    controller.cambio_ventana(lambda frame: _NetStat_Funtions.Win_NetStat(frame, controller.current_theme))

def B_Options(event, controller):
    def show_submenu(event):
        submenu.post(event.x_root, event.y_root)

    # create dropdown menu
    menu = tk.Menu(controller.root, bg=controller.current_theme["bg_color"], fg=controller.current_theme["fg_color"], tearoff=0)
    
    # add options to main menu
    menu.add_command(label="Option 1", command=lambda: print("Option 1 selected"))
    menu.add_command(label="Option 2", command=lambda: print("Option 2 selected"))
    
    # create submenu theme options
    submenu = tk.Menu(menu, bg=controller.current_theme["bg_color"], fg=controller.current_theme["fg_color"], tearoff=0)
    submenu.add_command(label="Dark", command=lambda: controller.switch_theme('dark'))
    submenu.add_command(label="Light", command=lambda: controller.switch_theme('light'))
    # add option to the button "theme/tema"
    menu.add_cascade(label="Tema", menu=submenu)

    # get the button who actived the menu using the event widget
    button = event.widget

    # Get the coordinates of the button in the main window
    x = button.winfo_rootx()
    y = button.winfo_rooty() + button.winfo_height()

    # show the menu in the button position
    menu.post(x, y)
    
    # add the submenu to the button option in the top bar main menu
    menu.entryconfig("Tema", command=lambda e=None: show_submenu(e))
