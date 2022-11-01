'''
FlexMusic Client Library\n
Designed for integration with pycord/discord.py Discord API applications\n
\n
This library is open source and intended for use with FlexMusic servers. FlexMusic is an open source music retrieval server that works as a backend for Discord app development. More information about FlexMusic can be found at https://github.com/89mpxf/flexmusic\n
\n
FlexMusic, created by mpxf (https://github.com/89mpxf)
'''

from .src.exception import Exception
from .src.fmclient import FMClient
from .src.track import Track