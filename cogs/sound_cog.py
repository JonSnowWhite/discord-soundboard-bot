from discord.ext import commands
import discord
from ext_module import ExtModule
import os
import asyncio
from random import randint
from discord import opus


class SoundboardCog:
    """Cog for the soundboard feature"""

    # see play command changes

    def __init__(self, bot: commands.Bot, folder=None, log_channel_id: int=None, tag_dict: dict={}):
        """The constructor for the SoundboardCog class, it assigns the important variables used by the commands below
        Args:
            bot: The bot the Cog will be added to (commands.Bot)
            folder: The path to the folder with the sound files (str)
            log_channel_id: The id of the log_channel (int)
            """
        self.folder = folder
        self.bot = bot
        self.log_channel_id = log_channel_id
        self.send_log = None             # will be assigned later
        self.sound_list = SoundboardCog._load_songs(self.folder)
        self.tag_dict = tag_dict
        self.tag_dict = dict((k.lower(), v) for k, v in self.tag_dict.items())  # lower all keys
        for value in self.tag_dict:     # lower all values
            self.tag_dict[value] = [name.lower() for name in self.tag_dict[value]]
        for tag in self.tag_dict.keys():  # removing invalid filenames
            self.tag_dict[tag] = [name for name in self.tag_dict[tag] if name in self.sound_list]

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
        self.send_log = ExtModule.get_send_log(self)
        opus.load_opus('libopus.so.0')  # the opus library

    @commands.command(name='play',
                      description='name(optional) || Plays the sound with the given name. Ignores upper/lowercase.'
                                  ' If none is found or none is given the sound is chosen randomly.'
                                  ' Requires you to be in a voice channel!')
    @ExtModule.reaction_respond
    async def play(self, ctx: commands.Context, *args):
        """This command plays the first sound name found in args, if one exists.
        If none exists, all args will be interpreted as tags. The command will create the cut, of all
        valid tag parameters and play a random file from that.
        If that list is empty/no args is formatted validly this command plays a random sound

        Args:
            ctx: The context of the command, which is mandatory in rewrite (commands.Context)
            args: Shall contain at least one filnename or multiple tags (all String)
            """
        try:  # user must be connected to a voice channel
            voice_channel = ctx.author.voice.channel
        except AttributeError:
            await ctx.send(content='To use this command you have to be connected to a voice channel!')
            raise discord.DiscordException

        _name_cut = self.sound_list

        for arg in args:  # check if one is a name
            if arg.lower() in self.sound_list:
                _name_cut = [arg.lower()]
                break
        if len(_name_cut) > 1:
            for arg in args:  # if no name is found go through the tags
                if arg.lower() in self.tag_dict.keys():
                    _name_cut = [name for name in _name_cut if name in self.tag_dict[arg.lower()]]  # update the cut
        if len(_name_cut) == 0:  # play a random sound if the tags have no cut
            _name_cut = self.sound_list
            try:
                await ctx.send(content='No name with all the tags given. Playing a random sound.')
            except discord.DiscordException:
                pass
        name = _name_cut[randint(1, len(_name_cut)) - 1]
        try:
            vc = await voice_channel.connect()
        except discord.ClientException:
            await ctx.send('I am already playing in a voice channel.'
                           ' Please try again later or stop me with the stop command!')
            raise discord.DiscordException
        vc.play(discord.FFmpegPCMAudio(self.folder + '/' + name + '.mp3'),
                after=lambda e: SoundboardCog.disconnector(vc, self.bot))
        await self.send_log('Playing: ' + name)

    @commands.command(name='stop',
                      aliases=['halt'],
                      description='The bot will stop playing a sound and leave the current voice channel.'
                                  'Requires you to be in the same voice channel as the bot!')
    @ExtModule.reaction_respond
    async def stop(self, ctx: commands.Context):
        """This function stops the bot playing a sound and makes it leave the current voice channel.
         Args:
             ctx: The context of the command, which is mandatory in rewrite (commands.Context)
             """
        for connection in self.bot.voice_clients:
            if ctx.author.voice.channel == connection.channel:
                return await connection.disconnect()

    @commands.command(name='soundlist',
                      aliases=['sounds'], description='Prints a list of all sounds on the soundboard.')
    @ExtModule.reaction_respond
    async def soundlist(self, ctx: commands.Context):
        """This function prints a list of all the sounds on the Soundboard to the channel/user where it was requested.
        Args:
            ctx: The context of the command, which is mandatory in rewrite (commands.Context)
            """
        _sound_string = 'List of all sounds (command format !play [soundname]):'
        for sound in self.sound_list:
            if len(_sound_string) + 1 + len(sound) > 1800:
                await ctx.channel.send(_sound_string)
            _sound_string = _sound_string + '\n' + sound
        await ctx.channel.send(_sound_string)

    @commands.command(name='taglist',
                      aliases=['tags'], description='Prints a list of all tags with soundnames on the soundboard.')
    @ExtModule.reaction_respond
    async def taglist(self, ctx: commands.Context):
        """This function prints a list of all the tags with their sounds on the Soundboard to the
         channel/user where it was requested.
        Args:
            ctx: The context of the command, which is mandatory in rewrite (commands.Context)
            """
        _tag_string = 'tag || sounds\n'
        for tag in self.tag_dict.keys():
            if len(_tag_string) > 1800:
                await ctx.channel.send(_tag_string)
                _tag_string = ''
            _tag_string = _tag_string + tag + ' || '
            for sound in self.tag_dict[tag]:
                _tag_string = _tag_string + sound + ' '
            _tag_string = _tag_string + '\n'
        await ctx.channel.send(_tag_string)

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
