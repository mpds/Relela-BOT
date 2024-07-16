####################################################################################
#  Required libraries

import os
import json
import random
import datetime
import nvidia_smi
import pandas as pd
from datetime import datetime

import discord
from discord.ext import commands
from discord.ext import tasks

from dotenv import load_dotenv

import subprocess
from subprocess import call

####################################################################################

# Load Server and Channel Ids
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN_RELELA_1")
CHANNEL_1 = os.getenv("DISCROD_CHANNEL_1")

# Create dataframes to check usage status
df_backup = pd.DataFrame(columns=["user", "datetime"])
df_backup.to_csv("df_backup.csv")

# Initialize bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(intents=intents, command_prefix="!")

####################################################################################

# Discord functions and commands
@bot.command(name="commands", help="show the commands availables")
async def help(ctx):
    message = """
    ```
    ◾ gpustat: Displays the status of used GPUs.
    ◾ runstatus: Displays a detailed log of the codes being executed on the server. 
        The query shows ram memory, cpu usage, vram usage, query start date, gpu used and running command.
    ◾ checklog: Displays the last 5 lines of a log in txt or log format. Example: !checklog [path]
    ◾ roll_dice: Roll a die. Example: !roll_dice 2 6 (WHY?, IDK)
    ```
              """
    await ctx.send(message)


@bot.command(name="gpustat", help="Displays the status of used GPUs")
async def gpustatus_relela1(ctx):
    nvidia_smi.nvmlInit()

    deviceCount = nvidia_smi.nvmlDeviceGetCount()
    for i in range(deviceCount):
        handle = nvidia_smi.nvmlDeviceGetHandleByIndex(i)
        info = nvidia_smi.nvmlDeviceGetMemoryInfo(handle)
        info = "Device {}: {}, Memory : ({:.2f}% free): {} GB (total), {} GB (free), {} GB (used)".format(
            i,
            nvidia_smi.nvmlDeviceGetName(handle).decode("utf-8"),
            100 * info.free / info.total,
            round(info.total / (1024**3), 3),
            round(info.free / (1024**3), 3),
            round(info.used / (1024**3), 3),
        )
        print(info)
        await ctx.send(info)

    nvidia_smi.nvmlShutdown()


@bot.command(
    name="runstatus",
    help="Displays a detailed log of the codes being executed on the server.",
)
async def runstatus(ctx):

    run_info = os.popen(
        "ps -up `nvidia-smi -q -x | grep pid | sed -e 's/<pid>//g' -e 's/<\/pid>//g' -e 's/^[[:space:]]*//'`"
    ).read()

    if run_info != "":
        run_gpustat = os.popen("gpustat").read()
        interest_values = [0, 2, 3, 8, 9]

        for it, line in enumerate(run_info.splitlines()):
            if it == 0:
                continue
            line_list = line.split(" ")
            line_list = [i for i in line_list if "" != i]

            print(line_list)

            command_str = ""
            for e in range(10, len(line_list)):
                command_str = command_str + " " + line_list[e]

            line_list = [line_list[i] for i in interest_values]

            for line in run_gpustat.splitlines():
                if line_list[0] in line:
                    gpu_name = line.split("|")[0]
                    usage_gpu = line.split("|")[2].strip()
                    gpu_name = gpu_name.strip()

            try:
                hour_date = int(line_list[3].split(":")[0])
                if hour_date < 12:
                    hour_date = line_list[3] + " AM"
                else:
                    hour_date = line_list[3] + " PM"
            except:
                hour_date = str(line_list[3].split(":")[0])

            command_line = line.split(" python")[-1]

            str_out = f"""
            ```python
            SERVER    🖥️: ReLeLa-01
            USER      👤: {line_list[0]}
            %CPU      💻: {line_list[1]}% 
            %MEM      🐏: {line_list[2]}%
            GPU       📇: {gpu_name}
            GPU USAGE 📉: {usage_gpu}
            START     📅: {hour_date}
            COMMAND   🤖: {command_str.strip()}
            ```
            """
            print(str_out)
            await ctx.send(str_out)

    else:
        await ctx.send(">>> Nadie se encuentra utilizando las GPUs")


@bot.command(name="roll_dice", help="Simulates rolling dice.")
async def roll(ctx, number_of_dice, number_of_sides):
    number_of_dice = int(number_of_dice)
    number_of_sides = int(number_of_sides)

    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(", ".join(dice))


@bot.listen()
async def on_ready():
    task_loop.start()


@tasks.loop(seconds=1800)
async def task_loop():
    print("working...")
    channel = bot.get_channel(CHANNEL_1)
    dict_users = {}
    run_info = os.popen(
        "ps -up `nvidia-smi -q -x | grep pid | sed -e 's/<pid>//g' -e 's/<\/pid>//g' -e 's/^[[:space:]]*//'`"
    ).read()
    df_backup = pd.read_csv("df_backup.csv", index_col=[0])

    for it, line in enumerate(run_info.splitlines()):
        if it == 0:
            continue
        line_list = line.split(" ")
        line_list = [i for i in line_list if "" != i]
        user_name = line_list[0]
        dict_users["user"] = user_name
        dict_users["datetime"] = datetime.now()
        df_backup = pd.concat([df_backup, pd.DataFrame(dict_users, index=[0])])
        df_backup = df_backup.reset_index(drop=True)

    df_backup["datetime"] = pd.to_datetime(df_backup["datetime"])
    for user in df_backup["user"].unique():
        min_date = df_backup[df_backup["user"] == user]["datetime"].min()
        max_date = df_backup[df_backup["user"] == user]["datetime"].max()
        if (max_date - min_date).seconds > 86400:
            string_output = f"{user} aún sigues utilizando la gpu?, las has utilizado por mas de 24 hrs"
            print(string_output)
            await channel.send(string_output)
            df_backup = df_backup[df_backup["user"] != user]

    df_backup.to_csv("df_backup.csv")


@bot.command(
    name="checklog",
    help="Displays the last 5 lines of a log in txt or log format.",
)
async def checklog(ctx, path_log, n=5):
    file = open(path_log, "r")
    lines = file.read().splitlines()
    file.close()
    lines = lines[len(lines) - int(n) :]

    for line in lines:
        await ctx.send(line)


####################################################################################
# run server
bot.run(TOKEN)
