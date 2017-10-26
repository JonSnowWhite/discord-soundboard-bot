from discord.ext import commands
import discord
from ext_module import ExtModule


class UserCog:
    """This Cog contains Interaction enhancing commands for the User
    """
    def __init__(self, bot: commands.Bot, log_channel_id: int=None):
        """The constructor of the UserCog class, assigns the important variables
        Args:
            bot: The bot the commands will be added to (commands.Bot)
            log_channel_id: The id of the log_channel (int)
        """
        self.bot = bot
        self.log_channel_id = log_channel_id
        self.log_channel = None             # will be assigned in the on_ready event
        self.bot.remove_command('help')

    async def on_ready(self):
        """Is called when the bot is completely started up. Calls in this function need variables only a started bot can give.
        """
        self.log_channel = self.bot.get_channel(self.log_channel_id)

    @commands.command(aliases=['complain', 'suggestion', 'complaint'],
                      description='(textblock) || The textblock will be send as a suggestion'
                                  ' to the admins of this bot. You can also use this for bug report!')
    async def suggest(self, ctx: commands.Context, *args):
        """This command sends the text given to the log_channel and pins it there.
        Args:
            ctx: The context of the command, which is mandatory in rewrite (commands.Context)
            args: The words the text will consist of (str)
            """
        text = ''
        for word in args:
            text = text + str(word) + ' '
        text = text[:-1]
        message = await self.log_channel.send('***New suggestion:*** ' + text)
        try:
            await message.pin()
        except discord.Forbidden:
            await self.log_channel.send('Couldnt pin the last suggestion due to permissions')
        except discord.HTTPException:
            await self.log_channel.send('Pinning the last suggestion failed. More than 50 pins?')
        return await ctx.author.send('Your suggestion has been received and will be taken into consideration.'
                                     ' Visit the repo for more information: \n '
                                     '<https://github.com/JonSnowWhite/discord-soundboard-bot>')

    @commands.command(aliases=['hlep', 'mayday'],
                      description='Sends you the names, aliases and description of all commands per PM!')
    async def help(self, ctx: commands.Context):
        """This function sends a list of all the command + aliases + description to the requester
        Args:
            ctx: The context of the command, which is mandatory in rewrite (commands.Context)
            """
        _help_string = 'command name || (aliases): || arguments || help description\n'
        for command in self.bot.commands:
            if ExtModule.is_admin_predicate in command.checks:
                continue
            _command_help = ExtModule._help(command)
            if len(_help_string) + len(_command_help) > 1800:
                await ctx.message.author.send('```\n' + _help_string + '\n```')
                _help_string = 'command name || (aliases): || help description\n\n' + _command_help
            else:
                _help_string = _help_string + '\n\n' + _command_help
        await ctx.author.send('```\n' + _help_string + '\n```')
        return await ctx.channel.send('Help message(s) successfully delivered!')
