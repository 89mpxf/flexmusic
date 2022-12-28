# Import dependencies
from datetime import datetime

def logTime() -> str:
    return " [" + str(datetime.now().strftime("%a %b %d %H:%M:%S")) + "] "