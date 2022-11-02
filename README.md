# FlexMusic
FlexMusic is a lightweight alternative for other music backends used for Discord bot development. While still following a client-server model, FlexMusic takes a different approach by leaving the handling of audio streams themselves to the client, rather than handling audio streams within the server and passing them along to the client. The server instead opts to handle the data collection and API interactions necessary for music processing, and passes the data along to the client. This allows for a significant performance uplift and much higher stability than other backend options.

Furthermore, the FlexMusic client integrates seemlessly alongside [pycord](https://github.com/Pycord-Development/pycord)'s Client/Bot event loop, allowing for easy and performant deployment. The example code below demonstrates this integration.

```python
import discord
from discord.ext import commands
from fmc import FlexMusic # Import FlexMusic client library

client = commands.Bot() # Initialize Discord client
fmclient = FlexMusic.FMClient(client) # Initialize FMClient

@client.event
async def on_ready():
  await fmclient.connect() # Connect FMClient to FlexMusic server once Discord client event loop starts
  
@client.slash_command()
@discord.guild_only()
async def play(ctx, *, query):
    await ctx.defer()
    results = await FMClient.search(query, amount=1) # Send a search request to the FlexMusic server
    voice = await ctx.author.voice.channel.connect() 
    voice.play(results[0].src) # Play the audio stream data returned from the FlexMusic server
  
client.run(token) # Run Discord client event loop
```

At the moment, the FlexMusic client and server are both in extremely early stages of development. For the time being, it is not recommended FlexMusic be deployed in a production setting. Some current goals towards preparing FlexMusic for production are:
- Expanding the FlexMusic client to more Discord API libraries
- Proper stability/endurance testing
- More services (Vimeo, SoundCloud, Spotify, etc.)
- More contributors / maintainers (hit me up :D)

# Documentation

## Event Reference
The FlexMusic client's binding to the Discord client allows for monitoring of active voice clients. FlexMusic takes advantage of this by creating custom events relating to player and track status that can be handled as regular Discord events. These events can be found below.

### player_join
```python
@client.event
async def on_player_join(voice_client: discord.VoiceClient):
```
Called when the player officially connects to the voice channel and the player is finished being internally cached. Returns the voice client object of the player that raised the event.

### player_leave
```python
@client.event
async def on_player_leave(channel_id: int):
```
Called when Discord reports that the voice client of the player has disconnected and the player is finished being cleaned up from the internal cache. Returns the integer ID of the channel the player left from.
