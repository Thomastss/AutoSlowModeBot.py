# Discord Auto Slow Mode Bot (Python)

A robust Discord slowmode bot designed to handle chat floods with dynamic slowmode, channel locking capabilities, and automated logging with Embeds.

[![Discord Support](https://img.shields.io/badge/Discord-Support-7289DA?style=for-the-badge&logo=discord)](https://discord.gg/4YDMkn5u3y)

## 🚀 Features

* **Dynamic Slowmode:** Automatically detects message spikes and enables slowmode.
* **Auto-Reset:** A background task disables slowmode once the chat calms down.
* **Admin Immunity:** Admins/Moderators are exempt from slowmode logic.
* **Lock/Unlock System:** Quickly lock a channel for @everyone.
* **Centralized Embed Logging:** Sends moderation actions to a designated log channel with timestamps and mentions.
* **Customizable Prefix:** Change your bot's prefix easily via environment variables.

## 🛠️ Installation

1.  Clone the repository:
    git clone https://github.com/Thomastss/AutoSlowModeBot.py.git
    cd AutoSlowModeBot.py

2.  Install the required dependencies:
    pip install -r requirements.txt

3.  Set up your environment variables:
    * Copy the .env.example file and rename it to .env
    * Open .env and fill in your details.

4.  Create your Discord Bot:
    * Go to the Discord Developer Portal (https://discord.com/developers/applications).
    * Enable Message Content Intent under the Bot tab.
    * Invite the bot with Manage Channels and Manage Roles permissions.

## ⚙️ Configuration (.env)

Your .env file should follow this structure:

```.env
# Discord Bot Token (Get it from Discord Developer Portal)
DISCORD_TOKEN=your_token_here_is_hidden

# The ID of the channel where the bot will post logs
LOG_CHANNEL_ID=your_log_channel_id_here

# The prefix that you want the bot to use for commands
COMMAND_PREFIX=!
```

## 🎮 Commands

| Command | Permission | Description |
| :--- | :--- | :--- |
| !lock | Manage Roles | Completely locks the channel for regular members. |
| !unlock | Manage Roles | Unlocks the channel and resets permissions. |

*Note: Use the prefix defined in your .env file.*

## 📝 How it Works

The bot monitors the rate of incoming messages. If more than 10 messages are sent within a 10-second window, it calculates a dynamic slowmode delay (up to 30 seconds). Once it detects 15 seconds of inactivity, it automatically removes the slowmode. All actions are logged in the specified log channel using rich Embeds.

## ⚖️ License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Created by Thomas 2026**
