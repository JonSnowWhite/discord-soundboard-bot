from discord.ext import commands
import discord
import os
import asyncio
from random import randint


class SoundboardCog:
    """Cog for the soundboard feature"""

    bot = None

    def __init__(self, bot: commands.Bot, folder=None, log_channel_id: int=None):
        """The constructor for the SoundboardCog class, it assigns the important variables used by the commands below
        Args:
            bot: The bot the Cog will be added to (commands.Bot)
            folder: The path to the folder with the sound files (str)
            log_channel_id: The id of the log_channel (int)
            """
        self.folder = folder
        self.bot = bot
        self.log_channel_id = log_channel_id
        self.log_channel = None             # will be assigned later
        self.sound_list = SoundboardCog._load_songs(self.folder)

    @staticmethod
    def _load_songs(folder):
        """This function returns a list with all the mp3-file names in the given folder
        Args:
            folder: The folder with the mp3 files (String)
        Returns:
            sound_list: The list with file names, all lowercase and without the .mp3 (list)
        This function raises an Exception, if the folder was empty
            """
        sound_list = sorted([i[:-4].lower() for i in os.listdir(folder) if '.mp3' in i])
        if not sound_list:
            raise Exception("No mp3 files in the given folder")
        return sound_list

    async def on_ready(self):
        self.log_channel = self.bot.get_channel(self.log_channel_id)

    @commands.command(description='name(optional) || Plays the sound with the given name. Ignores upper/lowercase.'
                                  ' If none is found or none is given the sound is chosen randomly.'
                                  ' Requires you to be in a voice channel!')
    async def play(self, ctx: commands.Context, name=''):
        """This command plays the sound with the given name (random if no name given or name is write falsely)

        Args:
            ctx: The context of the command, which is mandatory in rewrite (commands.Context)
            name: The name of the sound file to be played, empty by default (String)
            """
        try:
            voice_channel = ctx.author.voice.channel
        except AttributeError:
            return await ctx.send(content='To use this command you have to be connected to a voice channel!')
        if name != '' and name.lower() not in self.sound_list:
            await ctx.send('This files does\'t exist. Check the help command for more info!')
            name = self.sound_list[randint(1, len(self.sound_list)) - 1]
        elif name == '':
            name = self.sound_list[randint(1, len(self.sound_list)) - 1]
        try:
            vc = await voice_channel.connect()
        except discord.ClientException:
            return await ctx.send('I am already playing in a voice channel.'
                                  ' Please try again later or stop me with the stop command!')
        vc.play(discord.FFmpegPCMAudio(self.folder + '/' + name.lower() + '.mp3'),
                after=lambda e: SoundboardCog.disconnector(vc, self.bot))
        try:
            await self.log_channel.send('Playing: ' + name)
        except AttributeError:
            pass

    @commands.command(aliases=['halt'],
                      description='The bot will stop playing a sound and leave the current voice channel.'
                                  'Requires you to be in the same voice channel as the bot!')
    async def stop(self, ctx: commands.Context):
        """This function stops the bot playing a sound and makes it leave the current voice channel.
         Args:
             ctx: The context of the command, which is mandatory in rewrite (commands.Context)
             """
        for connection in self.bot.voice_clients:
            if ctx.author.voice.channel == connection.channel:
                return await connection.disconnect()

    @commands.command(aliases=['sounds'], description='Prints a list of all sounds on the soundboard.')
    async def soundlist(self, ctx: commands.Context):
        """This function prints a list of all the sounds on the Soundboard to the channel/user where it was requested.
        Args:
            ctx: The context of the command, which is mandatory in rewrite (commands.Context)
            """
        _sound_string = 'List of all sounds:'
        for sound in self.sound_list:
            if len(_sound_string) + 1 + len(sound) > 1800:
                await ctx.channel.send(_sound_string)
                _sound_string = ''
            else:
                _sound_string = _sound_string + '\n' + sound
        return await ctx.channel.send(_sound_string)

    @staticmethod
    def disconnector(voice_client: discord.VoiceClient, bot: commands.Bot):
        """This function is passed as the after parameter of FFmpegPCMAudio() as it does not take coroutines.
        Args:
            voice_client: The voice client that will be disconnected (discord.VoiceClient)
            bot: The bot that will terminate the voice client, which will be this very bot
            """
        coro = voice_client.disconnect()
        fut = asyncio.run_coroutine_threadsafe(coro, bot.loop)
        try:
            fut.result()
        except asyncio.CancelledError:
            pass
