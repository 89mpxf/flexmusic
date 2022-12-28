# Import local dependencies
from .session import SessionManager
from .util import logTime

def shutdown(session_manager: SessionManager):
    print(logTime() + "Received server shutdown signal.")
    for session in session_manager.sessions:
        print(logTime() + f"Closing connection to {session.addr[0]}:{session.addr[1]}...")
        session.close()
    print(logTime() + "Server shutdown complete.")