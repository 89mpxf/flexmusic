# Import dependencies
from discord import VoiceClient, AudioSource
from typing import Callable, Optional, Any

# Import local dependencies
from .track import Track
from ..util._queue import Queue

class FMPlayer(VoiceClient):
    def __init__(self, voice_client: VoiceClient):
        self.__class__ = type(voice_client.__class__.__name__, (self.__class__, voice_client.__class__), {})
        self.__dict__ = voice_client.__dict__
        self._voice_client = voice_client
        self.queue = Queue()

    def play(self, track: Track | AudioSource, *, after: Callable[[Optional[Exception]], Any] = None):
        """
        This is the play method for the FMPlayer class. It wraps the play method of the VoiceClient class, so it can still be used as normal.\n
        This method adds support for FlexMusic Track objects.
        """
        if isinstance(track, Track):
            if self.queue.is_empty:
                self.queue.add(track)
            if after is not None:
                return self._voice_client.play(track.src, after=after)
            return self._voice_client.play(track.src)
        else:
            if after is not None:
                return self._voice_client.play(track, after=after)
            return self._voice_client.play(track)