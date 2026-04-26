from flask import Flask, jsonify
import discord
from discord.ext import commands
import re
import threading
import time

app = Flask(__name__)

# --- CONFIGURATION ---
TOKEN = 'MTQ5NDk1MzYyMDgxNzU4MDIxMw.G_ZsaU.OQPcHDL4zGB_eYZrlgSV34ieg_RstubhYdsgIo'
PING_CHANNEL_ID = 1494916192811614269 
ALLOWED_ROLES = [1494585525431173150, 1494585579503878225]

# The 3 specific Voice Channel IDs to moderate
MONITORED_VC_CHANNELS = [
    1497743873194070136,
    1494586238349475953, 
    1494586241193349213
]

# --- SETUP ---
intents = discord.Intents.default()
intents.members = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

def has_invalid_name(display_name):
    """
    Returns True if the name is INVALID (missing callsign).
    """
    strict_patterns = [
        r"^[789]D-\d+",     # LEO
        r"^PUMP-\d+",       # Fire
        r"^AER-\d+", 
        r"^TANK-\d+",
        r"^AMB-\d+",
        r"^EMS-\d+",
        r"^E-\d+",
        r"^TOW-\d+",
        r"^PLOW-\d+"
    ]
    combined = "|".join(strict_patterns)
    return not re.match(combined, display_name, re.IGNORECASE)

async def send_violation_embed(member):
    # Skip staff/bypass roles
    if any(role.id in ALLOWED_ROLES for role in member.roles):
        return

    if has_invalid_name(member.display_name):
        channel = bot.get_channel(PING_CHANNEL_ID)
        if channel:
            try:
                embed = discord.Embed(
                    description=(
                        "You're currently not following the rules of our <#1494586214710509588>. "
                        "Please ensure your Discord nickname matches your Roblox username.\n\n"
                        "**LEO Callsigns**:\n"
                        "Broward County Sheriff's - `9D-### | Username`\n"
                        "Fort Lauderdale Police - `8D-### | Username`\n"
                        "Florida Highway Patrol- `7D-### | Username`\n\n"
                        "**Fire/EMS Callsigns**:\n"
                        "Pumpers - `PUMP-# | Username`\n"
                        "Ladder/Aerials - `AER-# | Username`\n"
                        "EMS - `EMS-# | Username`\n"
                        "Engines - `E-# | Username`\n\n\n"
                        "-# Be sure to replace the hashtags with your unit number. Place your "
                        "Roblox username where it states \"username\"."
                    ),
                    color=16777215
                )
                embed.set_thumbnail(url="https://media.discordapp.net/attachments/1461933173012168818/1494567335615266826/flrp_new_logo.png?ex=69e50e0c&is=69e3bc8c&hm=9369a5616f4a4956f523b22255f2a4a7783a9558af87d81eacf695b2f6bda3b4&")
                embed.set_author(name="Fort Lauderdale Roleplay Automation")

                await channel.send(content=f"{member.mention}", embed=embed)
            except Exception as e:
                print(f"Error: {e}")

@bot.event
async def on_voice_state_update(member, before, after):
    """
    Triggers ONLY when a user interacts with a voice channel.
    """
    # 1. Check if the user is JOINING one of the 3 target channels
    if after.channel and after.channel.id in MONITORED_VC_CHANNELS:
        
        # 2. Check if they were NOT in this channel before
        # (This prevents pings when they just mute/unmute or deafen)
        if before.channel is None or before.channel.id != after.channel.id:
            await send_violation_embed(member)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}. Monitoring ONLY the 3 specified VCs.')

def run_bot():
    """Run the Discord bot in a separate thread"""
    bot.run(TOKEN)

# Flask routes
@app.route('/')
def home():
    return jsonify({
        "status": "running",
        "service": "Fort Lauderdale Roleplay Discord Bot",
        "description": "Monitoring voice channels for callsign compliance"
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

@app.route('/status')
def status():
    return jsonify({
        "bot_connected": bot.is_ready() if hasattr(bot, 'user') else False,
        "monitored_channels": MONITORED_VC_CHANNELS,
        "ping_channel": PING_CHANNEL_ID
    })

if __name__ == '__main__':
    # Start Discord bot in background thread
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    
    # Give bot time to connect
    time.sleep(2)
    
    # Start Flask web server
    app.run(host='0.0.0.0', port=8080)
