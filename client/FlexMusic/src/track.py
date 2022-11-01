# Import dependencies
from discord import FFmpegPCMAudio

# FFMPEG options
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}

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