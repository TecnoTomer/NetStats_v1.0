import tkinter as tk
from PIL import Image, ImageTk
from tkinter import scrolledtext
import folium
import os
import webview
import subprocess
import re
import threading
import time
import random
from ping3 import ping
import requests
import json

import _Variables
import _NetStat_Funtions
import _Buttons_Funtions

search_entry = None
#img motion
angle = 0
rotation_speed = 100
stop_flag = False

n = random.randint(2, 5)

def rotate_image():
    global angle
    global stop_flag

    # Verifica si la rotación debe detenerse
    if stop_flag:
        return

    # Incrementa el ángulo de rotación
    angle = (angle + 10) % 360  # Ajusta el valor 10 para cambiar el ángulo de rotación por iteración
    
    # Rota la imagen original sin expandirla
    rotated_img = Loading_img.rotate(angle, resample=Image.BICUBIC, expand=False)
    
    # Mantener el tamaño de la imagen original y centrarla
    width, height = rotated_img.size
    centered_img = Image.new("RGBA", (150, 150), (255, 255, 255, 0))
    centered_img.paste(rotated_img, ((150 - width) // 2, (150 - height) // 2))

    # Crear la imagen para Tkinter
    img = ImageTk.PhotoImage(centered_img)
    
    # Actualiza la etiqueta con la imagen rotada
    Loading_img_label.config(image=img)
    Loading_img_label.image = img
    
    # Llama a la función nuevamente después de `rotation_speed` milisegundos
    Loading_img_label.after(rotation_speed, rotate_image)

def start_rotation():
    global stop_flag
    stop_flag = False
    rotate_image()

def stop_rotation():
    global stop_flag
    stop_flag = True

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

    #check box
    checkbox_one_var = tk.BooleanVar()
    checkbox_one = tk.Checkbutton(
    search_page, 
    bg=_Variables.inicial_theme["bg_color"], 
    fg=_Variables.inicial_theme["fg_color"], 
    text=_Variables.languages[_Variables.current_language]["checkBox_one"], 
    variable=checkbox_one_var)
    checkbox_one.place(x=130, y=410)

    checkbox_all_var = tk.BooleanVar()
    checkbox_all = tk.Checkbutton(
    search_page, 
    bg=_Variables.inicial_theme["bg_color"], 
    fg=_Variables.inicial_theme["fg_color"], 
    text=_Variables.languages[_Variables.current_language]["checkBox_all"], 
    variable=checkbox_all_var)
    checkbox_all.place(x=280, y=410)

    #BUTTON#
    #normal image
    start_buton_leave = Image.open(
        _Variables.inicial_theme["bt_start_normal_image"] 
        if _Variables.current_language == 'en'
        else _Variables.inicial_theme["bt_iniciar_normal_image"]
    )
    start_buton_leave = start_buton_leave.resize((140, 50)) #rezise
    normal_image = ImageTk.PhotoImage(start_buton_leave) #convert to format photoimage
    #hover image
    start_buton_enter = Image.open(
        _Variables.inicial_theme["bt_start_select_image"]
        if _Variables.current_language == "en"
        else _Variables.inicial_theme["bt_iniciar_select_image"]
        )
    start_buton_enter = start_buton_enter.resize((140, 50))
    hover_image = ImageTk.PhotoImage(start_buton_enter)
    # create label with the normal image
    button_label = tk.Label(search_page, image=normal_image, bg=_Variables.inicial_theme["bg_color"])
    button_label.place(x=340, y=550)
    button_label.image = normal_image  # Mantener la referencia

    button_label.bind("<Enter>", lambda event: _Buttons_Funtions.on_enter(event, button_label, hover_image))
    button_label.bind("<Leave>", lambda event: _Buttons_Funtions.on_leave(event, button_label, normal_image))
    button_label.bind("<Button-1>", lambda event: _Buttons_Funtions.start_button(event, search_entry))


    return search_page

# Ejemplo de función para actualizar la interfaz de usuario
def update_ui_track(message):
    # Este es un ejemplo de cómo podrías actualizar la interfaz de usuario
    # Puedes ajustar esto según cómo quieras mostrar los mensajes
    if 'text_widget' in globals():
        text_widget.insert(tk.END, message + '\n')
        text_widget.see(tk.END)

def obtener_tracert(dominio, archivo_salida):
    def worker():
        _Variables.ip_insert_entry = dominio
        msg = _Variables.languages[_Variables.current_language]["try_conection"]
        update_ui_track(f"{msg} {dominio}...")
        time.sleep(n)
        if verificar_ip_ping3(dominio):
            update_ui_track(_Variables.languages[_Variables.current_language]["try_conection1"])
            time.sleep(n)
            update_ui_track(_Variables.languages[_Variables.current_language]["time"])
            time.sleep(n)
            update_ui_track(_Variables.languages[_Variables.current_language]["obtain_data"])
            # Ejecutar el comando tracert y capturar toda la salida
            comando = ["tracert", dominio]
            resultado = subprocess.run(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            if resultado.returncode != 0:
                update_ui_track(_Variables.languages[_Variables.current_language]["track_error"])
                time.sleep(n)
                update_ui_track(resultado.stderr)
                return

            # Guardar la salida completa en un archivo
            with open(archivo_salida, 'w') as archivo:
                archivo.write(resultado.stdout)
                update_ui_track(_Variables.languages[_Variables.current_language]["task_complete"])
                time.sleep(n)
            hilo1 = threading.Thread(target=clean)
            hilo1.start()
        else: 
            stop_rotation()
            update_ui_track(_Variables.languages[_Variables.current_language]["track_error"])
            return

    def clean():
        update_ui_track(_Variables.languages[_Variables.current_language]["clean"])
        patron_ip = re.compile(r'(\d{1,3}\.){3}\d{1,3}|\S+\s+\[\d{1,3}(\.\d{1,3}){3}\]')

        with open(archivo_salida, 'r') as archivo:
            lineas = archivo.readlines()

            # Procesar cada línea a partir de la quinta línea
            for linea in lineas[4:]:
                # Saltar los primeros 32 caracteres de cada línea y buscar coincidencias
                parte_relevante = linea[32:].strip()
                match = patron_ip.search(parte_relevante)
                if match:
                    _Variables.alL_hops.append(match.group())

        for i in _Variables.alL_hops:#imprimera los saltos
            update_ui_track(i)
            time.sleep(n)
        
        # Convertir la lista 'resultados' en una cadena con saltos de línea
        with open(archivo_salida, "w") as archivo:
            archivo.write("\n".join(_Variables.alL_hops))
            time.sleep(n)
            update_ui_track(_Variables.languages[_Variables.current_language]["task_complete"])

            hilo2 = threading.Thread(target=guardar_datos_ip_en_json)
            hilo2.start()

    def guardar_datos_ip_en_json():
        # Lista de IPs y nodos a procesar
        ips = _Variables.alL_hops  # Reemplaza esto con la lista de IPs y nodos

        # Diccionario para almacenar la información de cada IP
        datos_ips = {}

        for entrada in ips:
            # Inicializar variables
            nodo = None
            ip = None

            # Verificar si el formato es "nodo [ip]"
            if '[' in entrada and ']' in entrada:
                nodo, ip = entrada.split('[')
                nodo = nodo.strip()
                ip = ip.strip(']')
            else:
                ip = entrada.strip()  # Asumir que es una IP pura

            # Parámetros para la solicitud a la API
            payload = {
                'key': 'C87980CFD102895533EA9C272B7237A1',  # Reemplaza con tu clave API válida
                'ip': ip,
                'format': 'json'
            }

            # Realizar la solicitud GET a la API
            try:
                text = _Variables.languages[_Variables.current_language]["resques_iploction"]
                update_ui_track(f"\n{text}{ip}...")
                api_result = requests.get('https://api.ip2location.io/', params=payload)

                # Comprobar si la solicitud fue exitosa
                if api_result.status_code == 200:
                    # Convertir la respuesta en formato JSON a un diccionario de Python
                    datos_ip = api_result.json()

                    # Almacenar los datos de la IP en el diccionario general
                    datos_ips[ip] = {
                        "nodo": nodo,  # Agregar el nodo al diccionario, será None si es una IP pura
                        "country_code": datos_ip.get("country_code"),
                        "country_name": datos_ip.get("country_name"),
                        "region_name": datos_ip.get("region_name"),
                        "city_name": datos_ip.get("city_name"),
                        "latitude": datos_ip.get("latitude"),
                        "longitude": datos_ip.get("longitude"),
                        "zip_code": datos_ip.get("zip_code"),
                        "time_zone": datos_ip.get("time_zone"),
                        "asn": datos_ip.get("asn"),
                        "as": datos_ip.get("as"),
                        "is_proxy": datos_ip.get("is_proxy")
                    }
                    msg = _Variables.languages[_Variables.current_language]["task_complete"]
                    update_ui_track(f"{msg} {ip}\n")
                else:
                    msg = _Variables.languages[_Variables.current_language]["Error"]
                    update_ui_track(f"\n{msg} {api_result.status_code} {ip}")

            except requests.exceptions.RequestException as e:
                msg = _Variables.languages[_Variables.current_language]["Error"]
                update_ui_track(f"\n{msg}{ip}: {e}")

        # Guardar todos los datos en un archivo JSON
        with open(_Variables.IPlocation_basic_data, 'w') as archivo_json:
            json.dump(datos_ips, archivo_json, indent=4)
            update_ui_track(_Variables.languages[_Variables.current_language]["task_complete"])

    # Crear un hilo para ejecutar el tracert
    hilo = threading.Thread(target=worker)
    hilo.start()

def loading(frame, data):
    # subframe from root window_TrackIp
    loading_page = tk.Frame(frame, bg=_Variables.inicial_theme["bg_color"])
    loading_page.pack(side="top", fill="both", expand=True)

    # CENTER LOGO #
    global Loading_img
    Loading_img = Image.open(_Variables.loading_img)
    Loading_img = Loading_img.resize((150, 150))
    img = ImageTk.PhotoImage(Loading_img)
    global Loading_img_label
    Loading_img_label = tk.Label(loading_page, image=img, bg=_Variables.inicial_theme["bg_color"])
    Loading_img_label.place(x=170, y=10)
    Loading_img_label.image = img


    text_label = tk.Label(
        loading_page, 
        text=_Variables.languages[_Variables.current_language]["working"], 
        font=(_Variables.poppins_negrita, 20),
        bg=_Variables.inicial_theme["bg_color"], 
        fg=_Variables.inicial_theme["fg_color"])
    text_label.place(x=190, y=170)

    global text_widget
    text_widget = tk.Text(loading_page, height=25, width=68, bg=_Variables.inicial_theme["bg_color"], fg=_Variables.inicial_theme["fg_color"], font=(_Variables.poppins, 10))
    text_widget.place(x=10, y=215)
    
    start_rotation()

    # Iniciar la tarea en segundo plano
    obtener_tracert(data, _Variables.tracker_ip_output)

    return loading_page

#verify ip in use or not
def verificar_ip_ping3(ip, num_pings=6, min_respuestas_validas=3, timeout=1):
    respuestas_validas = 0

    for _ in range(num_pings):
        respuesta = ping(ip, timeout=timeout)
        if respuesta:
            respuestas_validas += 1

    return respuestas_validas >= min_respuestas_validas

#FUNCIONES PARA MOSTAR UBICACINES EN MAPA
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
