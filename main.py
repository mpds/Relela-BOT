from discord.ext import commands

from relela_bot.commands import register_commands
from relela_bot.tasks import start_tasks
from relela_bot.utils import init_bot, init_dataframes, load_env_vars

# Initialize environment variables, dataframes, and bot
TOKEN, CHANNEL_1 = load_env_vars()
init_dataframes()
bot = init_bot()

# Register commands
register_commands(bot)

# Start tasks
start_tasks(bot, CHANNEL_1)

# Run server
bot.run(TOKEN)
