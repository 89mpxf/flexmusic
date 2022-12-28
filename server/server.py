# Import dependencies
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR

# Import local dependencies
from src.motd import splash
from src.session import SessionManager, session_bootstrapper

def start_server(host: str = "0.0.0.0", port: int = 5000) -> socket:
    server = socket(AF_INET, SOCK_STREAM)
    server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server.bind((host, port))
    splash(host, port)
    return server

def run_server(server):
    session_manager = SessionManager()
    try:
        while True:
            server.listen(5)
            sock, addr = server.accept()
            session_bootstrapper(sock, addr, session_manager)
    except KeyboardInterrupt:
        pass
    except:
        raise

if __name__ == '__main__':
    run_server(start_server())