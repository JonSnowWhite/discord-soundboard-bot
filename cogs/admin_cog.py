from discord.ext import commands
import discord
from ext_module import ExtModule
from ext_module import PmForbidden


class AdminCog:
    """This cog contains commands that can be used by the bots admin(s).
    This will not contain commands, which ban and kick a user or let the bot behave as a server admin.
    """
    def __init__(self, bot: commands.Bot, log_channel_id: int=None):
        """The constructor for the AdminCog class, it assigns the important variables used by the commands below
        Args:
            bot: The bot the commands will be added to (commands.Bot)
            log_channel_id: The id of the log_channel (int)
            """
        self.bot = bot
        self.log_channel_id = log_channel_id
        self.send_log = None                  # will be assigned in the on_ready event

    async def on_ready(self):
        """Is called when the bot is completely started up. Calls in this function need variables only a started bot can give.
        """
        self.send_log = ExtModule.get_send_log(self)
        game = discord.Game(name='!help')
        await self.bot.change_presence(game=game)

    async def on_guild_join(self, guild: discord.Guild):
        """Is called when the bot joins a new guild. Sends an informative message to the log_channel
        Args:
            guild: The guild which the bot joined on (discord.Guild)
            """
        await self.send_log('Joined guild: ' + guild.name)

    async def on_guild_remove(self, guild: discord.Guild):
        """Is called when the bot leaves a guild. Sends an informative message to the log_channel
        Args:
            guild: The guild which was left by the bot (discord.Guild)
            """
        await self.send_log('Left guild: ' + guild.name)

    @commands.command(name='serverlist',
                      aliases=['list'],
                      description='Prints a list of all the servers'
                                  ' this bot is a member of to the admin log_channel')
    @ExtModule.is_admin()
    @ExtModule.reaction_respond
    async def serverlist(self, ctx: commands.Context):
        """This function sends a list with all the servers this bot is a member of to the self.log_channel
        Args:
            ctx: The context of the command, which is mandatory in rewrite
        """
        _guild_names = 'List of all guilds: '
        for guild in self.bot.guilds:
            if len(_guild_names) + len(guild.name) > 1800:  # not accurate, 200 literals buffer catch it
                await self.send_log(_guild_names)
                _guild_names = ''
            else:
                _guild_names = _guild_names + ', ' + guild.name + '(' + str(guild.id) + ')'
        await self.send_log(_guild_names)

    @commands.command(name='leave',
                      description='(ID) || The bot will attempt to leave the server with the given ID.')
    @ExtModule.is_admin()
    @ExtModule.reaction_respond
    async def leave(self, ctx: commands.Context, guild_id: int=None):
        """This commands makes the bot leave the server with the given ID
        Args:
            ctx: The context of the command, which is mandatory in rewrite (commands.Context)
            guild_id: The id of the server, which will be left (int)
            """
        guild = self.bot.get_guild(int(guild_id))
        try:
            await guild.leave()
        except discord.HTTPException:
            await self.send_log('Could not leave guild ' + guild.name)
            raise discord.DiscordException
        except AttributeError:
            await self.send_log('Guild not found ' + guild.name)
            raise discord.DiscordException
        else:
            await self.send_log('Left guild successfully ' + guild.name)

    @commands.command(name='sendtoall',
                      aliases=['send_to_all', 'send-to-all', 'broadcast'],
                      description='(textblock) || The bot will attempt to send the textblock to every server'
                                  ' he is a member of. Do NOT use for spamming purposes.')
    @ExtModule.is_admin()
    @ExtModule.reaction_respond
    async def sendtoall(self, ctx: commands.Context, *args):
        """This command tries to send a message to all guilds this bot is a member of.
        Args:
            ctx: The context of the command, which is mandatory in rewrite (commands.Context)
            args: The words of the message to be send
            """
        message = ''
        for word in args:
            message = message + str(word) + ' '
        message = message[:-1]
        for guild in self.bot.guilds:
            _channel = guild.text_channels[0]
            _maximum = max([len(channel.members) for channel in guild.text_channels])
            for channel in guild.text_channels:
                if len(channel.members) == _maximum:
                    _channel = channel
                    break               # take the topmost channel with most members reading it
            try:
                await _channel.send(message)
            except discord.Forbidden:
                await self.send_log('Missing permissions for guild ' + guild.name)
            except discord.HTTPException:
                await self.send_log('Failed to send message to ' + guild.name + ' with a connection error')
            else:
                await self.send_log('Successfully send the message to guild ' + guild.name)

    @commands.command(name='adminhelp',
                      aliases=['admin-help', 'admin_help', 'helpadmin'],
                      description='Sends you the names, aliases and description of all commands per PM!')
    @ExtModule.is_admin()
    @ExtModule.reaction_respond
    async def adminhelp(self, ctx: commands.Context):
        """This function sends a list of all the admin commands + aliases + description to the requester
                Args:
                    ctx: The context of the command, which is mandatory in rewrite (commands.Context)
        """
        _help_string = 'command name || (aliases): || arguments || help description\n'
        for command in self.bot.commands:
            if ExtModule.is_admin_predicate not in command.checks:
                continue
            _command_help = ExtModule._help(command)
            if len(_help_string) + len(_command_help) > 1800:
                try:
                    await ctx.message.author.send('```\n' + _help_string + '\n```')
                except discord.DiscordException:
                    raise PmForbidden
                _help_string = 'command name || (aliases): || help description\n\n' + _command_help
            else:
                _help_string = _help_string + '\n\n' + _command_help
        try:
            await ctx.author.send('```\n' + _help_string + '\n```')
        except discord.DiscordException:
            raise PmForbidden

    @commands.command(name='change_activity',
                      aliases=['change_game'],
                      description='Changes the activity in the activity feed of the bot')
    @ExtModule.is_admin()
    @ExtModule.reaction_respond
    async def change_activity(self, ctx: commands.Context, *args):
        """This function changes sets the activity in the activity feed of the bot to the words delivered in args
        Args:
            *args: The words of the activity
            ctx: The context of the command, which is mandatory in rewrite
        """
        activity = ''
        for word in args:
            activity = activity + ' ' + str(word)
        game = discord.Game(name=activity)
        await self.bot.change_presence(game=game)
        await self.send_log('Changed activity to: ' + activity)
