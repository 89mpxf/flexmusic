# Import dependencies
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR

# Import local dependencies
from src.protocol.client_handler import ClientHandler
from src.motd import splash

def start_server(host: str = "0.0.0.0", port: int = 5000) -> socket:
    server = socket(AF_INET, SOCK_STREAM)
    server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
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