# Import dependencies
import discord

# Import local dependencies
from .track import Track
from ..util._queue import Queue

class FMPlayer(discord.VoiceClient):
    def __init__(self, voice_client: discord.VoiceClient):
        self.__class__ = type(voice_client.__class__.__name__, (self.__class__, voice_client.__class__), {})
        self.__dict__ = voice_client.__dict__
        self._voice_client = voice_client
        self.queue = Queue()
