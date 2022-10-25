# Import dependencies
import json

# Import local dependencies
from ..services.youtube import YoutubeServiceHandler

class ClientRouter(object):
    def __init__(self):
        self.YoutubeServiceHandler = YoutubeServiceHandler()

    def route(self, data):
        if data["service"] == "youtube":
            if data["operation"] == "search":
                output = self.YoutubeServiceHandler.search(data["payload"]["query"], data["payload"]["amount"])
                return {"success": True, "response": output}
