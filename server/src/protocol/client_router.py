# Import dependencies
import json

# Import local dependencies
from ..services.youtube import YoutubeServiceHandler
from ..util import logTime

class ClientRouter(object):
    def __init__(self):
        self.YoutubeServiceHandler = YoutubeServiceHandler()

    def route(self, data):
        try:
            if data["service"] == "youtube":
                if data["operation"] == "search":
                    output = self.YoutubeServiceHandler.search(data["payload"]["query"], data["payload"]["amount"])
                    return {"success": True, "response": output}
                elif data["operation"] == "get":
                    output = self.YoutubeServiceHandler.get(data["payload"]["url"])
                    return {"success": True, "response": output}
        except Exception as e:
            print(logTime() + f"An error occured while processing request: {type(e).__name__} - {e} ({e.__traceback__.tb_next.tb_frame.f_code.co_filename}@{e.__traceback__.tb_next.tb_frame.f_lineno})")
            return {"success": False, "error": "An error occured while handling this request."}

