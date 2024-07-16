# ReLeLa Discord Bot

<p align="center"> 
<img src="./images/logo_relela.png" width=250/>
</p>

A Discord bot for monitoring GPU usage and running various commands, designed to assist users in managing and tracking server resources.

## Features

- **gpustat**: Displays the status of used GPUs.
- **runstatus**: Displays a detailed log of the codes being executed on the server.
- **checklog**: Displays the last 5 lines of a log file in txt or log format.
- **roll_dice**: Simulates rolling dice.

## Setup

### Prerequisites

- Python 3.7 or higher
- Discord account and bot token
- NVIDIA GPU and drivers
- `nvidia-smi` installed and accessible from the command line

### Environment Variables

Create a `.env` file in the root directory and add your Discord bot token and channel ID:

```env
DISCORD_TOKEN_RELELA_1=your_discord_bot_token
DISCORD_CHANNEL_1=your_discord_channel_id
```

### Data Files

The bot uses a CSV file to track user activity. Ensure the `./execution_data/df_backup.csv` file exists in the root directory:

```csv
user,datetime
```

## Running the Bot

Run the bot using the following command:

```sh
python bot.py
```

## Commands

### General Commands

- `!commands`: Show the available commands.

### GPU Monitoring

- `!gpustat`: Displays the status of used GPUs.
- `!runstatus`: Displays a detailed log of the codes being executed on the server.

### Utility

- `!checklog [path]`: Displays the last 5 lines of a log file in txt or log format.
- `!roll_dice [number_of_dice] [number_of_sides]`: Simulates rolling dice.