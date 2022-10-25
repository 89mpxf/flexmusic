# Import dependencies
from youtube_dl import YoutubeDL
import time

# Import local dependencies
from ..util import logTime

class YoutubeServiceHandler(object):
    def __init__(self):
        self.YDL_OPTIONS = {
            'search': {
                'format': 'bestaudio',
                'noplaylist': True,
                'quiet': True,
                'youtube_include_dash_manifest': False
            }
        }

    def search(self, query, amount: int = 10):
        search_results = []
        with YoutubeDL(self.YDL_OPTIONS["search"]) as api:
            print(logTime() + f"Executing YouTube search with query '{query}'...")
            st = time.time()
            raw_data = api.extract_info(f"ytsearch{amount}:{query}", download=False)["entries"]
            et = time.time()
            print(logTime() + f"YouTube query finished with {len(raw_data)} results ({str(round(et - st, 2))}s)")
            for i in range(len(raw_data)):
                data = {}
                data["id"] = raw_data[i]["id"]
                data["title"] = raw_data[i]["title"]
                data["artist"] = raw_data[i]["uploader"]
                data["duration"] = raw_data[i]["duration"]
                data["cover"] = raw_data[i]["thumbnail"]
                data["source"] = raw_data[i]["formats"][0]["url"]

                search_results.append(data)
                
        return search_results
