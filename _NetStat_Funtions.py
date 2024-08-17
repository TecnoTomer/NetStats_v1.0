import tkinter as tk
from tkinter import ttk
import json
import os
import psutil
import sys
import importlib
import win32serviceutil
import time
import threading
import subprocess

import _Variables
import _Buttons_Funtions
import _TrackIp_Funtions

last_event = None

# call funtion Update_all with the frame window_Netstat and the actual theme
def update_periodically(tree, frame, theme, label1, label2):
    gather_network_data()
    update_treeview(tree)

    # count open port ans update var Variables.open_port
    count_open_ports = sum(1 for item in tree.get_children() if tree.item(item, 'values')[5] in ["LSN", "EST"])
    _Variables.open_ports = count_open_ports
    
    # update label text
    label1.config(text=f"Total Ports: {_Variables.total_ports}")
    label2.config(text=f"Open Ports: {_Variables.open_ports}")
    
    # set the new update every 10 seconds
    frame.after(10000, update_periodically, tree, frame, theme, label1, label2)

#TREEVIEW#
def column_row_click(event, *text_inf, **theme):
    # Get the column that was clicked
    column_id = tree.identify_column(event.x)
    # Get the row that was clicked
    row_id = tree.identify_row(event.y)
    
    # Check if the clicked column is "Status" (column identifier #6)
    if column_id == "#6" and not row_id:  # Make sure it is not a row
        # Get the text of the clicked column
        column_text = tree.heading(column_id)["text"]
        
        # Show a box with text only for the "Status" column
        
        show_tooltip(event.x_root, event.y_root, *text_inf, **theme)

def row_click(event, *text_inf, **theme):
    # Obtener el identificador de columna y fila donde se hizo clic
    column_id = tree.identify_column(event.x)
    row_id = tree.identify_row(event.y)
    
    if row_id:  # Asegúrate de que se hizo clic en una fila válida
        # Mostrar el tooltip con el texto de la celda clickeada
        show_tooltip(event.x_root, event.y_root, *text_inf, **theme)

def show_tooltip(x, y, text, theme):
    _Variables.current_tooltip

    # Si ya hay un tooltip activo, destrúyelo
    if _Variables.current_tooltip is not None:
        _Variables.current_tooltip.destroy()

    # Crear un nuevo Toplevel window como tooltip
    tooltip = tk.Toplevel(tree)
    tooltip.wm_overrideredirect(True)  # Eliminar bordes de ventana
    tooltip.geometry(f"+{x}+{y}")  # Posicionar el tooltip

    # Añadir una etiqueta con el texto
    label = tk.Label(
        tooltip, 
        text=text, 
        bg=theme["bg_color"],
        fg=theme["fg_color"],  # Texto del tooltip
        relief="solid", 
        borderwidth=1
    )
    label.pack()

    # Actualizar y almacenar el tooltip actual
    tooltip.update_idletasks()
    _Variables.current_tooltip = tooltip

    # Destruir el tooltip después de un tiempo
    tooltip.after(2000, lambda: destroy_tooltip())

def destroy_tooltip():
    if _Variables.current_tooltip is not None:
        _Variables.current_tooltip.destroy()
        _Variables.current_tooltip = None

def show_context_menu(event, theme):
    # get selected item
    item = tree.identify_row(event.y)
    global last_event
    if item:
        # show the context menu in the mouse position
        last_event = event  # Almacenar el evento
        context_menu.post(event.x_root, event.y_root)

