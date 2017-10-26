"""This module contains additional functions, checks and classes used int the Cogs"""
from discord.ext import commands


class ExtModule:

    @staticmethod
    async def is_admin_predicate(ctx: commands.Context):
        """The predicate which will later be used to define a command check.
        Args:
            ctx: The context of the command, which is mandatory in rewrite(commands.Context)
        Returns:
            Boolean: True or False, wether the invoker of a command fulfills the predicate
            """
        return commands.is_owner()

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
