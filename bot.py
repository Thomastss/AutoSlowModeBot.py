import discord
from discord.ext import commands, tasks
import time
import os
import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
LOG_CHANNEL_ID = int(os.getenv('LOG_CHANNEL_ID'))
PREFIX = os.getenv('COMMAND_PREFIX', '!') # Διαβάζει το prefix, default είναι το '!'

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True 
intents.guilds = True

# Χρήση του PREFIX από το .env
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

message_counts = {}

# --- Logging Function ---
async def log_to_channel(action, channel=None, user=None, color=discord.Color.blue()):
    log_channel = bot.get_channel(LOG_CHANNEL_ID)
    if not log_channel: return
    
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    bold_time = f"**{current_time}**"
    
    embed = discord.Embed(
        title="🛡️ Security Log", 
        description=f"Action recorded at {bold_time}", 
        color=color
    )
    embed.add_field(name="Action", value=action, inline=False)
    
    if channel: 
        embed.add_field(name="Channel", value=channel.mention, inline=True)
    if user: 
        embed.add_field(name="Moderator/User", value=user.mention, inline=True)
        
    await log_channel.send(embed=embed)

@tasks.loop(seconds=10)
async def auto_reset_slowmode():
    now = time.time() * 1000
    for channel_id in list(message_counts.keys()):
        messages = message_counts[channel_id]
        if messages and (now - messages[-1] > 15000):
            channel = bot.get_channel(channel_id)
            if channel and hasattr(channel, 'slowmode_delay') and channel.slowmode_delay != 0:
                await channel.edit(slowmode_delay=0)
                await log_to_channel("Slowmode disabled (Inactivity)", channel=channel, color=discord.Color.green())
                message_counts[channel_id] = [] 

async def check_slowmode(channel):
    now = time.time() * 1000
    if channel.id not in message_counts: message_counts[channel.id] = []
    messages = message_counts[channel.id]
    while messages and (now - messages[0] > 10000): messages.pop(0)
    if len(messages) >= 10:
        time_elapsed = now - messages[0]
        if time_elapsed < 10000:
            slowmode_delay = min(30, (len(messages) // 10) * 2)
            if channel.slowmode_delay != slowmode_delay:
                await channel.edit(slowmode_delay=slowmode_delay)
                await log_to_channel(f"Dynamic Slowmode enabled: **{slowmode_delay}s**", channel=channel, color=discord.Color.orange())

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    print(f'Current prefix: {PREFIX}') # Επιβεβαίωση στην κονσόλα
    if not auto_reset_slowmode.is_running(): auto_reset_slowmode.start()

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.reply(
            f"❌ {ctx.author.mention}, you don't have the **Manage Roles** permission!", 
            delete_after=10
        )
        try:
            await ctx.message.delete(delay=10)
        except:
            pass

@bot.event
async def on_message(message):
    if message.author.bot: return
    
    if message.author.guild_permissions.manage_messages:
        await bot.process_commands(message)
        return
        
    channel_id = message.channel.id
    if channel_id not in message_counts: message_counts[channel_id] = []
    message_counts[channel_id].append(time.time() * 1000)
    await check_slowmode(message.channel)
    await bot.process_commands(message)

@bot.command()
@commands.has_permissions(manage_roles=True)
async def lock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send("🔒 **Channel Locked.**")
    await log_to_channel("Channel manually **Locked**", channel=ctx.channel, user=ctx.author, color=discord.Color.red())

@bot.command()
@commands.has_permissions(manage_roles=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=None)
    await ctx.send("🔓 **Channel Unlocked.**")
    await log_to_channel("Channel manually **Unlocked**", channel=ctx.channel, user=ctx.author, color=discord.Color.green())

bot.run(TOKEN)