import tkinter as tk
from tkinter import ttk
import json
import os
import psutil

import _Variables

# call funtion Update_all with the frame window_Netstat and the actual theme
def update_periodically(tree, frame, theme, label1):
    gather_network_data()
    update_treeview(tree)

    # count open port ans update var Variables.open_port
    count_open_ports = sum(1 for item in tree.get_children() if tree.item(item, 'values')[5] in ["LSN", "EST"])
    _Variables.open_ports = count_open_ports
    
    # update label text
    label1.config(text=f"Open Ports: {_Variables.open_ports}")
    
    # set the new update every 10 seconds
    frame.after(10000, update_periodically, tree, frame, theme, label1)

#TREEVIEW#
def column_row_click(event, theme):
    # Get the column that was clicked
    column_id = tree.identify_column(event.x)
    # Get the row that was clicked
    row_id = tree.identify_row(event.y)
    
    # Check if the clicked column is "Status" (column identifier #6)
    if column_id == "#6" and not row_id:  # Make sure it is not a row
        # Get the text of the clicked column
        column_text = tree.heading(column_id)["text"]
        
        # Show a box with text only for the "Status" column
        text = (
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
        show_tooltip(event.x_root, event.y_root, text, theme)

def show_tooltip(x, y, text, theme):
    # Create a Toplevel window as a tooltip
    tooltip = tk.Toplevel(tree)
    tooltip.wm_overrideredirect(True)  # Remove window borders
    tooltip.geometry(f"+{x}+{y}")  # Position the tooltip

    # Add a Label with the text
    label = tk.Label(
        tooltip, 
        text=text, 
        bg=theme["bg_color"],
        fg=theme["fg_color"],  # Tooltip text
        relief="solid", 
        borderwidth=1
    )
    label.pack()

    tooltip.update_idletasks()
    # destroy tooltip after a while
    tooltip.after(2000, tooltip.destroy)

def show_context_menu(event, theme):
    # get selected item
    item = tree.identify_row(event.y)
    
    if item:
        # show the context menu in the mouse position
        context_menu.post(event.x_root, event.y_root)

def crear_treeview(parent, theme):
    global tree
    tree = ttk.Treeview(parent, columns=("col1", "col2", "col3", "col4", "col5", "col6"), show="headings")

    # define the colums header
    tree.heading("col1", text="PORT")
    tree.heading("col2", text="PID")
    tree.heading("col3", text="LAND")
    tree.heading("col4", text="WAN")
    tree.heading("col5", text="SERVICE")
    tree.heading("col6", text="STATUS")

    # Set column widths and disable resizing
    column_widths = {
        "col1": 50,
        "col2": 60,
        "col3": 115,
        "col4": 115,
        "col5": 80,
        "col6": 70
    }

    for col, width in column_widths.items():
        tree.column(col, width=width, anchor="center", stretch=False)

    # create a contextual menu
    global context_menu
    context_menu = tk.Menu(tree, tearoff=0)
    context_menu.add_command(label="Opción 1", bg=theme["bg_color"], fg=theme["fg_color"])
    context_menu.add_command(label="Opción 2", bg=theme["bg_color"], fg=theme["fg_color"])
    

    # add treeview to the container
    tree.pack(expand=True, fill="both")

    # create a vertical scrollbar
    scrollbar = ttk.Scrollbar(tree, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    # disable the resizing
    def fixed_column_width(event):
        for col, width in column_widths.items():
            tree.column(col, width=width)
    
    tree.bind('<Motion>', fixed_column_width)
    tree.bind("<Button-1>", lambda event: column_row_click(event, theme))
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

    _Variables.open_ports = count_est + count_lsn

    # Opcional: Forzar actualización de todos los widgets
    tree.update_idletasks()

#STATUS TOP BAR#
def create_stat_bar(frame):
    theme = _Variables.Actual_teme
    # Crear el marco para la barra de estado
    stat_bar = tk.Frame(frame, bg=theme["bg_color"], height=20)
    stat_bar.pack(side='top', fill='x')

    label1 = tk.Label(stat_bar, text=f"Open Ports: {_Variables.open_ports}", bg=theme["bg_color"], fg=theme["fg_color"])
    label1.pack(side='left', padx=5)
    
    return label1

#main funtion show frame NetStat
def Win_NetStat(frame, theme, *args):
    _Variables.Actual_teme = theme
    gather_network_data()
        
    window_Netstat = tk.Frame(frame, bg=theme["bg_color"])
    window_Netstat.pack(side="top", fill="both", expand=True)

    #create treeview
    tree = crear_treeview(window_Netstat, theme)
    label1 = create_stat_bar(frame) #bottom bar
    update_periodically(tree, window_Netstat, theme, label1) #every 10 secons update data on bottom bar and treeview data.
    
    return window_Netstat

#DATA#
#JSON LOCAL DATA
def update_json_with_option(file_path, key, value):
    # Verificar si el archivo existe
    if not os.path.exists(file_path):
        # Crear un archivo nuevo con la estructura inicial
        data = {"options": []}
    else:
        # Leer el contenido del archivo existente
        with open(file_path, 'r') as file:
            data = json.load(file)

    # Buscar si la opción ya existe
    option_exists = False
    for option in data["options"]:
        if key in option:
            # Si la opción existe, actualizar el valor
            option[key] = value
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

def assign_variables_from_json(data):
    for option in data.get("options", []):
        if "theme" in option:
            _Variables.theme = option["theme"]

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
        # Obtener la información de la conexión
        process_name = psutil.Process(conn.pid).name() if conn.pid else 'Unknown Process'
        local_address = f"{conn.laddr.ip}:{conn.laddr.port}"
        remote_address = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else 'N/A'
        
        # Usar abreviatura para el estado
        short_status = status_mapping.get(conn.status, conn.status)
        
        if short_status == "NONE": continue
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

        #guardar datos al json
        with open(filename, 'w') as file:
            json.dump(network_data, file, indent=4)