# Import dependencies
import asyncio, json, time

# Import local dependencies
from .exception import Exception
from .track import Track
from ._clientrequestscheduler import _ClientRequestScheduler

class FMClient(object):
    '''
    FlexMusic Client (FMClient) object.\n
    By default, this client attempts to connect to localhost:5000. If the FlexMusic server you are using exists on a different port or machine, supply the "host" or "port" arguments.\n
    The only required argument is a Discord bot object. This is so the even
    '''

    def __init__(self, client, debug: bool = False, host: str = "localhost", port: int = 5000):
        self.client = client
        self.read, self.write = None, None
        self.host, self.port = host, port
        self.scheduler = _ClientRequestScheduler()
        self.debug = debug
        if self.debug:
            print("FlexMusic Client successfully initialized")
            print("Debug mode is currently active.")

    # Internal event monitoring task
    async def _listen_for_events(self):
        _internal_session_cache = {}
        while True:
            _active_clients = []
            for voice_client in self.client.voice_clients:
                _active_clients.append(str(voice_client.channel.id))
                if str(voice_client.channel.id) not in _internal_session_cache:
                    self.client.dispatch("player_join", voice_client)
                    if self.debug:
                        print(f"Dispatched player_join event ({str(voice_client.channel.id)})")
                    _internal_session_cache[f"{voice_client.channel.id}"] = {}
                    _internal_session_cache[f"{voice_client.channel.id}"]["playing"] = voice_client.is_playing()
                    _internal_session_cache[f"{voice_client.channel.id}"]["paused"] = voice_client.is_paused()
                    continue

                if voice_client.is_playing() is not _internal_session_cache[f"{voice_client.channel.id}"]["playing"]:
                    if voice_client.is_playing() is False:
                        self.client.dispatch("track_end", voice_client)
                        if self.debug:
                            print(f"Dispatched track_end event ({str(voice_client.channel.id)})")
                    else:
                        self.client.dispatch("track_start", voice_client)
                        if self.debug:
                            print(f"Dispatched track_start event ({str(voice_client.channel.id)})")
                    _internal_session_cache[f"{voice_client.channel.id}"]["playing"] = voice_client.is_playing()

                if voice_client.is_paused() is not _internal_session_cache[f"{voice_client.channel.id}"]["paused"]:
                    if voice_client.is_paused() is False:
                        self.client.dispatch("track_pause", voice_client)
                        if self.debug:
                            print(f"Dispatched track_pause event ({str(voice_client.channel.id)})")
                    else:
                        self.client.dispatch("track_resume", voice_client)
                        if self.debug:
                            print(f"Dispatched track_resume event ({str(voice_client.channel.id)})")
                    _internal_session_cache[f"{voice_client.channel.id}"]["paused"] = voice_client.is_playing()
            
            _temp = {}
            for client in _internal_session_cache.keys():
                if client in _active_clients:
                    _temp[f"{client}"] = _internal_session_cache[f"{client}"]
                else:
                    self.client.dispatch("player_leave", int(client))
                    if self.debug:
                        print(f"Dispatched player_leave event ({client})")
            _internal_session_cache = _temp
            await asyncio.sleep(0.01)
    
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
        asyncio.create_task(self._listen_for_events())
        print("Started background event dispatcher")

    async def search(self, query: str = None, service: str = "youtube", amount: int = 10):
        '''
        Main track search function.\n
        By default, this will search YouTube.\n
        This function returns a list of Track objects found with the given query, up to the maximum amount defined.
        '''
        if query is None:
            raise Exception.MissingQuery

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
                    output.append(Track(resp["response"][i]["source"], resp["response"][i]["id"], resp["response"][i]["title"], resp["response"][i]["artist"], resp["response"][i]["duration"], resp["response"][i]["cover"]))
                return output
            else:
                raise Exception.NoResultsFound
        else:
            raise Exception.ServerRaisedError

    async def get(self, url: str = None, service: str = "youtube"):
        '''
        Main direct URL handling function.\n
        By default, this treats all URLs as YouTube URLs. URLs for a different service or file path will require providing a service manually.\n
        The search function will redirect to this function in the event you pass a URL as the query. It is recommended you call this function directly for all URLs instead of relying on the redirection.\n
        This function will return a single Track object, however, will return a list of tracks if a playlist URL was passed.
        '''
        if not url:
            raise Exception.MissingURL

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
                    output.append(Track(resp["response"][i]["source"], resp["response"][i]["id"], resp["response"][i]["title"], resp["response"][i]["artist"], resp["response"][i]["duration"], resp["response"][i]["cover"]))
                return output
            else:
                raise Exception.NoResultsFound
        else:
            raise Exception.ServerRaisedError