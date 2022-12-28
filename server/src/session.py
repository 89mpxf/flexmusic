# Import dependencies
from socket import socket

# Import local dependencies
from src.protocol.client_handler import ClientHandler

class SessionManager:
    def __init__(self):
        self._sessions = []

    @property
    def sessions(self) -> list[ClientHandler]:
        return self._sessions

    def add_session(self, session: ClientHandler):
        self._sessions.append(session)

    def remove_session(self, session: ClientHandler):
        self._sessions.remove(session)

def session_bootstrapper(sock: socket, addr: tuple[str, int], session_manager: SessionManager):
    session = ClientHandler(sock, addr, session_manager)
    session.start()
    session_manager.add_session(session)