import discord
from discord.ext import commands
import vinted_scraper
import asyncio
import colorama
from colorama import *

colorama.init()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
scraper = vinted_scraper.VintedScraper("https://www.vinted.com")
print(Fore.RED + """
      
   
  _______ _ _                      _       _           _   _           _   
 |__   __(_) |                    (_)     | |         | | | |         | |  
    | |   _| |_ __ _ _ __   __   ___ _ __ | |_ ___  __| | | |__   ___ | |_ 
    | |  | | __/ _` | '_ \  \ \ / / | '_ \| __/ _ \/ _` | | '_ \ / _ \| __|
    | |  | | || (_| | | | |  \ V /| | | | | ||  __/ (_| | | |_) | (_) | |_ 
    |_|  |_|\__\__,_|_| |_|   \_/ |_|_| |_|\__\___|\__,_| |_.__/ \___/ \__|
                                                                           
                                                                           
   
      """ + Fore.RESET)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await search_vinted()

async def search_vinted():
    await bot.wait_until_ready()
    while not bot.is_closed():
        items = scraper.search({"search_text": "board games"})
        
        if items:
            for item in items:
                item_info = scraper.item(item.id)
                embed = create_embed(item_info)
                channel = bot.get_channel()  # Remplacez par l'ID de votre canal Discord (int)
                await channel.send(embed=embed)

        await asyncio.sleep(300)

def create_embed(item_info):
    embed = discord.Embed(
        title=f"**{item_info.title}**",
        description=f"[Voir l'article sur Vinted]({item_info.url})",
        color=0x3498db
    )

    embed.add_field(name="💲 Prix", value=f"{item_info.price}€", inline=True)
    embed.add_field(name="📏 Taille", value=item_info.size_title if hasattr(item_info, 'size_title') else "Pas de donnée", inline=True)
    embed.add_field(name="🏷️ Marque", value=item_info.brand_title if hasattr(item_info, 'brand_title') else "Pas de donnée", inline=True)
    embed.add_field(name="👍👎 Avis", value=f"{item_info.positive} 👍 / {item_info.negative} 👎" if hasattr(item_info, 'positive') and hasattr(item_info, 'negative') else "Pas de donnée", inline=True)
    embed.add_field(name="🌍 Localisation", value=f"{item_info.country_title}, {item_info.city}" if hasattr(item_info, 'country_title') and hasattr(item_info, 'city') else "Pas de donnée", inline=True)
    embed.add_field(name="👤 Vendeur", value=item_info.username if hasattr(item_info, 'username') else "Pas de donnée", inline=True)
    
    # Ajouter jusqu'à 4 images
    if hasattr(item_info, 'photo') and hasattr(item_info.photo, 'thumbnails') and item_info.photo.thumbnails:
        for i, thumbnail in enumerate(item_info.photo.thumbnails[:4]):  # Limiter à 4 images
            embed.set_image(url=thumbnail.url)

    return embed

bot.run('')
