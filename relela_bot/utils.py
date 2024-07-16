import os

import discord
import pandas as pd
from discord.ext import commands
from dotenv import load_dotenv


# Module for environment variables
def load_env_vars():
    load_dotenv()
    return os.getenv("DISCORD_TOKEN_RELELA_1"), os.getenv("DISCORD_CHANNEL_1")


# Module for initializing dataframes
def init_dataframes():
    df_backup = pd.DataFrame(columns=["user", "datetime"])
    df_backup.to_csv("./backup_data/df_backup.csv")


# Module for initializing bot
def init_bot():
    intents = discord.Intents.default()
    intents.message_content = True
    return commands.Bot(intents=intents, command_prefix="!")
