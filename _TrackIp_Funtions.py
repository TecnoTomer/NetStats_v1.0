import tkinter as tk
from PIL import Image, ImageTk
import folium
import os
import webview

import _Variables
import _Buttons_Funtions

search_entry = None

#main funtion show frame NetStat
def Win_TrackIp(frame, theme):
    _Variables.global_ruta = os.path.join(os.getcwd(), _Variables.map_location)
    _Variables.inicial_theme = theme
        
    window_TrackIp = tk.Frame(frame, bg=theme["bg_color"])
    window_TrackIp.pack(side="top", fill="both", expand=True)

    search_track_page(window_TrackIp)

    global search_entry
    if _Variables.ip_insert_entry:
            search_entry.insert(0, _Variables.ip_insert_entry)

    return window_TrackIp

def search_track_page(frame):
    # subframe from root window_TrackIp
    search_page = tk.Frame(frame, bg=_Variables.inicial_theme["bg_color"])
    search_page.pack(side="top", fill="both", expand=True)

    #TITLE IMAGE#
    # load img
    title_img = Image.open(_Variables.inicial_theme["title_image"])
    # resize the image width & height
    resized_image = title_img.resize((500, 150))
    img = ImageTk.PhotoImage(resized_image)
    # label to show the img
    title_img_label = tk.Label(search_page, image=img, bg=_Variables.inicial_theme["bg_color"])
    # position
    title_img_label.place(x=0, y=10)
    title_img_label.image = img

    #CENTER LOGO#
    Logo_img = Image.open(_Variables.inicial_theme["logo"])
    resized_image = Logo_img.resize((500, 500))
    img = ImageTk.PhotoImage(resized_image)
    Logo_img_label = tk.Label(search_page, image=img, bg=_Variables.inicial_theme["bg_color"])
    Logo_img_label.place(x=0, y=160)
    Logo_img_label.image = img

    #SEARCH ENTRY#
    search_entry_canva = Image.open(_Variables.inicial_theme["search_entry"])
    resized_image = search_entry_canva.resize((400, 50))
    img = ImageTk.PhotoImage(resized_image)
    search_entry_label = tk.Label(search_page, image=img, bg=_Variables.inicial_theme["bg_color"])
    search_entry_label.place(x=50, y=350)
    search_entry_label.image = img

    # Crear un Entry transparente sobre la imagen
    global search_entry
    search_entry = tk.Entry(
        search_page,
        bg=_Variables.inicial_theme["entry"],  # Mismo color que el fondo
        bd=0,  # Sin borde
        font=_Variables.poppins_entry,  # Fuente y tamaño del texto
        fg=_Variables.inicial_theme["fg_color"],  # Color del texto
        highlightthickness=0,  # Sin borde de enfoque
        insertbackground=_Variables.inicial_theme["fg_color"],  # Color del cursor
        justify='center'  # Centrar el texto
    )

    # Colocar el Entry exactamente encima de la imagen
    search_entry.place(x=56, y=360, width=380, height=32)

    #BUTTON#
    start_buton_leave = Image.open(_Variables.inicial_theme["bt_start_normal_image"]) #imagen rute
    start_buton_leave = start_buton_leave.resize((140, 50)) #rezise
    normal_image = ImageTk.PhotoImage(start_buton_leave) #convert to format photoimage
    start_buton_enter = Image.open(_Variables.inicial_theme["bt_start_select_image"])
    start_buton_enter = start_buton_enter.resize((140, 50))
    hover_image = ImageTk.PhotoImage(start_buton_enter)
    # create label with the normal image
    button_label = tk.Label(search_page, image=normal_image, bg=_Variables.inicial_theme["bg_color"])
    button_label.place(x=340, y=550)
    button_label.image = normal_image  # Mantener la referencia

    button_label.bind("<Enter>", lambda event: _Buttons_Funtions.on_enter(event, button_label, hover_image))
    button_label.bind("<Leave>", lambda event: _Buttons_Funtions.on_leave(event, button_label, normal_image))
    button_label.bind("<Button-1>", lambda event: _Buttons_Funtions.start_button(search_entry))


    return search_page

# create a empty map
def create_initial_map(output_file=_Variables.global_ruta):
    mapa = folium.Map(location=[0, 0], zoom_start=2)  # Centrado en coordenadas [0, 0] con un zoom bajo
    mapa.save(output_file)
    print(f"Mapa inicial guardado en {output_file}")

# Actualizar el mapa con nuevas coordenadas
def update_map(lat, lon, output_file=_Variables.global_ruta):
    mapa = folium.Map(location=[lat, lon], zoom_start=13)  # Centrado en la nueva ubicación
    folium.Marker([lat, lon], popup="Ubicación IP").add_to(mapa)
    mapa.save(output_file)
    print(f"Mapa actualizado guardado en {output_file}")

# Mostrar el mapa en un frame de pywebview
def show_map_in_frame(map_file):
    if os.path.exists(map_file):
        window = webview.create_window("Mapa de Tracking de IP", map_file)
        webview.start()
    else:
        print(f"Archivo {map_file} no encontrado.")

    return window

# Recargar el contenido del mapa en la ventana existente
def reload_map_in_frame(window):
    update_map(4.609710, -74.081750)  # Ejemplo de nueva ubicación (Bogotá)
    window.load_url(f'file:///{Ruta}')
