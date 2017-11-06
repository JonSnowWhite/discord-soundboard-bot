"""This module contains additional functions, checks and classes used int the Cogs"""
from discord.ext import commands
import discord


class ExtModule:

    @staticmethod
    async def is_admin_predicate(ctx: commands.Context):
        """The predicate which will later be used to define a command check.
        Args:
            ctx: The context of the command, which is mandatory in rewrite(commands.Context)
        Returns:
            Boolean: True or False, wether the invoker of a command fulfills the predicate
            """
        return await ctx.bot.is_owner(ctx.author)

    @staticmethod
    def is_admin():
        """Command check that checks, if a command is invoked by an admin.
        """
        return commands.check(ExtModule.is_admin_predicate)

    @staticmethod
    def _help(command: commands.Command):
        """The body of the help and the adminhelp command
        Args:
            command: The command that will be formatted properly (commands.Command)
        Returns:
            _command_help: Formatted string (str)
            """
        _name = command.name
        _description = command.description if command.description is not '' else 'No help description available'
        _aliases = ''
        for alias in command.aliases:
            _aliases = _aliases + str(alias) + ', '
        _aliases = '(' + _aliases[:-2] + ')'
        return _name + ' ' + _aliases + ': ' + _description

    @staticmethod
    def _send_log_generator(log_channel):
        """Returns a send_log_channel function
        Args:
            log_channel: The destination send_log() will send its logs to, can be a user and text channel
            (inheriting class of both discord.Snowflake and discord.Messageable)
        Returns:
              send_log(): A function which sends the given message to the log_channel
            """
        async def send_log(message: str):
            """Sends the given message to the log_channel found in the closure. Using this function allows for easy logging
            Args:
                message: The message to be send
                """
            try:
                x = await log_channel.send(message)
                return x
                # return await log_channel.send(message)
            except discord.Forbidden:
                print('Permissions for log channel with id ' + str(log_channel.id) + ' missing')
            except discord.HTTPException:
                print('Sending a message to ' + log_channel.name + ' failed.')
        return send_log

    @staticmethod
    def get_send_log(cog):
        _log_channel = cog.bot.get_channel(cog.log_channel_id)
        if _log_channel is None:
            _log_channel = cog.bot.get_user(cog.log_channel_id)
        if _log_channel is None:
            print('ID for log_channel of cog ' + cog.__class__.__name__ + 'is not valid')
            return lambda x: print('Could not print help message' + x +
                                   'to log_channel of Cog' + cog.__class__.__name__ +
                                   'due to an invalid ID.')
        else:
            return ExtModule._send_log_generator(_log_channel)

    @staticmethod
    def reaction_respond(fun):
        """This decorator will catch any Exceptions commands may give and give different discord.Reactions considering
        if any (and if yes, which?) Exceptions occurred. The command will not have to handle feedback to the User,
        the User will see a simple reply through reactions and the bot does not need write permissions for commands,
        which do not base on text response.
        """
        async def responded_function(self, ctx: commands.Context, *args):
            try:
                await fun(self, ctx, *args)
            except PmForbidden:
                await ctx.message.add_reaction('\U0001F1F2')
                await ctx.message.add_reaction('\U0001F1F5')
                await ctx.message.add_reaction('\U0000274C')
                await ctx.message.add_reaction('\U0001F1F5')
                await ctx.message.add_reaction('\U0001F1EA')
                await ctx.message.add_reaction('\U0001F1F7')
                await ctx.message.add_reaction('\U0001F1F2')
                await ctx.message.add_reaction('\U0001F1F8')
            except discord.Forbidden:
                await ctx.message.add_reaction('\U0000274C')
                await ctx.message.add_reaction('\U0001F1F5')
                await ctx.message.add_reaction('\U0001F1EA')
                await ctx.message.add_reaction('\U0001F1F7')
                await ctx.message.add_reaction('\U0001F1F2')
                await ctx.message.add_reaction('\U0001F1F8')
            except Exception:
                await ctx.message.add_reaction('\U0000274C')
            else:
                await ctx.message.add_reaction('\U00002705')
        return responded_function


class PmForbidden(discord.Forbidden):
    """Exception that will be thrown manually after a pm to a user failed with discord.Forbidden
    """
    pass
