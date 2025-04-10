import socket
import threading
import requests

def handle_client(connection):
    while True:
        try:
            length_data = connection.recv(8)
            if not length_data:
                break
            length = int(length_data.decode().strip())
            request_data = connection.recv(length).decode()

            print(f"[Server] Got request:\n{request_data}")

            lines = request_data.split("\r\n")
            first_line = lines[0].split()
            method, url = first_line[0], first_line[1]

            response = requests.request(method, url)

            connection.sendall(f"{len(response.content):08}".encode())
            connection.sendall(response.content)

        except Exception as e:
            print(f"[Server] Error: {e}")
            break
    connection.close()

def start_proxy_server(host="0.0.0.0", port=9999):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    print(f"[Server] Listening on {host}:{port}")

    while True:
        conn, addr = server.accept()
        print(f"[Server] Connection from {addr}")
        threading.Thread(target=handle_client, args=(conn,)).start()

if __name__ == "__main__":
    start_proxy_server()