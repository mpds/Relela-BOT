import os
from datetime import datetime

import pandas as pd
from discord.ext import tasks

from relela_bot.discord_utils import (
    send_gpu_alert_embed_message,
    send_gpu_not_usage_embed_message,
    send_gpu_usage_embed_message,
)
from relela_bot.nvidia_utils import get_running_status


def start_tasks(bot, CHANNEL_1):
    @bot.listen()
    async def on_ready():
        task_loop.start()

    @tasks.loop(seconds=10)
    async def task_loop(
        backup_path="./backup_data/df_backup.csv",
        seconds_to_check=10,
        seconds_to_alert=30,
    ):
        print("working...")
        channel = bot.get_channel(int(CHANNEL_1))
        run_info = get_running_status()

        if os.path.exists(backup_path):
            df_backup = pd.read_csv(backup_path, index_col=[0])
        else:
            df_backup = pd.DataFrame(columns=["user", "datetime"])

        if run_info:
            for it, line in enumerate(run_info.splitlines()):
                if it == 0:
                    continue
                line_list = line.split()
                line_list = [i for i in line_list if i]
                user_name = line_list[0]

                if user_name not in df_backup["user"].values:
                    print(f"User {user_name} is using the GPU")
                    await send_gpu_usage_embed_message(channel, user_name)

                dict_users = {"user": user_name, "datetime": datetime.now()}
                df_backup = pd.concat([df_backup, pd.DataFrame(dict_users, index=[0])])
                df_backup = df_backup.reset_index(drop=True)

            df_backup["datetime"] = pd.to_datetime(df_backup["datetime"])
            print(df_backup["user"].unique())
            for user_name in df_backup["user"].unique():
                min_date = df_backup[df_backup["user"] == user_name]["datetime"].min()
                max_date = df_backup[df_backup["user"] == user_name]["datetime"].max()
                if (max_date - min_date).seconds >= seconds_to_alert:
                    await send_gpu_alert_embed_message(
                        channel, user_name, (max_date - min_date).seconds / 3600
                    )
                    # df_backup = df_backup[df_backup["user"] != user_name]
        else:
            for user_name in df_backup["user"].unique():
                max_date = df_backup[df_backup["user"] == user_name]["datetime"].max()
                max_date = pd.to_datetime(max_date)
                if (datetime.now() - max_date).seconds >= seconds_to_check:
                    df_backup = df_backup[df_backup["user"] != user_name]
                    await send_gpu_not_usage_embed_message(channel, user_name)

        df_backup.to_csv(backup_path)
