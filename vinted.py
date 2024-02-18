import os
import subprocess
import sys

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
            print(f"Module '{module}' n'est pas installé. Téléchargement en cours...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", module])
            print(f"Module '{module}' installé avec succès!")

install_missing_modules()

# Maintenant, vous pouvez importer vos modules en toute sécurité
import discord
from discord.ext import commands
import vinted_scraper
import asyncio
import colorama
from colorama import Fore
import fade


colorama.init()

TOKEN = os.getenv('DISCORD_TOKEN')  # Fetch token from environment variable
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))  # Fetch channel ID from environment variable

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
            items = scraper.search({"search_text": "board games"})

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
    embed.add_field(name="💲 **Prix**", value=f"**{item_info.price}€**", inline=False)

    # Add Size field
    embed.add_field(name="📏 **Taille**", value=f"**{item_info.size_title}**" if hasattr(item_info, 'size_title') else "Pas de donnée", inline=True)

    # Add Author field
    embed.add_field(name="👤 **Auteur**", value=f"**{item_info.username}**" if hasattr(item_info, 'username') else "Pas de donnée", inline=True)

    # Add State field
    embed.add_field(name="📦 **État**", value=f"**{item_info.condition}**" if hasattr(item_info, 'condition') else "Pas de donnée", inline=True)

    # Add Image with Link
    if hasattr(item_info, 'photos') and item_info.photos:
        embed.set_image(url=item_info.photos[0].thumbnails[0].url)  # Display the first thumbnail

    return embed

bot.run(TOKEN)