def crear_treeview(parent, theme):
    # Estilo para el Treeview
    style = ttk.Style()
    style.configure("Custom.Treeview", 
                    font=_Variables.poppins,
                    background=theme["bg_color"],  # Color de fondo
                    fieldbackground=theme["bg_color"],  # Color de fondo de los campos
                    foreground=theme["fg_color"])  # Color del texto

    global tree
    tree = ttk.Treeview(parent, style="Custom.Treeview", columns=("col1", "col2", "col3", "col4", "col5", "col6"), show="headings")

    # define the colums header
    tree.heading("col1", text=_Variables.languages[_Variables.current_language]["Port"])
    tree.heading("col2", text=_Variables.languages[_Variables.current_language]["Pid"])
    tree.heading("col3", text=_Variables.languages[_Variables.current_language]["Local_IP"])
    tree.heading("col4", text=_Variables.languages[_Variables.current_language]["Remote_IP"])
    tree.heading("col5", text=_Variables.languages[_Variables.current_language]["Service"])
    tree.heading("col6", text=_Variables.languages[_Variables.current_language]["Status"])

    # Set column widths and disable resizing
    column_widths = {
        "col1": 50,
        "col2": 60,
        "col3": 120,
        "col4": 120,
        "col5": 80,
        "col6": 70
    }

    for col, width in column_widths.items():
        tree.column(col, width=width, anchor=tk.CENTER)
    global context_menu
    context_menu = tk.Menu(tree, tearoff=0)
    context_menu.config(
        font=_Variables.poppins,
        background=theme["bg_color"],
        foreground=theme["fg_color"],
        activebackground=theme["on_enter"],
        activeforeground=theme["activeforeground"],
        relief='flat',
        bd=1
    )

    def execute_details():
        if last_event:
            _Buttons_Funtions.B_details(last_event)

    def execute_Trackip():
        if last_event:
            get_selected_item_data()
            if _Variables._wan:
                if _Variables._wan == "N/A":
                    update_ui(_Variables.languages[_Variables.current_language]["pid"])
                elif ':' in _Variables._wan:
                    ip, port = _Variables._wan.split(":")
                    _Variables.ip_insert_entry = ip
                    _Buttons_Funtions.B_TrackIp(last_event, _Variables.app_controller)


    #context_menu when click some treeview row
    context_menu.add_command(label=_Variables.languages[_Variables.current_language]['Reboot'], command=restart_service)
    context_menu.add_command(label=_Variables.languages[_Variables.current_language]['Details'], command=execute_details)
    context_menu.add_command(label=_Variables.languages[_Variables.current_language]['Track_IP'], command=execute_Trackip)
    context_menu.add_command(label=_Variables.languages[_Variables.current_language]['Kill_Task'], command=_Kill)
    context_menu.add_command(label=_Variables.languages[_Variables.current_language]['Properties'])
    context_menu.add_command(label=_Variables.languages[_Variables.current_language]['Search_Online'])
    context_menu.add_command(label=_Variables.languages[_Variables.current_language]['Show_in_Folder'])

    # add treeview to the container
    tree.pack(expand=True, fill=tk.BOTH)

    # disable the resizing
    def fixed_column_width(event):
        for col, width in column_widths.items():
            tree.column(col, width=width)
    
    tree.bind('<Motion>', fixed_column_width)
    tree.bind("<Button-1>", lambda event: column_row_click(event, _Variables.colum_text_inf if _Variables.current_language == 'en' else _Variables.colum_text_inf_es, theme))
    tree.bind("<Button-3>", lambda event: show_context_menu(event, theme))

    return tree

def update_treeview(tree):
    # Leer el archivo JSON
    file_path = _Variables.rute_network_data
    try:
        with open(file_path, 'r') as file:
            data_dict = json.load(file)
    except FileNotFoundError:
        print(f"El archivo {file_path} no se encontró.")
        return
    except json.JSONDecodeError:
        print("Error al decodificar el archivo JSON.")
        return
    
    # Limpia el contenido existente del TreeView
    for item in tree.get_children():
        tree.delete(item)

    # Variables para contar los puertos en estado LSN y EST
    count_lsn = 0
    count_est = 0
    _Variables.open_ports = 0

    # Procesar los datos JSON para convertirlos en el formato requerido
    data = []
    for process_name, entries in data_dict.items():
        for entry in entries:
            # Extraer valores del JSON y construir las tuplas
            data.append((
                str(entry["Port"]),          # Columna 1: Port
                str(entry["Pid"]),           # Columna 2: PID
                entry["Land"],               # Columna 3: Land
                entry["Wan"],                # Columna 4: WAN
                process_name,                # Columna 5: Service
                entry["Status"]              # Columna 6: Status
            ))

            # Contar los estados LSN y EST
            if entry["Status"] == "LSN":
                count_lsn += 1
            elif entry["Status"] == "EST":
                count_est += 1

    # Insertar los datos en el TreeView
    for item in data:
        tree.insert("", "end", values=item)

    # Asegurarse de que haya al menos 23 filas en total
    total_rows = len(data)
    empty_rows_needed = 29 - total_rows

    for _ in range(empty_rows_needed):
        # Insertar filas vacías si se necesitan
        tree.insert("", "end", values=("", "", "", "", "", ""))

    _Variables.open_ports = count_est + count_lsn
    _Variables.total_ports = total_rows

    # Opcional: Forzar actualización de todos los widgets
    tree.update_idletasks()

#STATUS TOP BAR#
def create_stat_bar(frame):
    theme = _Variables.inicial_theme
    # Crear el marco para la barra de estado
    stat_bar = tk.Frame(frame, bg=theme["bg_color"], height=20)
    stat_bar.pack(side='top', fill='x')

    label1 = tk.Label(stat_bar, text=f"Total Ports: {_Variables.total_ports}", bg=theme["bg_color"], fg=theme["fg_color"])
    label1.pack(side='left', padx=5)

    label2 = tk.Label(stat_bar, text=f"Open Ports: {_Variables.open_ports}", bg=theme["bg_color"], fg=theme["fg_color"])
    label2.pack(side='left', padx=5)
    
    return label1, label2

#main funtion show frame NetStat
def Win_NetStat(frame, theme, *args):
    _Variables.inicial_theme = theme
    gather_network_data()
        
    window_Netstat = tk.Frame(frame, bg=theme["bg_color"])
    window_Netstat.pack(side="top", fill="both", expand=True)

    #create treeview
    global tree
    tree = crear_treeview(window_Netstat, theme)
    label1, label2 = create_stat_bar(frame) #bottom bar
    update_periodically(tree, window_Netstat, theme, label1, label2) #every 10 secons update data on bottom bar and treeview data.
    
    return window_Netstat

