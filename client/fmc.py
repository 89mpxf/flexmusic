#
# FlexMusic Client Library
# Designed for integration with pycord/discord.py Discord API applications
# 
# This library is open source and intended for use with FlexMusic servers
# FlexMusic is an open source music retrieval server that works as a backend for Discord app development
# More information about FlexMusic can be found at https://github.com/89mpxf/flexmusic
# 
# FlexMusic, created by mpxf (https://github.com/89mpxf)
#

# Import dependencies
import asyncio
from discord import FFmpegPCMAudio, PCMVolumeTransformer
from time import sleep
import json

# FFMPEG options
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}

# Main library class
class FlexMusic(object):
    '''
    FlexMusic Client Library\n1
    Open source library designed to interface the FlexMusic server with pycord/discord.py bot clients.\n
    Development started and maintained by https://github.com/89mpxf.
    '''

    # Exceptions
    class Exception(object):
        '''
        FlexMusic Client exception parent class\n
        All client exceptions/errors exist within this class
        '''

        #
        # Base exception declarations
        #

        # Base client exception
        class ClientException(Exception):
            '''
            Base exception for all FlexMusic errors propagated during client-side request operation\n
            This should not be raised directly.
            '''
            pass

        # Base server exception
        class ServerException(Exception):
            '''
            Base exception for all FlexMusic errors propagated during server-side request operation\n
            This should not be raised directly.
            '''
            pass

        # Base user exception
        class UserException(Exception):
            '''
            Base exception for all FlexMusic errors propagated as a result of user error\n
            This should not be raised directly.
            '''
            pass

        #
        # Client exception declarations
        #

        class NoResultsFound(ClientException):
            '''Raised when a search request returns no results'''
            pass

        #
        # Server exception declarations
        #

        class ServerRaisedError(ServerException):
            '''Raised when a server request fails on the server's end.'''
            pass

        #
        # User eception declaration
        #

        class MissingQuery(UserException):
            '''Raised when a function that requires a query does not receive one'''
            pass

        class MissingURL(UserException):
            '''Raised when a function that requires a URL does not receive one'''
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
        def src(self):
            '''Returns the PCM audio stream of the track to be played by the client.'''
            return FFmpegPCMAudio(self.source, **FFMPEG_OPTIONS)

    # Main client import
    class FMClient(object):
        '''
        FlexMusic Client (FMClient) object.\n
        By default, this client attempts to connect to localhost:5000. If the FlexMusic server you are using exists on a different port or machine, supply the "host" or "port" arguments.\n
        The only required argument is a Discord bot object. This is so the even
        '''

        def __init__(self, debug: bool = False, host: str = "localhost", port: int = 5000):
            self.read, self.write = None, None
            self.host, self.port = host, port
            self.scheduler = FlexMusic._ClientRequestScheduler()
            self.debug = debug
            if self.debug:
                print("FlexMusic Client successfully initialized")
                print("Debug mode is currently active.")
        
        # Client connection coroutine, call after event loop starts
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
                        if self.debug:
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
            if query is None:
                raise FlexMusic.Exception.MissingQuery

            if query.startswith("https://") or query.startswith("http://"):
                return await self.get(query, service=service)

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
                if self.debug:
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
            else:
                raise FlexMusic.Exception.ServerRaisedError

        async def get(self, url: str = None, service: str = "youtube"):
            '''
            Main direct URL handling function.\n
            By default, this treats all URLs as YouTube URLs. URLs for a different service or file path will require providing a service manually.\n
            The search function will redirect to this function in the event you pass a URL as the query. It is recommended you call this function directly for all URLs instead of relying on the redirection.\n
            This function will return a single Track object, however, will return a list of tracks if a playlist URL was passed.
            '''
            if not url:
                raise FlexMusic.Exception.MissingURL

            payload = {
                "service": service,
                "operation": "get",
                "payload": {
                    "url": url,
                }
            }

            id = self.scheduler.queue_job()
            if self.debug:
                print(f"Queued client request (Job ID: {str(id)})")

            while not self.scheduler.ready(id):
                if self.debug:
                    print(f"Client is busy. Waiting to start job... (Job ID: {str(id)})")
                await asyncio.sleep(1)

            self.write.write(json.dumps(payload).encode())

            if self.debug:
                print(f"Sent get request to server ({service}, {url})...")

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
            else:
                raise FlexMusic.Exception.ServerRaisedError