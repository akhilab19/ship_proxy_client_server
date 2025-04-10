import socket
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Lock

class ProxyHandler(BaseHTTPRequestHandler):
    lock = Lock()
    backend = socket.create_connection(('proxy_server', 9999))

    def do_GET(self):
        with ProxyHandler.lock:
            request_line = f"{self.command} {self.path} HTTP/1.1\r\n"
            headers = ''.join(f"{k}: {v}\r\n" for k, v in self.headers.items())
            full_request = (request_line + headers + "\r\n").encode()

            ProxyHandler.backend.sendall(f"{len(full_request):08}".encode())
            ProxyHandler.backend.sendall(full_request)

            length = int(ProxyHandler.backend.recv(8).decode())
            response = ProxyHandler.backend.recv(length)

            self.send_response(200)
            self.end_headers()
            self.wfile.write(response)

def run_proxy(host='0.0.0.0', port=8080):
    httpd = HTTPServer((host, port), ProxyHandler)
    print(f"[Ship Proxy] Listening on {host}:{port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run_proxy()