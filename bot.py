import discord
import os
from discord.ext import commands
from discord import app_commands

# ==========================================
# 1. DROPDOWN MENU SETUP
# ==========================================

class JJSDropdown(discord.ui.Select):
    def __init__(self):
        # Define the options the user will see in the menu
        options = [
            discord.SelectOption(
                label="Sedse JJS Script", 
                description="Click here for the Sedse JJS Script", 
                emoji="📜",
                value="sedse_jjs"
            ),
            discord.SelectOption(
                label="JJS Piano", 
                description="Click here for info on JJS Piano", 
                emoji="🎹",
                value="jjs_piano"
            ),
            discord.SelectOption(
                label="JJS Piano Open Source", 
                description="Click here for info on the Open Source version", 
                emoji="💻",
                value="jjs_piano_os"
            )
        ]
        super().__init__(
            placeholder="Choose a script...", 
            min_values=1, 
            max_values=1, 
            options=options, 
            custom_id="persistent_jjs_dropdown" 
        )

    async def callback(self, interaction: discord.Interaction):
        # Logic to determine which message to send based on the choice
        if self.values[0] == "sedse_jjs":
            response_text = "Here is the **Sedse JJS Script**!:\n`loadstring(game:HttpGet(\"https://raw.githubusercontent.com/SedseXD/sedsejjs/refs/heads/main/sedse's%20scripts\"))()`"
        
        elif self.values[0] == "jjs_piano":
            response_text = "Here is the information and link for **JJS Piano**!:\n `loadstring(game:HttpGet('https://raw.githubusercontent.com/SedseXD/piano/refs/heads/main/pianoscript.lua'))()`"
        
        elif self.values[0] == "jjs_piano_os":
            response_text = "Here is the GitHub link and info for **JJS Piano Open Source**!: https://raw.githubusercontent.com/SedseXD/piano/refs/heads/main/pianoscript.lua"

        # ephemeral=True means only the person who clicked it sees the response
        await interaction.response.send_message(response_text, ephemeral=True)

class JJSView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None) # timeout=None makes the menu work even after bot restarts
        self.add_item(JJSDropdown())

# ==========================================
# 2. BOT CONFIGURATION
# ==========================================

intents = discord.Intents.default()
intents.message_content = True # Required for the !sync command to work

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    # This ensures the dropdown menu continues to work after the bot restarts
    bot.add_view(JJSView())
    print(f'Logged in successfully as {bot.user}')
    print("-" * 30)
    print("BOT STATUS: Online")
    print("ACTION REQUIRED: Type !sync in your Discord server to activate /script")
    print("-" * 30)

# ==========================================
# 3. COMMANDS
# ==========================================

# --- SLASH COMMAND ---
# This is the /script command
@bot.tree.command(name="script", description="Open the script selection menu")
async def script(interaction: discord.Interaction):
    await interaction.response.send_message("Please select a script from below:", view=JJSView(), ephemeral=True)

# --- SYNC COMMAND ---
# This is a hidden prefix command. 
# Type !sync in your server to force Discord to load the /script command.
@bot.command()
async def sync(ctx):
    try:
        synced = await bot.tree.sync()
        await ctx.send(f"✅ Successfully synced {len(synced)} slash command(s)! You can now use `/script`.")
        print(f"Synced {len(synced)} commands.")
    except Exception as e:
        await ctx.send(f"❌ Sync failed: {e}")
        print(f"Error syncing: {e}")

# ==========================================
# 4. RUN BOT
# ==========================================

# This gets the token from your Railway environment variables
TOKEN = os.getenv("DISCORD_TOKEN")

if TOKEN:
    bot.run(TOKEN)
else:
    print("ERROR: No DISCORD_TOKEN found in environment variables!")
