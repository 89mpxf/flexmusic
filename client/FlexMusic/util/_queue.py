# Import local dependencies
from ..src.track import Track

class Queue(object):
    '''
    FlexMusic Client Queue Handler Utility\n
    This object is a singular queue. It can be assigned to a player and used to add a queue system to music.
    '''

    def __init__(self):
        self._queue = []
        self._pos = 0

    #
    # Class method definition
    #

    def add(self, *args: Track | list[Track]):
        '''Adds the provided Track object(s) to the queue'''
        self._queue.extend(*args)

    def empty(self):
        '''Empty the queue and reset the position'''
        self._queue.clear()
        self._pos = 0

    #
    # Property definitions
    #

    @property
    def is_empty(self) -> bool:
        '''Returns True if queue is empty. Returns False if queue is not empty'''
        return not self._queue

    @property
    def upcoming(self) -> None | list[Track]:
        '''Returns all tracks in the queue starting at the track directly after the currently playing track. If there are no tracks in the queue after this position, or at all, this will return None'''
        if not self._queue:
            return None
        return self._queue[self._pos + 1:]

    @property
    def current_track(self) -> None | Track:
        '''Returns the current track. If nothing is playing or the queue is empty, this will return None'''
        if not self._queue:
            return None
        if self._pos <= len(self._queue) - 1:
            return self._queue[self._pos]

    @property
    def length(self) -> int:
        '''Returns the integer length of the entire queue'''
        return len(self._queue)

    @property
    def history(self) -> None | list[Track]:
        '''Returns all tracks in the queue that have already been played. If the queue is empty or nothing has been played yet, this will return None'''
        if not self._queue:
            return None
        return self._queue[:self._pos]

    @property
    def next(self) -> None | Track:
        '''Returns the next track in the queue and advances the queue position. If the queue is empty or there is no song after, this will not advance the queue position and return None'''
        if not self._queue:
            return None
        self._pos += 1
        if self._pos < 0 or self._pos > len(self._queue) - 1:
            return None
        return self._queue[self._pos]