#!/usr/bin/env python
import http.server, ssl, socket

def get_lan_ip():
    # Opens a dummy connection to find the LAN IP used
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Doesn't need to be reachable
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

ip = get_lan_ip()

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")

server_address = (ip, 8443)
httpd = http.server.HTTPServer(server_address, http.server.SimpleHTTPRequestHandler)

httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
print(f"Serving on https://{ip}:8443")
httpd.serve_forever()
