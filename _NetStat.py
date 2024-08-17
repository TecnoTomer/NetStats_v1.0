import tkinter as tk
from PIL import Image, ImageTk
import json
import os
import sys
import subprocess
import time

import _Alerts
import _Variables
import _Buttons_Funtions
import _NetStat_Funtions

class AppController:
    def __init__(self, root):
        self.root = root
        self.current_frame = None
        
        # Inicializar con el tema claro por defecto
        self.current_theme = self.load_saved_theme("theme", "light")
        self.current_language = self.load_language("language", "en")

        # Crear la barra superior antes de crear el contenedor de frames
        self.top_bar = self.create_top_bar()

        # Contenedor para todos los frames, asegurándose de que esté debajo de la barra superior
        self.frame_container = tk.Frame(root)
        self.frame_container.pack(side="top", fill="both", expand=True, after=self.top_bar)

        #aplicar tema
        self.apply_theme(self.current_theme)
        #self.load_language(self.current_language)

    def load_saved_theme(self, key, valor):
        # Leer el archivo JSON para obtener el tema
        data = _NetStat_Funtions.read_json_file(_Variables.rute_data)
        # Asignar el tema guardado, por defecto 'light'
        theme_name = data.get("options", [{}])[0].get(key, valor)
        # Establecer la variable global theme en Variables
        _Variables.theme = theme_name
        # Devolver la configuración de tema apropiada
        return _Variables.dark_theme if theme_name == 'dark' else _Variables.light_theme

    def load_language(self, key, valor):
        # Leer el archivo JSON para cargar el idioma guardado
        try:
            data = _NetStat_Funtions.read_json_file(_Variables.rute_data)
            _Variables.current_language = data.get("options", [{}])[0].get(key, valor)
        except FileNotFoundError:
            _Variables.current_language = "en"  # Valor predeterminado si no se encuentra el archivo
        #return _Variables

    def create_top_bar(self):
        top_bar = tk.Frame(self.root, bg=self.current_theme["bg_color"], height=20)
        top_bar.pack(side='top', fill='x')
        
        # Configuración de botones
        #Home
        button1 = tk.Button(
            top_bar, 
            text=_Variables.languages[_Variables.current_language]["Home"],
            font=_Variables.poppins,
            width=10, 
            bg=self.current_theme["bg_color"], 
            fg=self.current_theme["fg_color"],
            borderwidth=0,
            relief="flat",
            command=lambda: _Buttons_Funtions.B_Home(None, self)
        )
        button1.pack(side="left")
        button1.bind("<Enter>", lambda e: self.on_enter(e))
        button1.bind("<Leave>", lambda e: self.on_leave(e))
        #button1.config(text=languages[_Variables.current_language]["greeting"])

        #Track IP
        button2 = tk.Button(
            top_bar, 
            text=_Variables.languages[_Variables.current_language]["Track_IP"], 
            font=_Variables.poppins,
            width=10, 
            bg=self.current_theme["bg_color"], 
            fg=self.current_theme["fg_color"],
            borderwidth=0,
            relief="flat"
        )
        button2.pack(side="left")
        button2.bind("<Enter>", lambda e: self.on_enter(e))
        button2.bind("<Leave>", lambda e: self.on_leave(e))
        button2.bind("<Button-1>", lambda event: _Buttons_Funtions.B_TrackIp(event, self))

        #NetStat
        button3 = tk.Button(
            top_bar, 
            text=_Variables.languages[_Variables.current_language]["Running"],
            font=_Variables.poppins,
            width=10, 
            bg=self.current_theme["bg_color"], 
            fg=self.current_theme["fg_color"],
            borderwidth=0,
            relief="flat"
        )
        button3.pack(side="left")
        button3.bind("<Enter>", lambda e: self.on_enter(e))
        button3.bind("<Leave>", lambda e: self.on_leave(e))
        button3.bind("<Button-1>", lambda event: _Buttons_Funtions.B_Netstat(event, self))

        #Options
        button4 = tk.Button(
            top_bar,
            text=_Variables.languages[_Variables.current_language]["Options"],
            font=_Variables.poppins,
            width=10, 
            bg=self.current_theme["bg_color"], 
            fg=self.current_theme["fg_color"],
            borderwidth=0,
            relief="flat"
        )
        button4.pack(side="left")
        button4.bind("<Enter>", lambda e: self.on_enter(e))
        button4.bind("<Leave>", lambda e: self.on_leave(e))
        button4.bind("<Button-1>", lambda event: _Buttons_Funtions.B_Options(event, self))

        #Help
        button5 = tk.Button(
            top_bar, 
            text=_Variables.languages[_Variables.current_language]["Help"], 
            font=_Variables.poppins,
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
        widget['font'] = _Variables.poppins_negrita

    def on_leave(self, event):
        widget = event.widget
        widget['bg'] = self.current_theme["bg_color"]
        widget['font'] = _Variables.poppins

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
                widget['font'] = _Variables.poppins_negrita

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

    def switch_theme(self, valor):
        if valor == _Variables.theme:
            _Alerts.alerta_ok(
                _Variables.titulo, 
                _Variables.languages[_Variables.current_language]["Noti"], 
                _Variables.languages[_Variables.current_language]["same_chane"])
        else:
            answer = _Alerts.alerta_aceptar(
                _Variables.titulo, 
                _Variables.languages[_Variables.current_language]["Noti"], 
                _Variables.languages[_Variables.current_language]["Restart"])
            if answer == 1:
                # Cambiar el tema actual solo si es diferente al tema guardado
                if valor == 'dark' and _Variables.theme == 'light':
                    self.current_theme = _Variables.dark_theme
                    _Variables.theme = 'dark'

                elif valor == 'light' and _Variables.theme == 'dark':
                    self.current_theme = _Variables.light_theme
                    _Variables.theme = 'light'

                else:
                    return
                
                # Guardar el nuevo tema en el archivo JSON
                self.save_current_value("theme", _Variables.theme) #save new theme at json file land options data

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

    def save_current_value(self, variable, valor):
        # Leer los datos actuales
        data = _NetStat_Funtions.read_json_file(_Variables.rute_data)
        # Actualizar o añadir el tema
        if not data.get("options"):
            data["options"] = [{}]
        data["options"][0][variable] = valor

        # Escribir los datos actualizados al archivo
        with open(_Variables.rute_data, 'w') as file:
            json.dump(data, file, indent=4)

    def switch_language(self, valor):
        # switch languaje
        if valor == _Variables.current_language:
            _Alerts.alerta_ok(
                _Variables.titulo, 
                _Variables.languages[_Variables.current_language]["Noti"], 
                _Variables.languages[_Variables.current_language]["same_chane"])
        else:
            answer = _Alerts.alerta_aceptar(
                _Variables.titulo, 
                _Variables.languages[_Variables.current_language]["Noti"], 
                _Variables.languages[_Variables.current_language]["Restart"])
            if answer != 2:
                if valor == "en" and _Variables.current_language == "es":
                    _Variables.current_language = "en"
                elif valor == "es" and _Variables.current_language == "en":
                    _Variables.current_language = "es"
                else: return

                self.save_current_value("language", _Variables.current_language)

                reiniciar_aplicacion()
            else:
                return

def reiniciar_aplicacion():
    # Guarda el intérprete de Python actual
    python = sys.executable
    # Usa subprocess para lanzar una nueva instancia de esta aplicación
    subprocess.Popen([python] + sys.argv)
    # Cierra la instancia actual
    sys.exit()

def Win_p(frame, theme):
    window_p = tk.Frame(frame, bg=theme["bg_color"])
    window_p.pack(side="top", fill="both", expand=True)

    #logotipe img
    logo_img = Image.open(theme["logotipe"])
    logo_img = logo_img.resize((150, 150))
    img_logo = ImageTk.PhotoImage(logo_img)
    logo_img = tk.Label(window_p, image=img_logo, bg=theme["bg_color"])
    logo_img.place(x=170, y=5)
    logo_img.image = img_logo    
    #iplocation img
    Iplocation_img = Image.open(theme["IpLocation"])
    Iplocation_img = Iplocation_img.resize((300, 80))
    img_iplocation = ImageTk.PhotoImage(Iplocation_img)
    Iplocation_img = tk.Label(window_p, image=img_iplocation, bg=theme["bg_color"])
    Iplocation_img.place(x=110, y=520)
    Iplocation_img.image = img_iplocation
    #back img
    background_img = Image.open(theme["Background"])
    background_img = background_img.resize((500, 350))
    img_back = ImageTk.PhotoImage(background_img)
    background_img = tk.Label(window_p, image=img_back, bg=theme["bg_color"])
    background_img.place(x=0, y=150)
    background_img.image = img_back

    return window_p

def main():
    _NetStat_Funtions.update_json_with_option(_Variables.rute_data, "theme", _Variables.inicial_theme)
    #_NetStat_Funtions.update_json_with_option(_Variables.rute_data, "language", _Variables.current_language)
    #size window_root
    ancho = 500
    alto = 650

    _Variables.window_root.title(_Variables.titulo) #Titulo
    _Variables.window_root.geometry(f"{ancho}x{alto}")

    #screen width & heigth
    pantalla_ancho = _Variables.window_root.winfo_screenwidth()
    pantalla_alto = _Variables.window_root.winfo_screenheight()

    #position to center window_root
    x = (pantalla_ancho - ancho) // 2
    y = (pantalla_alto - alto) // 2

    #block size
    _Variables.window_root.resizable(False, False)

    #center the windows_root
    _Variables.window_root.geometry(f"{ancho}x{alto}+{x}+{y}")

    #windows_root icon
    #_Variables.window_root.iconbitmap(_Variables.icono)

    icono_imagen = tk.PhotoImage(file=_Variables.icono_bar)

    # Establecer el icono de la ventana y barra de tareas
    #_Variables.window_root.iconphoto(False, icono_imagen)
    _Variables.window_root.iconphoto(True, icono_imagen)

    # Crear el controlador de la aplicación
    app_controller = AppController(_Variables.window_root)
    _Variables.app_controller = app_controller
    #app_controller.cambio_ventana(Win_p, )
    app_controller.cambio_ventana(lambda frame: Win_p(frame, app_controller.current_theme))

    _Variables.window_root.mainloop()

if __name__ == "__main__":
    main()
