import os
import random
import socket

from discord.ext import commands
import subprocess

from relela_bot.discord_utils import send_embed_message
from relela_bot.nvidia_utils import get_gpu_status, get_running_status


def register_commands(bot):
    @bot.command(name="commands", help="show the commands availables")
    async def help(ctx):
        title = "Commands availables"
        message = """
        📌 commands: Displays the commands available.
        📌 gpustat: Displays the status of used GPUs.
        📌 runstatus: Displays a detailed log of the codes being executed on the server. 
        📌 ping: Check the bot's latency.
        """

        image_path = "./relela_bot/bot_images/monkey.jpeg"
        await send_embed_message(ctx, title, message, image_path)

    @bot.command(name="gpustat", help="Displays the status of used GPUs")
    async def gpustatus_relela1(ctx):
        hostname = socket.gethostname()
        title = f"GPU Status on {hostname}"
        gpu_info = get_gpu_status()
        for info in gpu_info:
            await ctx.send(f"{title}\n```python\n{info}```")

    @bot.command(
        name="runstatus",
        help="Displays a detailed log of the codes being executed on the server.",
    )
    async def runstatus(ctx):
        run_info = get_running_status()
        if run_info:
            
            try:
                run_gpustat = subprocess.run(["gpustat"], capture_output=True, text=True, check=True).stdout
            except (subprocess.SubprocessError, FileNotFoundError) as e:
                run_gpustat = ""
                await ctx.send(f">>> Error running gpustat: {str(e)}")
            print(run_gpustat)

            interest_values = [0, 2, 3, 8, 9]

            for it, line in enumerate(run_info.splitlines()):
                if it == 0:
                    continue
                line_list = line.split()
                line_list = [i for i in line_list if i]

                command_str = " ".join(line_list[10:])
                line_list = [line_list[i] for i in interest_values]

                for line in run_gpustat.splitlines():
                    if line_list[0] in line:
                        gpu_name = line.split("|")[0].strip()
                        usage_gpu = line.split("|")[2].strip()
                    else:
                        gpu_name = "N/A"
                        usage_gpu = "N/A"

                hour_date = line_list[3].split(":")[0]
                hour_date = (
                    f"{hour_date} AM" if int(hour_date) < 12 else f"{hour_date} PM"
                )
                hostname = socket.gethostname()

                title = "Running Status"
                str_out = f"""
                ```python
                SERVER    🖥️: {hostname}
                USER      👤: {line_list[0]}
                %CPU      💻: {line_list[1]}% 
                %MEM      🐏: {line_list[2]}%
                GPU       📇: {gpu_name}
                GPU USAGE 📉: {usage_gpu}
                START     📅: {hour_date}
                COMMAND   🤖: {command_str.strip()}
                ```
                """
                image_path = "./relela_bot/bot_images/status.gif"
                await send_embed_message(ctx, title, str_out, image_path)
        else:
            hostname = socket.gethostname()
            await ctx.send(f">>> Nadie se encuentra utilizando las GPUs en el servidor {hostname}.")
    
    @bot.command(name="ping", help="Check the bot's latency.")
    async def ping(ctx):
        latency = round(bot.latency * 1000)
        await ctx.send(f"🏓 Pong! Latency: {latency}ms")

    # @bot.command(name="roll_dice", help="Simulates rolling dice.")
    # async def roll(ctx, number_of_dice: int, number_of_sides: int):
    #     dice = [
    #         str(random.choice(range(1, number_of_sides + 1)))
    #         for _ in range(number_of_dice)
    #     ]
    #     await ctx.send(", ".join(dice))

    #@bot.command(
    #    name="checklog", help="Displays the last 5 lines of a log in txt or log format."
    #)
    #@commands.cooldown(1, 10, commands.BucketType.user)
    #async def checklog(ctx, path_log: str, n: int = 5):
    #    if not path_log.starts_with("./logs/"):
    #        await ctx.send("❌ Access denied.")
    #        return
    #    with open(path_log, "r") as file:
    #        lines = file.read().splitlines()
    #    lines = lines[-n:]

    #    for line in lines:
    #        await ctx.send(line)
