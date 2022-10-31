# Import dependencies
import time
import yt_dlp
import multiprocessing as mp
from youtube_dl import YoutubeDL

# Import local dependencies
from ..util import logTime

class YoutubeServiceHandler(object):
    def __init__(self):
        self.source_retrieval_options = {
            'format': 'bestaudio',
            'quiet': True,
            'skip_download': True,
            'forceurl': True,
            'simulate': True,
            'youtube_include_dash_manifest': False
        }
        self.search_options = {
            'quiet': True,
            'simulate': True,
            'skip_download': True,
            'noplaylist': True,
            'extract_flat': True
        }

    def _process_audio_stream(self, data: dict):
        with YoutubeDL(self.source_retrieval_options) as api:
            data['source'] = api.extract_info(f"https://youtube.com/watch?v={data['id']}", download=False)["formats"][0]["url"]
        return data

    def get_audio_streams(self, sources: list):
        print(logTime() + f"Fetching audio streams for {len(sources)} sources...")
        st = time.time()
        pool = mp.Pool(processes=len(sources))
        processed_sources = pool.map(self._process_audio_stream, sources)
        et = time.time()
        print(logTime() + f"Successfully fetched audio streams for {len(sources)} sources ({str(round(et - st, 2))}s)")
        return processed_sources

    def search(self, query: str, amount: int = 10):
        search_results = []
        with yt_dlp.YoutubeDL(self.search_options) as api:
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
                try:
                    data["cover"] = raw_data[i]["thumbnail"]
                except KeyError:
                    data["cover"] = raw_data[i]["thumbnails"][0]["url"]
                search_results.append(data)
        search_results = self.get_audio_streams(search_results)
        return search_results

    def get(self, url: str):
        results = []
        with yt_dlp.YoutubeDL(self.search_options) as api:
            print(logTime() + f"Getting YouTube data from '{url}'...")
            st = time.time()
            raw_data = api.extract_info(url, download=False)
            et = time.time()
            print(logTime() + f"YouTube data fetch for '{url}' completed ({str(round(et - st, 2))}s)")
            if not "entries" in raw_data:
                data = {}
                data["id"] = raw_data["id"]
                data["title"] = raw_data["title"]
                data["artist"] = raw_data["uploader"]
                data["duration"] = raw_data["duration"]
                try:
                    data["cover"] = raw_data["thumbnail"]
                except KeyError:
                    data["cover"] = raw_data["thumbnails"][0]["url"]
                results.append(data)
            else:
                for i in range(len(raw_data["entries"])):
                    data = {}
                    data["id"] = raw_data["entries"][i]["id"]
                    data["title"] = raw_data["entries"][i]["title"]
                    data["artist"] = raw_data["entries"][i]["uploader"]
                    data["duration"] = raw_data["entries"][i]["duration"]
                    try:
                        data["cover"] = raw_data["entries"][i]["thumbnail"]
                    except KeyError:
                        data["cover"] = raw_data["entries"][i]["thumbnails"][0]["url"]
                    results.append(data)
            results = self.get_audio_streams(results)
            return results