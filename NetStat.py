import tkinter as tk
import json
import os
import sys
import subprocess
import time

import Alerts
import Variables
import Buttons_Funtions
import NetStat_Funtions

class AppController:
    def __init__(self, root):
        self.root = root
        self.current_frame = None
        
        # Inicializar con el tema claro por defecto
        self.current_theme = self.load_saved_theme()

        # Crear la barra superior antes de crear el contenedor de frames
        self.top_bar = self.create_top_bar()

        # Contenedor para todos los frames, asegurándose de que esté debajo de la barra superior
        self.frame_container = tk.Frame(root)
        self.frame_container.pack(side="top", fill="both", expand=True, after=self.top_bar)

        #aplicar tema
        self.apply_theme(self.current_theme)

    def load_saved_theme(self):
        # Leer el archivo JSON para obtener el tema
        data = NetStat_Funtions.read_json_file(Variables.rute_data)
        # Asignar el tema guardado, por defecto 'light'
        theme_name = data.get("options", [{}])[0].get("theme", "light")
        # Establecer la variable global theme en Variables
        Variables.theme = theme_name
        # Devolver la configuración de tema apropiada
        return Variables.dark_theme if theme_name == 'dark' else Variables.light_theme

    def create_top_bar(self):
        top_bar = tk.Frame(self.root, bg=self.current_theme["bg_color"], height=20)
        top_bar.pack(side='top', fill='x')
        
        # Configuración de botones
        #Home
        button1 = tk.Button(
            top_bar, 
            text="Home", 
            font=Variables.poppins,
            width=10, 
            bg=self.current_theme["bg_color"], 
            fg=self.current_theme["fg_color"],
            borderwidth=0,
            relief="flat",
            command=lambda: Buttons_Funtions.B_Home(None, self)
        )
        button1.pack(side="left")
        button1.bind("<Enter>", lambda e: self.on_enter(e))
        button1.bind("<Leave>", lambda e: self.on_leave(e))

        #Track IP
        button2 = tk.Button(
            top_bar, 
            text="Track Ip", 
            font=Variables.poppins,
            width=10, 
            bg=self.current_theme["bg_color"], 
            fg=self.current_theme["fg_color"],
            borderwidth=0,
            relief="flat"
        )
        button2.pack(side="left")
        button2.bind("<Enter>", lambda e: self.on_enter(e))
        button2.bind("<Leave>", lambda e: self.on_leave(e))

        #NetStat
        button3 = tk.Button(
            top_bar, 
            text="NetStat", 
            font=Variables.poppins,
            width=10, 
            bg=self.current_theme["bg_color"], 
            fg=self.current_theme["fg_color"],
            borderwidth=0,
            relief="flat"
        )
        button3.pack(side="left")
        button3.bind("<Enter>", lambda e: self.on_enter(e))
        button3.bind("<Leave>", lambda e: self.on_leave(e))
        button3.bind("<Button-1>", lambda event: Buttons_Funtions.B_Netstat(event, self))

        #Options
        button4 = tk.Button(
            top_bar, 
            text="Options", 
            font=Variables.poppins,
            width=10, 
            bg=self.current_theme["bg_color"], 
            fg=self.current_theme["fg_color"],
            borderwidth=0,
            relief="flat"
        )
        button4.pack(side="left")
        button4.bind("<Enter>", lambda e: self.on_enter(e))
        button4.bind("<Leave>", lambda e: self.on_leave(e))
        button4.bind("<Button-1>", lambda event: Buttons_Funtions.B_Options(event, self))

        #Help
        button5 = tk.Button(
            top_bar, 
            text="Help", 
            font=Variables.poppins,
            width=10, 
            bg=self.current_theme["bg_color"], 
            fg=self.current_theme["fg_color"],
            borderwidth=0,
            relief="flat",
            #command=lambda: Buttons_Funtions.B_Netstat(None, self)
        )
        button5.pack(side="left")
        button5.bind("<Enter>", lambda e: self.on_enter(e))
        button5.bind("<Leave>", lambda e: self.on_leave(e))

        return top_bar

    def on_enter(self, event):
        widget = event.widget
        widget['bg'] = self.current_theme["on_enter"]
        widget['font'] = Variables.poppins_negrita

    def on_leave(self, event):
        widget = event.widget
        widget['bg'] = self.current_theme["bg_color"]
        widget['font'] = Variables.poppins

    def create_event(self, widget): #Función auxiliar para crear un evento simulado.
        class Event:
            def __init__(self, widget):
                self.widget = widget
        return Event(widget)

    def simulate_hover_effects(self):
        # Simular el efecto de `on_enter` para aplicar el tema
        for widget in self.top_bar.winfo_children():
            if isinstance(widget, tk.Button):
                # Aplicar efecto de `on_enter`
                widget['bg'] = self.current_theme["on_enter"]
                widget['font'] = Variables.poppins_negrita

                # Restaurar a `on_leave` después de un corto tiempo
                self.root.after(5, lambda w=widget: self.on_leave(self.create_event(w)))

    def cambio_ventana(self, ventana_factory):
        # Destruir el contenido actual del frame si existe
        if self.current_frame is not None:
            for widget in self.frame_container.winfo_children():
                widget.destroy()

        # Crear un nuevo frame utilizando la nueva ventana
        self.current_frame = ventana_factory(self.frame_container)
        self.current_frame.pack(side="top", fill="both", expand=True)

    def switch_theme(self, theme):
        Alert_text = f"Para aplicar el tema {theme}, es necesario reiniciar el aplicativo"
        answer = Alerts.alerta_aceptar(Variables.titulo, "¡Aviso!", Alert_text)
        if answer == 1:
            # Cambiar el tema actual solo si es diferente al tema guardado
            if theme == 'dark' and Variables.theme == 'light':
                self.current_theme = Variables.dark_theme
                Variables.theme = 'dark'
            elif theme == 'light' and Variables.theme == 'dark':
                self.current_theme = Variables.light_theme
                Variables.theme = 'light'
            else:
                return
            
            # Guardar el nuevo tema en el archivo JSON
            self.save_current_theme(theme)
            
            # Aplicar el tema nuevo
            self.apply_theme(self.current_theme)

            # Forzar actualización de todos los widgets
            self.root.update_idletasks()

            reiniciar_aplicacion()

        else:
            return

    def apply_theme(self, theme):
        # Aplicar el tema a la ventana principal
        self.root.configure(bg=theme["bg_color"])
        
        # Aplicar el tema a cada widget hijo
        for widget in self.root.winfo_children():
            self.apply_widget_theme(widget, theme)
        self.simulate_hover_effects()
        self.root.update_idletasks()


    def apply_widget_theme(self, widget, theme):
        # Aplicar los colores del tema a un widget
        if isinstance(widget, tk.Button):
            widget.configure(
                bg=theme["button_bg"],
                fg=theme["button_fg"],
                activebackground=theme["activebackground"],
                activeforeground=theme["activeforeground"],
                disabledforeground=theme["disabledforeground"],
                relief=tk.FLAT  # Puedes cambiar el estilo del botón
            )
            widget.update_idletasks
        elif isinstance(widget, tk.Label):
            widget.configure(
                bg=theme["bg_color"],
                fg=theme["fg_color"]
            )
            widget.update_idletasks()
        elif isinstance(widget, tk.Frame):
            widget.configure(
                bg=theme["bg_color"]
            )
            widget.update_idletasks()
        
        # Recursivamente aplicar a widgets hijos
        for child in widget.winfo_children():
            self.apply_widget_theme(child, theme)

    def save_current_theme(self, theme):
        # Leer los datos actuales
        data = NetStat_Funtions.read_json_file(Variables.rute_data)
        # Actualizar o añadir el tema
        if not data.get("options"):
            data["options"] = [{}]
        data["options"][0]["theme"] = theme
        # Escribir los datos actualizados al archivo
        with open(Variables.rute_data, 'w') as file:
            json.dump(data, file, indent=4)

