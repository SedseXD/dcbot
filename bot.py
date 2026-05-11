import discord
import os
from discord.ext import commands
from discord import app_commands # Necessary for slash commands

class JJSDropdown(discord.ui.Select):
    def __init__(self):
        options =[
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
            placeholder="Choose an option...", 
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
        super().__init__(timeout=None) # timeout=None makes the dropdown work even after bot restarts
        self.add_item(JJSDropdown())

# Setup Intents
intents = discord.Intents.default()
intents.message_content = True

# We define the bot class to handle the syncing of slash commands easily
class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # This registers the View so the dropdown keeps working after a bot restart
        self.add_view(JJSView())
        # This syncs the slash commands to Discord
        await self.tree.sync() 
        print("Slash commands synced!")

bot = MyBot()

# --- SLASH COMMAND ---
@bot.tree.command(name="script", description="Show the script selection menu")
async def script(interaction: discord.Interaction):
    """This replaces the !menu command with /script"""
    await interaction.response.send_message("Please select a script from below:", view=JJSView(), ephemeral=True)

@bot.event
async def on_ready():
    print(f'Logged in successfully as {bot.user}')

# --- RUN THE BOT ---
bot.run(os.getenv("DISCORD_TOKEN"))
