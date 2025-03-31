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

            interest_values = [0, 2, 3, 8, 9]

            for it, line in enumerate(run_info.splitlines()):
                if it == 0:
                    continue
                line_list = line.split()
                line_list = [i for i in line_list if i]

                if len(line_list) < max(interest_values) + 1:
                    continue  # Skip if line doesn't have enough elements

                command_str = " ".join(line_list[10:])
                line_list = [line_list[i] for i in interest_values]

                # Initialize GPU info as N/A
                gpu_name = "N/A"
                usage_gpu = "N/A"
                
                # Search for GPU info only if we have a username to match
                if line_list[0] and run_gpustat:
                    for gpu_line in run_gpustat.splitlines():
                        if line_list[0] in gpu_line:
                            parts = gpu_line.split("|")
                            if len(parts) > 2:
                                gpu_name = parts[0].strip()
                                usage_gpu = parts[2].strip()
                            break

                # Parse the time information more safely
                time_info = line_list[3] if len(line_list) > 3 else ""
                hour_date = time_info  # Default to full time string
                
                try:
                    # Try to parse as "HH:MM:SS" format
                    if ":" in time_info:
                        time_parts = time_info.split(":")
                        if len(time_parts) >= 2:
                            hour = int(time_parts[0])
                            period = "AM" if hour < 12 else "PM"
                            if hour > 12:
                                hour -= 12
                            hour_date = f"{hour}:{time_parts[1]} {period}"
                except (ValueError, IndexError):
                    pass  # Keep original format if parsing fails

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
