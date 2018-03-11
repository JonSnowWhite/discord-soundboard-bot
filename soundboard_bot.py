from discord.ext import commands
from cogs.sound_cog import SoundboardCog
from cogs.admin_cog import AdminCog
from cogs.user_cog import UserCog
from discord import opus


command_prefix = '!'
bot = commands.Bot(command_prefix=commands.when_mentioned_or(command_prefix))
sound_folder = '~~your folder~~'
log_channel_id = int('~~your log channel id~~')
standard_activity = command_prefix + 'help'
tag_dict={'tag1': ['name1', 'name2'],  # this dict saves the tags and their sounds. Be sure to use lists also when a tag has only 1 name
          'tag2': ['name1', 'name2', 'name3']}
bot.add_cog(SoundboardCog(bot=bot, folder=sound_folder, log_channel_id=log_channel_id, tag_dict=tag_dict))
bot.add_cog(AdminCog(bot=bot, log_channel_id=log_channel_id, activity =standard_activity))
bot.add_cog(UserCog(bot=bot, log_channel_id=log_channel_id))

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


bot.run('~~your token~~')
