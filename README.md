# discord-soundboard-bot
A soundboard bot for Discord written in Python with the discord.py[rewrite] library.

# Installation for Windows:
Check https://github.com/Rapptz/discord.py/tree/rewrite and https://discordpy.readthedocs.io/en/rewrite/ for general usage of the Discord Python API and questions(be sure to install discord.py[voice]).
You have to have the libopus-0.x64.dll or libopus-0.x86.dll file installed based upon your 32/64bit python interpreter. You also need ffmpeg on your computer and IN YOUR PATH VARIABLES. Just in case: (http://www.wikihow.com/Install-FFmpeg-on-Windows). Be sure to give the dll filename when loading the library as you are using Windows.

# Installation for Linux:
Check https://github.com/Rapptz/discord.py/tree/rewrite and https://discordpy.readthedocs.io/en/rewrite/ for general usage of the Discord Python API and questions(be sure to install discord.py[voice]).
Check if you have libopus on your computer (ldconfig -p | grep libopus/libopus0). This is installable via your favorite package manager. You also need ffmpeg here. On some distros you can install it via your favorite package manager, on raspberry you can't so you might need to compile it yourself (http://www.jeffreythompson.org/blog/2014/11/13/installing-ffmpeg-for-raspberry-pi/). Older raspberries can't handle the audio encoding, but newer can(I can vouch for that). Be sure to give the libopus filename when loading the library as you are using Linux.

# For Python 3.4.2: (unimportant if you use 3.5+)
http://discordpy.readthedocs.io/en/latest/migrating.html
Short version:
Replace ``async`` in ``async def`` with the decorator ``@asyncio.coroutine``. Replace ``await`` with ``yield from``. (Note: you can't return ``yield from``, so make an extra line where you return ``None``). In function ``disconnector()`` replace ``asyncio.run_coroutine_threadsafe`` with ``discord.compat.run_coroutine_threadsafe``.

# What is rewrite:
http://discordpy.readthedocs.io/en/rewrite/migrating.html
Short version:
Servers are guilds now // snowflakes are int // Models are Stateful, meaning much functionality went from discord.Client to the other Classes // Changes to the VoiceState of Members // many more misellaneous changes 
