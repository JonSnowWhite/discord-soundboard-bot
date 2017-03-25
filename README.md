# discord-soundboard-bot
A soundboard bot for Discord written in Python.

# Installation for Windows:
Check https://github.com/Rapptz/discord.py and http://discordpy.readthedocs.io/en/latest/api.html for general usage of the Discord Python API and questions(be sure to install discord.py[voice]).
You have to have to have the libopus-0.x64.dll or libopus-0.x86.dll file installed based upon your 32/64bit python interpreter. You also need ffmpeg on your computer and IN YOUR PATH VARIABLES. Just in case: (http://www.wikihow.com/Install-FFmpeg-on-Windows). Be sure to give the dll filename when loading the library as you are using Windows.

# Installation for Linux:
Check https://github.com/Rapptz/discord.py and http://discordpy.readthedocs.io/en/latest/api.html for general usage of the Discord Python API and questions(be sure to install discord.py[voice]).
Check if you have libopus on your computer (ldconfig -p | grep libopus/libopus0). This is installable via your favorite package manager. You also need ffmpeg here. On some distros you can install it via your favorite package manager, on raspberry you can't so you might need to compile it yourself (http://www.jeffreythompson.org/blog/2014/11/13/installing-ffmpeg-for-raspberry-pi/). Older raspberries can't handle the audio encoding anyways. Be sure to give the libopus filename when loading the library as you are using Linux.

# For Python 3.4.2 (unimportant if you use 3.5+)
http://discordpy.readthedocs.io/en/latest/migrating.html
Short version:
Replace ``async`` in ``async def`` with the decorator ``@asyncio.coroutine``. Replace ``await`` with ``yield from``. (Note: you can't return ``yield from``, so make an extra line where you return ``None``). In function ``disconnector()`` replace ``asyncio.run_coroutine_threadsafe`` with ``discord.compat.run_coroutine_threadsafe``.
