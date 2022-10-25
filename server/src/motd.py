# Import dependencies
import platform

def splash(hostname, port):
    print("")
    print(" FlexMusic Server")
    print(" Open-source socket-based music streaming server for Discord")
    print("")
    print(f" Running on {hostname}:{port}")
    print(f" OS: {platform.platform()}")
    print("")