# Import dependencies
from json import JSONDecodeError, loads, dumps
from threading import Thread

# Import local dependencies
from ..util import logTime
from .client_router import ClientRouter

class ClientHandler(Thread):
    def __init__(self, sock, addr):
        Thread.__init__(self)
        self.daemon = True
        self.addr, self.sock = addr, sock
        self.router = ClientRouter()
        print(logTime() + f"Connection established with {addr[0]}:{addr[1]} successfully")

    def run(self):
        try:
            while True:
                data = self.sock.recv(65536) ### MAIN DATA RECEIVE
                if not data:
                    return self.close()
                print(logTime() + f"Request received from {self.addr[0]}:{self.addr[1]}: " + data.decode())
                result = self.router.route(loads(data.decode()))
                self.sock.send(dumps(result).encode()) ### MAIN DATA RESPONSE
        except BrokenPipeError:
            print(logTime() + f"Connection from {self.addr[0]}:{self.addr[1]} closed unexpectedly")
            return self.close()
        except JSONDecodeError:
            print(logTime() + f"Connection from {self.addr[0]}:{self.addr[1]} closed from sending a bad request")
            return self.close()
        except:
            raise
        
    def close(self):
        print(logTime() + f"Terminated connection from {self.addr[0]}:{self.addr[1]} successfully")
        return self.sock.close()
