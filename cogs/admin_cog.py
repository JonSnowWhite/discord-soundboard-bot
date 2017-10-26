from discord.ext import commands
import discord
from ext_module import ExtModule


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
        self.log_channel = None                  # will be assigned in the on_ready event

    async def on_ready(self):
        """Is called when the bot is completely started up. Calls in this function need variables only a started bot can give.
        """
        self.log_channel = self.bot.get_channel(self.log_channel_id)

    async def on_guild_join(self, guild: discord.Guild):
        """Is called when the bot joins a new guild. Sends an informative message to the log_channel
        Args:
            guild: The guild which the bot joined on (discord.Guild)
            """
        await self.log_channel.send('Joined guild: ' + guild.name)

    async def on_guild_remove(self, guild: discord.Guild):
        """Is called when the bot leaves a guild. Sends an informative message to the log_channel
        Args:
            guild: The guild which was left by the bot (discord.Guild)
            """
        await self.log_channel.send('Left guild: ' + guild.name)

    @commands.command(aliases=['list'],
                      description='Prints a list of all the servers'
                                  ' this bot is a member of to the admin log_channel')
    @ExtModule.is_admin()
    async def serverlist(self, ctx: commands.Context):
        """This function sends a list with all the servers this bot is a member of to the self.log_channel
        Args:
            ctx: The context of the command, which is mandatory in rewrite
        """
        _guild_names = 'List of all guilds: '
        for guild in self.bot.guilds:
            if len(_guild_names) + len(guild.name) > 1800:  # not accurate, 200 literals buffer catch it
                await self.log_channel.send(_guild_names)
                _guild_names = ''
            else:
                _guild_names = _guild_names + ', ' + guild.name + '(' + str(guild.id) + ')'
        await self.log_channel.send(_guild_names)
        return await ctx.channel.send('Serverlist send')

    @commands.command(description='(ID) || The bot will attempt to leave the server with the given ID.')
    @ExtModule.is_admin()
    async def leave(self, ctx: commands.Context, guild_id: int=None):
        """This commands makes the bot leave the server with the given ID
        Args:
            ctx: The context of the command, which is mandatory in rewrite (commands.Context)
            guild_id: The id of the server, which will be left (int)
            """
        guild = self.bot.get_guild(guild_id)
        try:
            await guild.leave()
        except discord.HTTPException:
            await self.log_channel.send('Could not leave guild ' + guild.name)
        except AttributeError:
            await self.log_channel.send('Guild not found ' + guild.name)
        else:
            await self.log_channel.send('Left guild successfully ' + guild.name)

    @commands.command(aliases=['send_to_all', 'send-to-all', 'broadcast'],
                      description='(textblock) || The bot will attempt to send the textblock to every server'
                                  ' he is a member of. Do NOT use for spamming purposes.')
    @ExtModule.is_admin()
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
                await self.log_channel.send('Missing permissions for guild ' + guild.name)
            except discord.HTTPException:
                await self.log_channel.send('Failed to send message to ' + guild.name + ' with a connection error')
            else:
                await self.log_channel.send('Successfully send the message to guild ' + guild.name)

    @commands.command(aliases=['admin-help', 'admin_help', 'helpadmin'],
                      description='Sends you the names, aliases and description of all commands per PM!')
    @ExtModule.is_admin()
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
                await ctx.message.author.send('```\n' + _help_string + '\n```')
                _help_string = 'command name || (aliases): || help description\n\n' + _command_help
            else:
                _help_string = _help_string + '\n\n' + _command_help
        await ctx.author.send('```\n' + _help_string + '\n```')
        return await ctx.channel.send('Help message(s) successfully delivered!')