import tkinter as tk
from tkinter import ttk
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
import csv
import ipaddress
import shutil
#from tkinterweb import HtmlFrame
#from tkhtmlview import HTMLLabel
#from io import BytesIO
import tempfile
import webbrowser

import _Alerts
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

    if stop_flag:
        return

    angle = (angle + 10) % 360
    
    rotated_img = Loading_img.rotate(angle, resample=Image.BICUBIC, expand=False)
    
    width, height = rotated_img.size
    centered_img = Image.new("RGBA", (150, 150), (255, 255, 255, 0))
    centered_img.paste(rotated_img, ((150 - width) // 2, (150 - height) // 2))

    img = ImageTk.PhotoImage(centered_img)
    
    Loading_img_label.config(image=img)
    Loading_img_label.image = img
    
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

def update_ui_track(message):
    if 'text_widget' in globals():
        text_widget.insert(tk.END, message + '\n')
        text_widget.see(tk.END)

def obtener_tracert(dominio, archivo_salida): #working
    def worker():
        update_ui_track("Step #1")
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
        update_ui_track("\nStep #2")
        update_ui_track(_Variables.languages[_Variables.current_language]["clean"])
        patron_ip = re.compile(r'(\d{1,3}\.){3}\d{1,3}|\S+\s+\[\d{1,3}(\.\d{1,3}){3}\]')

        with open(archivo_salida, 'r') as archivo:
            lineas = archivo.readlines()

            for linea in lineas[4:]:
                parte_relevante = linea[32:].strip()
                match = patron_ip.search(parte_relevante)
                if match:
                    _Variables.alL_hops.append(match.group())

        for i in _Variables.alL_hops:#imprimera los saltos
            update_ui_track(i)
            time.sleep(n)
       
        with open(archivo_salida, "w") as archivo:
            archivo.write("\n".join(_Variables.alL_hops))
            time.sleep(n)
            update_ui_track(_Variables.languages[_Variables.current_language]["task_complete"])

            hilo2 = threading.Thread(target=guardar_datos_ip_en_json)
            hilo2.start()

    def guardar_datos_ip_en_json():
        update_ui_track("\nStep #3")
        # Lista de IPs y nodos a procesar
        ips = _Variables.alL_hops  # Reemplaza esto con la lista de IPs y nodos

        datos_ips = {}

        for entrada in ips:
            # Inicializar variables
            nodo = None
            ip = None

            if '[' in entrada and ']' in entrada:
                nodo, ip = entrada.split('[')
                nodo = nodo.strip()
                ip = ip.strip(']')
            else:
                ip = entrada.strip()  # Asumir que es una IP pura

            # Parámetros para la solicitud a la API
            payload = {
                'key':'key',  # Reemplaza con tu clave API válida
                'ip': ip,
                'format': 'json'
            }

            # Realizar la solicitud GET a la API
            try:
                text = _Variables.languages[_Variables.current_language]["resques_iploction"]
                update_ui_track(f"{text}{ip}...")
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
                    update_ui_track(f"{msg} {ip}")
                else:
                    msg = _Variables.languages[_Variables.current_language]["Error"]
                    update_ui_track(f"\n{msg} {api_result.status_code} {ip}")

            except requests.exceptions.RequestException as e:
                msg = _Variables.languages[_Variables.current_language]["Error"]
                update_ui_track(f"\n{msg}{ip}: {e}")

        # Guardar todos los datos en un archivo JSON
        with open(_Variables.IPlocation_basic_data, 'w') as archivo_json:
            json.dump(datos_ips, archivo_json, indent=4)

        hilo3 = threading.Thread(target=clean_location_data)
        hilo3.start()

    def clean_location_data():
        update_ui_track("\nStep #4")
        # Leer el archivo JSON
        with open(_Variables.IPlocation_basic_data, 'r') as archivo:
            datos = json.load(archivo)
        
        # Iterar sobre cada IP en el JSON
        for ip, valores in datos.items():
            text = _Variables.languages[_Variables.current_language]["resques_iploction"]
            update_ui_track(f"{text}{ip}...")
            # Extraer los valores deseados
            country_code = valores.get('country_code')
            city_name = valores.get('city_name')
            asn = valores.get('asn')
            Proxy_inf(ip, city_name, asn)
            Asn_inf(ip, asn)
            update_ui_track(f"Done...")
        update_ui_track(_Variables.languages[_Variables.current_language]["task_complete"])
        _Variables.eliminar_archivo('lib/resources/data/Asn_resultado.json')
        _Variables.eliminar_archivo('lib/resources/data/Proxy_resultados.json')
        _Variables.eliminar_archivo(_Variables.tracker_ip_output)
        stop_rotation()
        r = _Alerts.alerta_ok(
            _Variables.titulo, 
            _Variables.languages[_Variables.current_language]["Noti"],
            _Variables.languages[_Variables.current_language]["end"])
        if r == 1:
            hilo4 = threading.Thread(target=ShowMap)
            hilo4.start()

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

#FUNCIONES PARA ENCONTRAR ORGANIZAR DATA
#proxy_inf
def Proxy_inf(ip_buscada, city_name_buscado, asn_buscado):
    column_names = ['IP1', 'IP2', 'Proxy Type', 'Country Code', 'Country', 'Region', 'City', 'ISP', 'Domain', 'Usage Type', 'ASN', 'Last Seen', 'Threat', 'Residential', 'Provider']
    
    def extraer_datos_fila(fila, column_names):
        datos = next(csv.reader([fila], delimiter=',', quotechar='"'))
        return dict(zip(column_names, datos))

    def obtener_datos_por_asn(archivo_csv, asn_buscado):
        resultados = {}

        with open(archivo_csv, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=',', quotechar='"')
            next(reader)  # Saltar la fila de encabezado

            for fila in reader:
                datos = extraer_datos_fila(','.join(fila), column_names)
                asn = datos.get('ASN', '')
                ciudad = datos.get('City', '')

                if asn == asn_buscado:
                    if asn not in resultados:
                        resultados[asn] = {}
                    if ciudad not in resultados[asn]:
                        resultados[asn][ciudad] = datos

        return resultados
    
    # Paso 1: Buscar los datos en el CSV y guardarlos en un JSON
    datos_por_asn = obtener_datos_por_asn(_Variables.db_proxy, asn_buscado)
    
    if datos_por_asn:
        archivo_salida = 'lib/resources/data/Proxy_resultados.json'
        with open(archivo_salida, 'w', encoding='utf-8') as file:
            json.dump(datos_por_asn, file, indent=4, ensure_ascii=False)

        # Paso 2: Leer el archivo JSON guardado y extraer los datos
        with open(archivo_salida, 'r', encoding='utf-8') as file:
            datos_json = json.load(file)

        # Extraer los datos para la ciudad buscada
        datos_ciudad = datos_json.get(asn_buscado, {}).get(city_name_buscado, {})

        # Paso 3: Leer el archivo de ubicación de IPs y actualizar los datos de la IP buscada
        with open(_Variables.IPlocation_basic_data, 'r', encoding='utf-8') as archivo:
            datos_ips = json.load(archivo)

        if ip_buscada in datos_ips:
            # Actualizar los valores con los datos extraídos o con valores de relleno si no se encontraron datos
            datos_ips[ip_buscada].update({
                "IP1": datos_ciudad.get("IP1", "-"),
                "IP2": datos_ciudad.get("IP2", "-"),
                "Proxy Type": datos_ciudad.get("Proxy Type", "-"),
                "ISP": datos_ciudad.get("ISP", "-"),
                "Domain": datos_ciudad.get("Domain", "-"),
                "Usage Type": datos_ciudad.get("Usage Type", "-"),
                "Threat": datos_ciudad.get("Threat", "-"),
                "Residential": datos_ciudad.get("Residential", "-"),
                "Provider": datos_ciudad.get("Provider", "-")
            })

            # Guardar los cambios en el archivo JSON
            with open(_Variables.IPlocation_basic_data, 'w', encoding='utf-8') as archivo:
                json.dump(datos_ips, archivo, indent=4, ensure_ascii=False)

#asn_inf
def Asn_inf(ip_buscada, asn_buscado):
    column_names = ['IP1', 'IP2', 'Rango IP (CIDR)', 'ASN', 'Centro de Información']

    def extraer_datos_fila(fila, column_names):
        datos = next(csv.reader([fila], delimiter=',', quotechar='"'))
        return dict(zip(column_names, datos))

    def buscar_datos_por_asn(archivo_csv, asn_buscado):
        resultados = {}

        with open(archivo_csv, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=',', quotechar='"')
            
            # Saltar la fila de encabezado si el archivo CSV tiene encabezados
            next(reader)

            for fila in reader:
                datos = extraer_datos_fila(','.join(fila), column_names)
                asn = datos.get('ASN', '')
                rango_ip = datos.get('Rango IP (CIDR)', '')

                # Verificar si el ASN coincide con el buscado
                if asn == asn_buscado:
                    if asn not in resultados:
                        resultados[asn] = {}
                    resultados[asn][rango_ip] = datos

        return resultados

    # Obtener todos los datos con el ASN encontrado
    datos_encontrados = buscar_datos_por_asn(_Variables.db_asn, asn_buscado)
    
    if datos_encontrados:
        # Guardar los datos en un archivo JSON
        archivo_salida = 'lib/resources/data/Asn_resultado.json'
        with open(archivo_salida, 'w', encoding='utf-8') as file:
            json.dump(datos_encontrados, file, indent=4, ensure_ascii=False)

        # Leer el archivo JSON con los datos de ASN y rangos IP
        with open(archivo_salida, 'r', encoding='utf-8') as archivo:
            datos_asn = json.load(archivo)

        if asn_buscado not in datos_asn:
            update_ui_track(_Variables.languages[_Variables.current_language]["track_error"])
            return

        rangos_ip = datos_asn[asn_buscado]
        ip_encontrada = None
        rango_encontrado = None

        # Convertir la IP buscada en un objeto ipaddress
        ip_buscada_obj = ipaddress.ip_address(ip_buscada)

        for rango, detalles in rangos_ip.items():
            # Convertir el rango CIDR en una red IP
            red = ipaddress.ip_network(rango, strict=False)
            
            if ip_buscada_obj in red:
                ip_encontrada = detalles
                rango_encontrado = rango
                break
            else:
                # Comparar si la IP es la más cercana dentro de este rango
                if rango_encontrado is None or red.overlaps(ipaddress.ip_network(rango_encontrado)):
                    ip_encontrada = detalles
                    rango_encontrado = rango

        # Leer el archivo JSON donde se actualizarán los datos
        with open(_Variables.IPlocation_basic_data, 'r', encoding='utf-8') as archivo:
            datos_ips = json.load(archivo)

        if ip_buscada in datos_ips:
            # Actualizar los datos de la IP buscada con el rango IP encontrado o con "-"
            datos_ips[ip_buscada]["Rango IP (CIDR)"] = ip_encontrada.get("Rango IP (CIDR)", "-") if ip_encontrada else "-"

            # Guardar los cambios en el archivo JSON
            with open(_Variables.IPlocation_basic_data, 'w', encoding='utf-8') as archivo:
                json.dump(datos_ips, archivo, indent=4, ensure_ascii=False)

#MAP
def load_json(json_file_path):
    """Función para leer el archivo JSON y extraer IPs e información relevante."""
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    
    ips = list(data.keys())
    info_dict = {}
    list_ip_isp = {}

    for ip in ips:
        nodo = data[ip].get('nodo', None)
        domain = data[ip].get('Domain', '-')
        
        if nodo is None:
            # Si 'nodo' no está presente, combinar 'ip' y 'domain'
            list_ip_isp[ip] = f"{ip} - {domain}"
        else:
            # Si 'nodo' está presente, usarlo directamente
            list_ip_isp[ip] = f"{ip} - {nodo}"

        info_dict[ip] = {
            'country_name': data[ip].get('country_name', '-'),
            'region_name': data[ip].get('region_name', '-'),
            'city_name': data[ip].get('city_name', '-'),
            'latitude': data[ip].get('latitude', 0.0),
            'longitude': data[ip].get('longitude', 0.0),
            'domain': domain  # Añadir el dominio a la información
        }

    return ips, info_dict, list_ip_isp

def create_map(ips_info):
    """Función para crear un mapa, agregar puntos basado en las IPs e información extraída, y conectarlos con una línea roja."""
    # Filtrar IPs con coordenadas válidas
    valid_locations = {
        ip: info for ip, info in ips_info.items()
        if info['latitude'] is not None and info['longitude'] is not None
        and isinstance(info['latitude'], (int, float)) and isinstance(info['longitude'], (int, float))
    }

    # Verificar que haya al menos una ubicación válida
    if not valid_locations:
        raise ValueError("No se encontraron ubicaciones válidas en los datos proporcionados.")

    # Usar la primera ubicación válida para centrar el mapa
    first_location = list(valid_locations.values())[0]
    m = folium.Map(location=[first_location['latitude'], first_location['longitude']], zoom_start=5)

    # Lista para almacenar las coordenadas de los puntos
    coordinates = []

    # Añadir puntos al mapa
    for ip, info in valid_locations.items():
        popup_name = f"{ip} - {info['country_name']} - {info['region_name']} - {info['city_name']}"
        folium.Marker(
            location=[info['latitude'], info['longitude']],
            popup=popup_name
        ).add_to(m)
        coordinates.append([info['latitude'], info['longitude']])  # Agregar coordenadas a la lista

    # Añadir la línea roja que conecta todos los puntos
    folium.PolyLine(coordinates, color="red", weight=2.5, opacity=1).add_to(m)

    # Ruta donde se guardará el archivo HTML del mapa
    map_path = os.path.join(os.getcwd(), "lib/resources/locat/map.html")  # Guardar el mapa en el directorio actual como map.html

    # Asegurarse de que el directorio exista
    os.makedirs(os.path.dirname(map_path), exist_ok=True)

    # Guardar el mapa en el archivo HTML especificado
    m.save(map_path)
    return map_path

def load_json_data(json_file_path):
    """Función para leer el archivo JSON y extraer la información."""
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    return data

def get_ip_data(ip, data):
    """Función para obtener los datos de una IP del diccionario cargado."""
    return data.get(ip, None)

def display_ip_details(ip, data, right_sub_frame):
    """Actualiza los cuadros en right_sub_frame con los detalles de la IP seleccionada."""
    ip_data = get_ip_data(ip, data)
    
    # Limpiar el contenido del right_sub_frame
    for widget in right_sub_frame.winfo_children():
        widget.destroy()
    
    if ip_data:
        details = {
            "Nodo": ip_data.get('nodo', '-'),
            "Country Code": ip_data.get('country_code', '-'),
            "Country Name": ip_data.get('country_name', '-'),
            "Region Name": ip_data.get('region_name', '-'),
            "City Name": ip_data.get('city_name', '-'),
            "Latitude": ip_data.get('latitude', '-'),
            "Longitude": ip_data.get('longitude', '-'),
            "ZIP Code": ip_data.get('zip_code', '-'),
            "Time Zone": ip_data.get('time_zone', '-'),
            "ASN": ip_data.get('asn', '-'),
            "AS": ip_data.get('as', '-'),
            "Is Proxy": ip_data.get('is_proxy', '-'),
            "IP1": ip_data.get('IP1', '-'),
            "IP2": ip_data.get('IP2', '-'),
            "Proxy Type": ip_data.get('Proxy Type', '-'),
            "ISP": ip_data.get('ISP', '-'),
            "Domain": ip_data.get('Domain', '-'),
            "Usage Type": ip_data.get('Usage Type', '-'),
            "Threat": ip_data.get('Threat', '-'),
            "Residential": ip_data.get('Residential', '-'),
            "Provider": ip_data.get('Provider', '-'),
            "Rango IP (CIDR)": ip_data.get('Rango IP (CIDR)', '-')
        }

        # Configuración de la cuadrícula
        num_columns = 4
        row = 0
        column = 0

        # Tamaño base para los cuadros
        padding = 10

        # Crear una fuente para medir el tamaño del texto
        title_font = ("Arial", 12, "bold")
        value_font = ("Arial", 10)

        # Crear un Label temporal para medir el tamaño del texto
        temp_label = tk.Label(right_sub_frame, font=title_font)
        max_width = 0
        max_height = 0

        for key, value in details.items():
            # Medir el ancho y la altura del texto
            temp_label.config(text=key)
            title_width = temp_label.winfo_reqwidth()
            title_height = temp_label.winfo_reqheight()
            
            temp_label.config(text=value, font=value_font)
            value_width = temp_label.winfo_reqwidth()
            value_height = temp_label.winfo_reqheight()

            # Calcular el tamaño del cuadro
            width = max(title_width, value_width) + 2 * padding
            height = title_height + value_height + 3 * padding  # Ajustar altura para incluir espacio entre título y valor

            # Crear un frame para contener el título y el dato
            content_frame = tk.Frame(
                right_sub_frame,
                bg="#e0e0e0",
                bd=2,
                relief="solid",
                padx=padding,
                pady=padding,
                width=width,
                height=height
            )
            content_frame.grid(row=row, column=column, padx=5, pady=5, sticky="nsew")

            # Crear el Label para el título
            title_label = tk.Label(
                content_frame,
                text=key,
                bg="#e0e0e0",
                font=title_font,
                anchor="w",
                wraplength=width - 2 * padding  # Ajustar el ancho del texto
            )
            title_label.pack()

            # Crear el Label para el valor
            data_label = tk.Label(
                content_frame,
                text=value,
                bg="#e0e0e0",
                font=value_font,
                anchor="w",
                wraplength=width - 2 * padding  # Ajustar el ancho del texto
            )
            data_label.pack()

            # Actualizar el índice de fila y columna
            column += 1
            if column >= num_columns:
                column = 0
                row += 1

        # Configurar el grid para ajustar la expansión
        for i in range(row + 1):
            right_sub_frame.grid_rowconfigure(i, weight=1)
        for j in range(num_columns):
            right_sub_frame.grid_columnconfigure(j, weight=1)
    else:
        tk.Label(
            right_sub_frame,
            text="No data available for the selected IP",
            bg="#e0e0e0",
            font=("Arial", 12),
            padx=10,
            pady=10
        ).pack()

def ShowMap():
    # Crear la ventana principal
    root = tk.Tk()
    root.title("NetStatus_v1.0 - Tracking details")
    
    # Obtener el tamaño de la pantalla
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    root.geometry(f"{screen_width}x{screen_height}+0+0")

    # Crear el PanedWindow
    paned_window = tk.PanedWindow(root, orient="horizontal")
    paned_window.pack(fill="both", expand=True)

    # Definir el ancho personalizado para el left_sub_frame
    left_frame_width = int(screen_width * 0.3)  # Ejemplo: 30% del ancho de la pantalla
    
    # Crear el left_sub_frame con el ancho personalizado
    left_sub_frame = tk.Frame(paned_window, bg="#ffffff", width=left_frame_width)
    paned_window.add(left_sub_frame, minsize=left_frame_width)  # Añadir el frame izquierdo al PanedWindow

    # Crear el right_sub_frame que ocupará el resto del espacio
    right_sub_frame = tk.Frame(paned_window, bg="#ffffff")
    paned_window.add(right_sub_frame)  # Añadir el frame derecho al PanedWindow
    
    # Crear un Treeview en el left_sub_frame
    tree = ttk.Treeview(left_sub_frame, show='tree')  # Eliminar cabeceras con show='tree'
    tree.pack(fill="both", expand=True)

    # Cargar los datos del JSON
    data = load_json_data(_Variables.IPlocation_basic_data)
    ips, ips_info, list_ip_isp = load_json(_Variables.IPlocation_basic_data)

    # Insertar cada IP y nodo (o dominio) en el Treeview como una fila
    for ip, info in list_ip_isp.items():
        tree.insert("", "end", text=ip)  # Usa IP como texto de la fila

    # Configurar el grid para el right_sub_frame
    num_rows = 6
    num_columns = 4

    # Tamaño fijo para los cuadros
    frame_width = 120
    frame_height = 60

    for i in range(num_rows):
        right_sub_frame.grid_rowconfigure(i, weight=1)
    for j in range(num_columns):
        right_sub_frame.grid_columnconfigure(j, weight=1)

    # Función para manejar la selección en el Treeview
    def on_treeview_select(event):
        selected_item = tree.selection()
        if selected_item:
            selected_ip = tree.item(selected_item[0], 'text')  # Obtener IP de la fila seleccionada
            display_ip_details(selected_ip, data, right_sub_frame)

    # Configurar el Treeview para manejar la selección
    tree.bind('<<TreeviewSelect>>', on_treeview_select)

    # Crear el mapa y guardar la ruta del archivo
    map_path = create_map(ips_info)

    # Abrir el mapa en el navegador
    try:
        webbrowser.open(f'file://{map_path}')
    except Exception as e:
        print(f"Error al abrir el mapa en el navegador: {e}")

    root.mainloop()