# Import dependencies
import asyncio
from discord import FFmpegPCMAudio, PCMVolumeTransformer
from time import sleep
import json

# FFMPEG options
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}

class FlexMusic(object):
    '''
    FlexMusic Client Library\n
    Open source library designed to interface the FlexMusic server with pycord/discord.py bot clients.\n
    Development started and maintained by https://github.com/89mpxf.
    '''
    # Exceptions
    class Exception(object):
        class BaseException(Exception):
            '''Base exception for all FlexMusic client errors'''
            pass

        class NoResultsFound(BaseException):
            '''Raised when a search request returns no results'''
            pass

    # Client request scheduler
    class _ClientRequestScheduler(object):
        '''
        Request scheduler for FlexMusic client.\n
        For internal use only
        '''

        def __init__(self):
            self._job_queue = []
            self._finished_jobs = 0

        @property
        def latest_job_id(self):
            return len(self._job_queue)

        def queue_job(self):
            self._job_queue.append(job_id := int(len(self._job_queue)))
            return job_id

        def finish_job(self):
            self._finished_jobs += 1

        def ready(self, id):
            if id == self._finished_jobs:
                return True
            else:
                False

    # Track object constructor
    class Track(object):
        '''FlexMusic Track object; contains metadata attributes and audio stream for a given track.'''

        def __init__(self, source: str, id: str = None, title: str = None, artist: str = None, duration: int = None, cover: str = None):
            self.title = title
            self.artist = artist
            self.duration = duration
            self.cover = cover
            self.id = id
            self.source = source

        def __repr__(self):
            return f"<FlexMusic.Track title={self.title} artist={self.artist} duration={str(self.duration)} id={self.id}>"

        @property
        def stream(self):
            '''Returns the PCM audio stream of the track to be played by the client.'''
            return FFmpegPCMAudio(self.source, **FFMPEG_OPTIONS)

    # Main client import
    class FMClient(object):
        def __init__(self, client, debug: bool = False, host: str = "localhost", port: int = 5000):
            self.event_loop = client.loop
            self.read, self.write = None, None
            self.host, self.port = host, port
            self.scheduler = FlexMusic._ClientRequestScheduler()
            self.debug = debug
            print("FlexMusic Client successfully initialized")
            print("Debug mode is currently active.")
            
        async def connect(self):
            '''
            Main coroutine to start the FlexMusic client and bind the connection to the event loop.\n
            This coroutine should be called after the Discord client's event loop has started (i.e. on the "on_ready" event)\n
            '''
            if self.debug:
                print(f"Connecting to {self.host}:{self.port}...")
            while (self.read, self.write) == (None, None):
                try:
                    self.read, self.write = await asyncio.open_connection(self.host, self.port)
                    if self.read is not None and self.write is not None:
                        print(f"Connected to FlexMusic server at {self.host}:{str(self.port)} successfully.")
                except:
                    if self.debug:
                        print(f"Failed to connect to {self.host}:{self.port}, retrying in 5 seconds...")
                    await asyncio.sleep(5)

        async def search(self, query: str = None, service: str = "youtube", amount: int = 10):
            '''
            Main track search function.\n
            By default, this will search YouTube.\n
            This function returns a list of Track objects found with the given query, up to the maximum amount defined.
            '''
            if query is None or amount is None:
                return

            payload = {
                "service": service,
                "operation": "search",
                "payload": {
                    "query": query,
                    "amount": amount
                }
            }

            id = self.scheduler.queue_job()
            if self.debug:
                print(f"Queued client request (Job ID: {str(id)})")

            while not self.scheduler.ready(id):
                print(f"Client is busy. Waiting to start job... (Job ID: {str(id)})")
                await asyncio.sleep(1)

            self.write.write(json.dumps(payload).encode())

            if self.debug:
                print(f"Sent search request to server ({service}, {query}, {amount})...")

            data = await self.read.read(65536)
            if self.debug:
                print(f"Received response from server")
            
            self.scheduler.finish_job()
            if self.debug:
                print(f"Finished client request (Job ID: {str(id)})")

            resp = json.loads(data.decode())
            output = []
            if resp["success"] is True:
                if len(resp["response"]) > 0:
                    for i in range(len(resp["response"])):
                        output.append(FlexMusic.Track(resp["response"][i]["source"], resp["response"][i]["id"], resp["response"][i]["title"], resp["response"][i]["artist"], resp["response"][i]["duration"], resp["response"][i]["cover"]))
                    return output
                else:
                    raise FlexMusic.Exception.NoResultsFound


