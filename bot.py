import discord
import os
from discord.ext import commands
from discord import app_commands

# ==========================================
# 1. DROPDOWN MENU SETUP
# ==========================================

class JJSDropdown(discord.ui.Select):
    def __init__(self):
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
        if self.values[0] == "sedse_jjs":
            response_text = "Here is the **Sedse JJS Script**!:\n`loadstring(game:HttpGet(\"https://raw.githubusercontent.com/SedseXD/sedsejjs/refs/heads/main/sedse's%20scripts\"))()`"
        elif self.values[0] == "jjs_piano":
            response_text = "Here is the information and link for **JJS Piano**!:\n `loadstring(game:HttpGet('https://raw.githubusercontent.com/SedseXD/piano/refs/heads/main/pianoscript.lua'))()`"
        elif self.values[0] == "jjs_piano_os":
            response_text = "Here is the GitHub link and info for **JJS Piano Open Source**!: https://raw.githubusercontent.com/SedseXD/piano/refs/heads/main/pianoscript.lua"

        await interaction.response.send_message(response_text, ephemeral=True)

class JJSView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(JJSDropdown())

# ==========================================
# 2. BOT CLASS (For Auto-Sync)
# ==========================================

class MyBot(commands.Bot):
    def __init__(self):
        # We keep the prefix just in case, but the focus is on slash commands
        intents = discord.Intents.default()
        intents.message_content = True 
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # 1. Make the dropdown menu persistent
        self.add_view(JJSView())
        
        # 2. Automatically sync slash commands to Discord
        print("Syncing slash commands... please wait.")
        try:
            synced = await self.tree.sync()
            print(f"✅ Successfully synced {len(synced)} slash command(s)!")
        except Exception as e:
            print(f"❌ Sync failed: {e}")

bot = MyBot()

# ==========================================
# 3. COMMANDS
# ==========================================

@bot.tree.command(name="script", description="Open the script selection menu")
async def script(interaction: discord.Interaction):
    await interaction.response.send_message("Please select a script from below:", view=JJSView(), ephemeral=True)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    print("The bot is now online. If you have the 'applications.commands' scope, /script will appear shortly.")

# ==========================================
# 4. RUN
# ==========================================

TOKEN = os.getenv("DISCORD_TOKEN")
if TOKEN:
    bot.run(TOKEN)
else:
    print("ERROR: No DISCORD_TOKEN found!")
