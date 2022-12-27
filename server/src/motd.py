# Import dependencies
from platform import platform, python_version, python_compiler, python_implementation, system

def splash(hostname, port):
    print("")
    print(" FlexMusic Server")
    print(" Open-source music backend server for Discord")
    print("")
    print(f" Listening for connections on {hostname}:{port}")
    print("")
    print(f" OS: {platform()}")
    print(f" Python: {python_version()} [{python_implementation()} ({python_compiler()})]")
    print("")