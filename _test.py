from ping3 import ping

def verificar_ip_ping3(ip, num_pings=6, min_respuestas_validas=3):
    respuestas_validas = 0

    for _ in range(num_pings):
        respuesta = ping(ip)
        if respuesta:
            respuestas_validas += 1

    return respuestas_validas >= min_respuestas_validas

# Ejemplo de usos
ip = "20.44.229.112"  # Google DNS
if verificar_ip_ping3(ip):
    print(f"La IP {ip} está activa y respondió a suficientes pings.")
else:
    print(f"La IP {ip} no respondió a suficientes pings.")
