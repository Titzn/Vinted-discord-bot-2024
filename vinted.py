import os
import subprocess
import sys
import json

required_modules = [
    'discord',
    'vinted_scraper',
    'asyncio',
    'colorama',
    'fade'
]

def install_missing_modules():
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            print(f"Module '{module}' is not installed. Installing...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", module])
            print(f"Module '{module}' installed successfully!")

install_missing_modules()

# Now, you can safely import your modules
import discord
from discord.ext import commands
import vinted_scraper
import asyncio
import colorama
from colorama import Fore
import fade

colorama.init()

TOKEN = ""
CHANNEL_ID = ""
PRICE_RANGE = ""
ITEM_TYPE = ""

config_file = "config.json"

def load_or_create_config():
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            return json.load(f)
    else:
        config = {}
        config['TOKEN'] = input("Enter your Discord token: ")
        config['CHANNEL_ID'] = int(input("Enter your channel ID: "))
        config['PRICE_RANGE'] = input("Enter your price range (format: min€-max€): ")
        config['ITEM_TYPE'] = input("Enter the type of item you want to search for: ")
        with open(config_file, 'w') as f:
            json.dump(config, f)
        return config

config = load_or_create_config()
TOKEN = config['TOKEN']
CHANNEL_ID = config['CHANNEL_ID']
PRICE_RANGE = config['PRICE_RANGE']
ITEM_TYPE = config['ITEM_TYPE']

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
scraper = vinted_scraper.VintedScraper("https://www.vinted.com")
faded_text = fade.greenblue("""
  _______ _ _                      _       _           _   _           _   
 |__   __(_) |                    (_)     | |         | | | |         | |  
    | |   _| |_ __ _ _ __   __   ___ _ __ | |_ ___  __| | | |__   ___ | |_ 
    | |  | | __/ _` | '_ \  \ \ / / | '_ \| __/ _ \/ _` | | '_ \ / _ \| __|
    | |  | | || (_| | | | |  \ V /| | | | | ||  __/ (_| | | |_) | (_) | |_ 
    |_|  |_|\__\__,_|_| |_|   \_/ |_|_| |_|\__\___|\__,_| |_.__/ \___/ \__|                                                                          
                                                                                                                                                                                                                                             
                                   [+]Github: https://github.com/Titzn/
                                   [+]Discord: titzn
    """)

# Embed Colors
EMBED_COLOR = discord.Colour.blue()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await search_vinted()

async def search_vinted():
    while not bot.is_closed():
        try:
            items = scraper.search({"search_text": ITEM_TYPE})

            if items:
                for item in items:
                    item_info = scraper.item(item.id)
                    embed = create_embed(item_info)
                    channel = bot.get_channel(CHANNEL_ID)
                    await channel.send(embed=embed)
                    await asyncio.sleep(1)  # Pause for 1 second

            await asyncio.sleep(300)
        except Exception as e:
            print(f"An error occurred: {e}")

def create_embed(item_info):
    embed = discord.Embed(
        title=f"**{item_info.title}**",
        description=f"[{item_info.url}]",
        color=EMBED_COLOR
    )

    # Add Price field
    embed.add_field(name="💲 **Price**", value=f"**{item_info.price}€**", inline=False)

    # Add Size field
    embed.add_field(name="📏 **Size**", value=f"**{item_info.size_title}**" if hasattr(item_info, 'size_title') else "No data", inline=True)

    # Add Author field
    embed.add_field(name="👤 **Author**", value=f"**{item_info.username}**" if hasattr(item_info, 'username') else "No data", inline=True)

    # Add State field
    embed.add_field(name="📦 **Condition**", value=f"**{item_info.condition}**" if hasattr(item_info, 'condition') else "No data", inline=True)

    # Add Image with Link
    if hasattr(item_info, 'photos') and item_info.photos:
        embed.set_image(url=item_info.photos[0].thumbnails[0].url)  # Display the first thumbnail

    return embed

bot.run(TOKEN)
