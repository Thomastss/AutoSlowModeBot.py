import discord
from discord.ext import commands, tasks
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
LOG_CHANNEL_ID = int(os.getenv('LOG_CHANNEL_ID'))

# Initialize intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True 
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Dictionary to store message timestamps per channel
message_counts = {}

# Helper function for logging
async def log_to_channel(text):
    print(text) # Also print to console
    log_channel = bot.get_channel(LOG_CHANNEL_ID)
    if log_channel:
        await log_channel.send(f"📝 **Log:** {text}")

# 2. SUGGESTION: Background task to reset slowmode if channel becomes quiet
@tasks.loop(seconds=10)
async def auto_reset_slowmode():
    now = time.time() * 1000
    for channel_id in list(message_counts.keys()):
        messages = message_counts[channel_id]
        if messages and (now - messages[-1] > 15000):
            channel = bot.get_channel(channel_id)
            if channel and hasattr(channel, 'slowmode_delay') and channel.slowmode_delay != 0:
                await channel.edit(slowmode_delay=0)
                await log_to_channel(f"Slowmode disabled in {channel.name} due to inactivity.")
                message_counts[channel_id] = [] 

async def check_slowmode(channel):
    now = time.time() * 1000
    if channel.id not in message_counts:
        message_counts[channel.id] = []
        
    messages = message_counts[channel.id]
    
    while messages and (now - messages[0] > 10000):
        messages.pop(0)

    if len(messages) >= 10:
        time_elapsed = now - messages[0]
        if time_elapsed < 10000:
            slowmode_delay = min(30, (len(messages) // 10) * 2)
            if channel.slowmode_delay != slowmode_delay:
                await channel.edit(slowmode_delay=slowmode_delay)
                await log_to_channel(f"Dynamic Slowmode: {slowmode_delay}s set in {channel.name}")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    if not auto_reset_slowmode.is_running():
        auto_reset_slowmode.start()

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # 1. SUGGESTION: Admin Immunity
    if message.author.guild_permissions.manage_messages:
        await bot.process_commands(message)
        return

    channel_id = message.channel.id
    if channel_id not in message_counts:
        message_counts[channel_id] = []
    
    message_counts[channel_id].append(time.time() * 1000)
    await check_slowmode(message.channel)
    await bot.process_commands(message)

# 5. SUGGESTION: Lock and Unlock commands
@bot.command()
@commands.has_permissions(manage_roles=True)
async def lock(ctx):
    """Disables the ability for @everyone to send messages."""
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send("🔒 **Channel Locked.**")
    await log_to_channel(f"Channel {ctx.channel.name} was **locked** by {ctx.author}.")

@bot.command()
@commands.has_permissions(manage_roles=True)
async def unlock(ctx):
    """Resets permissions for @everyone."""
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=None)
    await ctx.send("🔓 **Channel Unlocked.**")
    await log_to_channel(f"Channel {ctx.channel.name} was **unlocked** by {ctx.author}.")

bot.run(TOKEN)