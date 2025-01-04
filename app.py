import nextcord
import asyncio
from nextcord.ext import commands
import os
import sys

ascii_art = r"""

     __  __     ______     __  __        ______   ______     __   __     ______     __        
    /\ \_\ \   /\  __ \   /\_\_\_\      /\  == \ /\  __ \   /\ "-.\ \   /\  ___\   /\ \       
    \ \  __ \  \ \  __ \  \/_/\_\/_     \ \  _-/ \ \  __ \  \ \ \-.  \  \ \  __\   \ \ \____  
     \ \_\ \_\  \ \_\ \_\   /\_\/\_\     \ \_\    \ \_\ \_\  \ \_\\"\_\  \ \_____\  \ \_____\ 
      \/_/\/_/   \/_/\/_/   \/_/\/_/      \/_/     \/_/\/_/   \/_/ \/_/   \/_____/   \/_____/ 
                                                                                          
  
"""

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def center_text(text):
    terminal_width = os.get_terminal_size().columns
    return text.center(terminal_width)

def center_ascii_art(ascii_art):
    lines = ascii_art.split("\n")
    return "\n".join([center_text(line) for line in lines])

def display_menu():
    clear_screen()
    # Apply lime color to ASCII art
    print(f"\033[1;32m{center_ascii_art(ascii_art)}\033[0m")
    print(center_text("\n\n"))
    print(f"\033[1;32m{center_text('1. List servers the bot is in.')}\033[0m")
    print(f"\033[1;32m{center_text('2. Exit.')}\033[0m\n")
    print(f"\033[31m{center_text('---------------------------------------------------------------------------')}\033[0m")
    print(center_text(""))

async def main_menu():
    while True:
        display_menu()
        print(f"\033[1;36m{center_text(f'Logged in as: {bot.user}')}\033[0m")
        print(f"\033[1;36m{center_text(f'Bot is in {len(bot.guilds)} servers.')}\033[0m")
        
        sys.stdout.write(f"\033[1;36m> \033[0m")
        sys.stdout.flush()
        
        choice = input()
        
        if choice == "":
            continue

        if choice == "1":
            await list_servers()
        elif choice == "2":
            print(f"\033[1;36m{center_text('Exiting...')}\033[0m")
            await bot.close()
            break
        else:
            print(f"\033[1;36m{center_text('Invalid choice. Please try again.')}\033[0m")

async def list_servers():
    clear_screen()
    print(f"\n\033[1;36m{center_text('Servers the bot is in:')}\033[0m")
    for i, guild in enumerate(bot.guilds):
        print(center_text(f"{i + 1}. {guild.name}"))

    try:
        server_number = int(input(f"\033[1;36m{center_text('Enter the number of the server to leave (or 0 to cancel): ')}\033[0m"))
        if server_number == 0:
            print(f"\033[1;36m{center_text('Action cancelled.')}\033[0m")
            return

        selected_guild = bot.guilds[server_number - 1]
        confirm = input(f"\033[1;36m{center_text(f'Are you sure you want the bot to leave {selected_guild.name}? (yes/no): ')}\033[0m").lower()

        if confirm == "yes":
            await selected_guild.leave()
            print(f"\033[1;36m{center_text(f'The bot has left {selected_guild.name}.')}\033[0m")
        else:
            print(f"\033[1;36m{center_text('Action cancelled.')}\033[0m")

    except (ValueError, IndexError):
        print(f"\033[1;36m{center_text('Invalid input. Please try again.')}\033[0m")

intents = nextcord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    clear_screen()
    await main_menu()

with open("token.txt", "r") as token_file:
    bot_token = token_file.read().strip()

bot.run(bot_token)
