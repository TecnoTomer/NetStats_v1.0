import ctypes 

def alerta_ok(titulo_ventana, titulo, texto):
	hwnd = ctypes.windll.user32.FindWindowW(None, titulo_ventana)
	resultado = ctypes.windll.user32.MessageBoxW(hwnd, texto, titulo, 64)
	return resultado

def alerta_error(titulo_ventana, titulo, texto):
	hwnd = ctypes.windll.user32.FindWindowW(None, titulo_ventana)
	resultado = ctypes.windll.user32.MessageBoxW(hwnd, texto, titulo, 18)
	return resultado

def alerta_aceptar(titulo_ventana, titulo, texto):
	hwnd = ctypes.windll.user32.FindWindowW(None, titulo_ventana)
	resultado = ctypes.windll.user32.MessageBoxW(hwnd, texto, titulo, 33)
	return resultado

def alerta_aceptar_sin(titulo, texto): #sin ser hijo de otra ventana con el titulo
	hwnd = None
	resultado = ctypes.windll.user32.MessageBoxW(hwnd, texto, titulo, 33)
	return resultado

def alerta_cerrar(titulo_ventana, titulo, texto):
	hwnd = ctypes.windll.user32.FindWindowW(None, titulo_ventana)
	resultado = ctypes.windll.user32.MessageBoxW(hwnd, texto, titulo, 52)
	return resultado

def alerta_Amarilla(titulo_ventana, titulo, texto):
	hwnd = ctypes.windll.user32.FindWindowW(None, titulo_ventana)
	resultado = ctypes.windll.user32.MessageBoxW(hwnd, texto, titulo, 48)
	return 
