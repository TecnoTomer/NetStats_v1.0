import ctypes 

def alerta_ok(Windows_title, title, text):
	hwnd = ctypes.windll.user32.FindWindowW(None, Windows_title)
	result = ctypes.windll.user32.MessageBoxW(hwnd, text, title, 64)
	return result

def alerta_error(Windows_title, title, text):
	hwnd = ctypes.windll.user32.FindWindowW(None, Windows_title)
	result = ctypes.windll.user32.MessageBoxW(hwnd, text, title, 18)
	return result

def alerta_aceptar(Windows_title, title, text):
	hwnd = ctypes.windll.user32.FindWindowW(None, Windows_title)
	result = ctypes.windll.user32.MessageBoxW(hwnd, text, title, 33)
	return result

def alerta_aceptar_sin(title, text): #sin ser hijo de otra ventana con el titulo
	hwnd = None
	result = ctypes.windll.user32.MessageBoxW(hwnd, text, title, 33)
	return result

def alerta_cerrar(Windows_title, title, text):
	hwnd = ctypes.windll.user32.FindWindowW(None, Windows_title)
	result = ctypes.windll.user32.MessageBoxW(hwnd, text, title, 52)
	return result

def alerta_Amarilla(Windows_title, title, text):
	hwnd = ctypes.windll.user32.FindWindowW(None, Windows_title)
	result = ctypes.windll.user32.MessageBoxW(hwnd, text, title, 48)
	return result