def reiniciar_aplicacion():
    # Guarda el intérprete de Python actual
    python = sys.executable
    #time.sleep(1)
    # Usa subprocess para lanzar una nueva instancia de esta aplicación
    subprocess.Popen([python] + sys.argv)
    
    # Cierra la instancia actual
    sys.exit()

def Win_p(frame, theme):
    window_p = tk.Frame(frame, bg=theme["bg_color"])
    window_p.pack(side="top", fill="both", expand=True)
    return window_p

def main():
    NetStat_Funtions.update_json_with_option(Variables.rute_data, "", "")
    #size window_root
    ancho = 500
    alto = 650

    Variables.window_root.title(Variables.titulo) #Titulo
    Variables.window_root.geometry(f"{ancho}x{alto}")

    #screen width & heigth
    pantalla_ancho = Variables.window_root.winfo_screenwidth()
    pantalla_alto = Variables.window_root.winfo_screenheight()

    #position to center window_root
    x = (pantalla_ancho - ancho) // 2
    y = (pantalla_alto - alto) // 2

    #block size
    Variables.window_root.resizable(False, False)

    #center the windows_root
    Variables.window_root.geometry(f"{ancho}x{alto}+{x}+{y}")

    #windows_root icon
    Variables.window_root.iconbitmap(Variables.icono)

    # Crear el controlador de la aplicación
    app_controller = AppController(Variables.window_root)
    #app_controller.cambio_ventana(Win_p, )
    app_controller.cambio_ventana(lambda frame: Win_p(frame, app_controller.current_theme))

    Variables.window_root.mainloop()

if __name__ == "__main__":
    main()
