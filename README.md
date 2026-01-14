# AutoSlowModeBot (Python)

A robust Discord moderation bot designed to handle chat floods with dynamic slowmode, channel locking capabilities, and automated logging.

## 🚀 Features

* **Dynamic Slowmode:** Automatically detects message spikes and enables slowmode.
* **Auto-Reset:** A background task disables slowmode once the chat calms down.
* **Admin Immunity:** Admins/Moderators are exempt from slowmode logic.
* **Lock/Unlock System:** Quickly lock a channel for @everyone.
* **Centralized Logging:** Sends moderation actions to a designated log channel.
* **Secure Configuration:** Uses .env files to keep secrets safe.

## 🛠️ Installation

1.  Clone the repository:
    git clone https://github.com/yourusername/your-repo-name.git
    cd your-repo-name

2.  Install the required dependencies:
    pip install discord.py python-dotenv

3.  Set up your environment variables:
    * Copy the .env.example file and rename it to .env
    * Open .env and paste your Discord Token and Log Channel ID.

4.  Create your Discord Bot:
    * Go to the Discord Developer Portal (https://discord.com/developers/applications).
    * Enable Message Content Intent under the Bot tab.
    * Invite the bot with Manage Channels and Manage Roles permissions.

## ⚙️ Configuration (.env)

Your .env file should look like this (but with your real data):
```.env
DISCORD_TOKEN=your_bot_token_here
LOG_CHANNEL_ID=your_log_channel_id_here
```

## 🎮 Commands

| Command | Permission | Description |
| :--- | :--- | :--- |
| !lock | Manage Roles | Completely locks the channel for regular members. |
| !unlock | Manage Roles | Unlocks the channel and resets permissions. |

## 📝 How it Works

The bot monitors the rate of incoming messages. If more than 10 messages are sent within a 10-second window, it calculates a dynamic slowmode delay (up to 30 seconds). Once it detects 15 seconds of inactivity, it removes the slowmode.

## ⚖️ License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Created by Thomas 2026**
