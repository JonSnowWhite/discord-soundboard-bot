"""
Copyright (c) <2017> <JonSnowWhite>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import os
from random import randint
import discord
import asyncio
from discord.ext import commands
from discord import game
from discord import opus


#----------------------Instanciations--------------

board_list = [i[:-4] for i in os.listdir() if '.mp3' in i] #creating a list of all the .mp3 files in the current folder
board_string = ''
for i in board_list:
    board_string = board_string + '\n' + i

if len(board_list) == 0:
    print('I will not run without at least one mp3 file in the given directory! Type to close me!')
    _tmp = input()
    raise Exception

bot = commands.Bot(command_prefix='!')

help_dict = {
                'play' : 'Type ' + bot.command_prefix + 'play + name \n List of names:' + board_string
                }

#---------------------Events-----------------------

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    opus.load_opus('libopus-0.x64.dll/libopus.so.0') #the opus library

#----------voice-Command and functions------------

def disconnector(bot, server):
    """This function solely exists to be passed to the attribute `later` when instanciating a new stream_player.
    This is used instead of the coroutine disconnect().

    Args:
        bot: the bot to disconnect (should always be the bot using the stream_player
        server: the server attached to the stream_player)
        """
    coro = bot.voice_client_in(server).disconnect()
    fut = asyncio.run_coroutine_threadsafe(coro, bot.loop)
    try:
        fut.result()
    except:
        pass


@bot.command(pass_context = True,  help = help_dict['play'], brief = 'Plays a sound. Use \'' + bot.command_prefix + 'help play\' for a list of names.', aliases = ['Sound', 'sound', 'Play'])
async def play(ctx, name = '', *args):
    """This is the command to start a sound. It has 4 basic steps: Connecting, setting up a player, playing, disconnecting

    Args:
        ctx: Context information about the command written by the user
        name: the name of the sound which should be played (wrong names are handled as an empty string)
    """
    server = ctx.message.server
    member = ctx.message.author
    channel = member.voice_channel

    #--------join the channel---------

    try:
        await bot.join_voice_channel(channel)
    except discord.InvalidArgument:
        return await bot.say('You\'re not in a voice channel!')
    except discord.ClientException:
        return await bot.say('I\'m busy, try again later!')

    if name != '' and not name in board_list:
        await bot.say('Not an available name. Type \'' + bot.command_prefix + 'help play\' for a list of names. Random sound incoming!')
        name = board_list[randint(1,len(board_list))-1]
    elif name == '':
        name = board_list[randint(1,len(board_list))-1]

    #-----set up the player

    try:
        player = bot.voice_client_in(server).create_ffmpeg_player(filename = name + '.mp3', after=lambda: disconnector(bot=bot, server=server))
    except:
        return await bot.say('I don\'t have this sound!/ffmpeg error!') #Should never occur as name is handled earlier
    #------play

    player.start()

#-----------------run the bot----------------------

bot.run('enter your token here')
