# Import dependencies
from socket import socket
from traceback import TracebackException

# Import local dependencies
from .session import SessionManager
from .util import logTime

def shutdown(session_manager: SessionManager):
    print(logTime() + "Received server shutdown signal")
    for session in session_manager.sessions:
        print(logTime() + f"Closing connection to {session.addr[0]}:{session.addr[1]}...")
        session.close()

def error_shutdown(error: Exception, session_manager: SessionManager):
    print("")
    print(" A fatal error occured while running the server and the server must shut down.")
    print(" A full traceback of the error can be found below:")
    print("")
    print("".join(TracebackException.from_exception(error).stack.format()))
    print("")
    print(" Under normal circumstances, this message should never seen by the user.")
    print(" Please report this error at: ")
    print(" https://github.com/89mpxf/flexmusic/issues")
    print("")
    return shutdown(session_manager)

def close_server(server: socket):
    print(logTime() + "Server shutdown successfully")
    server.close()