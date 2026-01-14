# Discord Guard Bot (Python)

A robust Discord moderation bot designed to handle chat floods with dynamic slowmode, channel locking capabilities, and automated logging.

## 🚀 Features

* **Dynamic Slowmode:** Automatically detects message spikes and enables slowmode. The delay increases based on the intensity of the "flood."
* **Auto-Reset:** A background task monitors channel activity and disables slowmode once the chat calms down.
* **Admin Immunity:** Administrators and Moderators (with Manage Messages permission) are exempt from triggering the slowmode logic.
* **Lock/Unlock System:** Quickly lock a channel to prevent @everyone from sending messages during raids or emergencies.
* **Centralized Logging:** Sends all moderation actions and automated changes to a designated log channel.
* **Secure Configuration:** Uses environment variables (.env) to keep your bot token and sensitive IDs safe.

## 🛠️ Installation

1.  Clone the repository:
    git clone [https://github.com/yourusername/your-repo-name.git](https://github.com/yourusername/your-repo-name.git)
    cd your-repo-name

2.  Install the required dependencies:
    This bot requires discord.py and python-dotenv.
    pip install discord.py python-dotenv

3.  Create your Discord Bot:
    * Go to the Discord Developer Portal ([https://discord.com/developers/applications](https://discord.com/developers/applications)).
    * Create a new Application and add a Bot.
    * Enable Message Content Intent under the Bot tab.
    * Invite the bot to your server with Manage Channels and Manage Roles permissions.

## ⚙️ Environment Setup (.env)

The bot uses a .env file to store sensitive information. Create a file named .env in the root directory and add the following (without quotes or backticks):
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

The bot monitors the rate of incoming messages. If more than 10 messages are sent within a 10-second window, the bot calculates a dynamic slowmode delay (up to 30 seconds) and applies it to the channel. Once the bot detects 15 seconds of inactivity, it automatically removes the slowmode.

---

**Created by Thomas &copy; 2026**
