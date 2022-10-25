# Import dependencies
import socket
from threading import enumerate, Thread

# Import local dependencies
from src.protocol.client_handler import ClientHandler
from src.motd import splash

def start_server(host: str = "0.0.0.0", port: int = 5000):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    splash(host, port)
    return server

def run_server(server):
    try:
        while True:
            server.listen(5)
            sock, addr = server.accept()
            ClientHandler(sock, addr).start()
    except KeyboardInterrupt:
        pass
    except:
        raise

if __name__ == '__main__':
    run_server(start_server())