#DATA#
#read data of treeview row select
def get_selected_item_data():
    selected_item = tree.selection()
    
    if not selected_item:
        return None  # No hay selección
    
    item_id = selected_item[0]
    item_data = tree.item(item_id, "values")

    _Variables._port = item_data[0]
    _Variables._pid = item_data[1]
    _Variables._land = item_data[2]
    _Variables._wan = item_data[3]
    _Variables._service = item_data[4]
    _Variables._status = item_data[5]

#button submenu treeview reboot
def restart_service():
    get_selected_item_data()
    global last_event
    if last_event:
        # Ejecutar el proceso en un hilo separado para evitar que la interfaz se congele
        threading.Thread(target=_restart_service_process).start()

def _restart_service_process():
    try:
        # Detener el servicio
        update_ui(_Variables.languages[_Variables.current_language]["stop_service"])
        win32serviceutil.StopService(_Variables._service)
        win32serviceutil.WaitForServiceStatus(_Variables._service, win32serviceutil.SERVICE_STOPPED)
        update_ui(_Variables.languages[_Variables.current_language]["done"])
        
        # Esperar antes de reiniciar
        time.sleep(4)
        
        # Iniciar el servicio
        update_ui(_Variables.languages[_Variables.current_language]["staring_service"])
        win32serviceutil.StartService(_Variables._service)
        win32serviceutil.WaitForServiceStatus(_Variables._service, win32serviceutil.SERVICE_RUNNING)
        update_ui(_Variables.languages[_Variables.current_language]["done"])

    except Exception as e:
        update_ui(_Variables.languages[_Variables.current_language]["error"])

def _Kill():
    get_selected_item_data()
    try:
        # Ejecutar el comando taskkill con el PID
        subprocess.run(["taskkill", "/PID", str(_Variables._pid), "/F"], check=True)
        update_ui(_Variables.languages[_Variables.current_language]["stop_process"])
    except subprocess.CalledProcessError or Exception as e:
        update_ui(_Variables.languages[_Variables.current_language]["error"])

def update_ui(message):
    # Esta función actualiza la interfaz de usuario. Asegúrate de que sea segura para el hilo.
    # Usualmente, usarás un método de hilo seguro como `after` en Tkinter.
    if last_event:
        row_click(last_event, message, _Variables.inicial_theme)

#JSON LOCAL DATA STATE OPTIONS
def update_json_with_option(file_path, key, value):
    # Verificar si el archivo existe
    if not os.path.exists(file_path):
        # Crear un archivo nuevo con la estructura inicial
        data = {"options": []}
    else:
        # Leer el contenido del archivo existente
        with open(file_path, 'r') as file:
            data = json.load(file)

    option_exists = False
    # Buscar si la opción ya existe

    for option in data["options"]:
        if key in option:
            option_exists = True
            break

    if not option_exists:
        # Añadir la nueva opción si no está presente
        data["options"].append({key: value})

    # Guardar el archivo actualizado
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

    # Devolver el contenido actualizado
    return data

def read_json_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    else:
        return {}

#JSON LOCAL DATA NETSTAT SCAN
def gather_network_data():
    # Diccionario para almacenar los datos
    network_data = {}
    filename = _Variables.rute_network_data
    
    # Mapeo de estados a abreviaturas
    status_mapping = {
        "ESTABLISHED": "EST",
        "LISTEN": "LSN",
        "CLOSE_WAIT": "CW",
        "TIME_WAIT": "TW",
        "SYN_SENT": "SYN",
        "SYN_RECEIVED": "SYN-R",
        "FIN_WAIT1": "FW1",
        "FIN_WAIT2": "FW2",
        "CLOSE": "CLOSE",
        "CLOSING": "CLOS",
        "LAST_ACK": "LA",
        "UNKNOWN": "UNK"
    }

    # Obtener todas las conexiones de red
    for conn in psutil.net_connections(kind='inet'):
        # Filtrar solo IPv4
        if ":" in conn.laddr.ip:  # Esto excluye las direcciones IPv6
            continue
        
        # Excluir direcciones que no sean "0.0.0.0" o "192.168.x.x"
        if conn.laddr.ip not in ["0.0.0.0"] and not conn.laddr.ip.startswith("192.168."):
            continue
        
        # Obtener la información de la conexión
        process_name = psutil.Process(conn.pid).name() if conn.pid else 'Unknown Process'
        local_address = f"{conn.laddr.ip}:{conn.laddr.port}"
        remote_address = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else 'N/A'
        
        # Usar abreviatura para el estado
        short_status = status_mapping.get(conn.status, conn.status)
        
        if short_status == "NONE": 
            continue
        
        # Crear el diccionario para la conexión
        connection_info = {
            "Port": conn.laddr.port,
            "Pid": conn.pid,
            "Land": conn.laddr.ip,
            "Wan": remote_address,
            "Status": short_status
        }
        
        # Agregar la información al diccionario principal
        if process_name not in network_data:
            network_data[process_name] = []
        network_data[process_name].append(connection_info)

    # Guardar datos en el archivo JSON
    with open(filename, 'w') as file:
        json.dump(network_data, file, indent=4)