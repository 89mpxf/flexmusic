# Import dependencies
from socket import socket

# Import local dependencies
from .session import SessionManager
from .util import logTime

def shutdown(session_manager: SessionManager):
    print(logTime() + "Received server shutdown signal")
    for session in session_manager.sessions:
        print(logTime() + f"Closing connection to {session.addr[0]}:{session.addr[1]}...")
        session.close()

def close_server(server: socket):
    print(logTime() + "Server shutdown successfully")
    server.close()