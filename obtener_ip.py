import socket

def obtener_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        return ip
    except Exception:
        return None

if __name__ == "__main__":
    ip = obtener_ip()
    if ip:
        print(ip)
    else:
        print("No se pudo obtener la IP")