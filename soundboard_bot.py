from discord.ext import commands
from cogs.sound_cog import SoundboardCog
from cogs.admin_cog import AdminCog
from cogs.user_cog import UserCog
from discord import opus


command_prefix = '!'
bot = commands.Bot(command_prefix=commands.when_mentioned_or(command_prefix))
sound_folder = '~~your folder~~'
log_channel_id = int('~~your log channel id~~')
bot.add_cog(SoundboardCog(bot=bot, folder=sound_folder, log_channel_id=log_channel_id))
bot.add_cog(AdminCog(bot=bot, log_channel_id=log_channel_id))
bot.add_cog(UserCog(bot=bot, log_channel_id=log_channel_id))

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    opus.load_opus('libopus.so.0')  # the opus library


bot.run('~~your token~~')
