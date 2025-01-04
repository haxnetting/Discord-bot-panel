import nextcord
import asyncio
from nextcord.ext import commands
import os
import sys
import re

ascii_art = r"""

     __  __     ______     __  __        ______   ______     __   __     ______     __        
    /\ \_\ \   /\  __ \   /\_\_\_\      /\  == \ /\  __ \   /\ "-.\ \   /\  ___\   /\ \       
    \ \  __ \  \ \  __ \  \/_/\_\/_     \ \  _-/ \ \  __ \  \ \ \-.  \  \ \  __\   \ \ \____  
     \ \_\ \_\  \ \_\ \_\   /\_\/\_\     \ \_\    \ \_\ \_\  \ \_\\"\_\  \ \_____\  \ \_____\ 
      \/_/\/_/   \/_/\/_/   \/_/\/_/      \/_/     \/_/\/_/   \/_/ \/_/   \/_____/   \/_____/ 
                            Made by: @haxmc (Thanks for using <3)                                                   
  
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
    print(f"\033[1;32m{center_ascii_art(ascii_art)}\033[0m")
    print(center_text("\n\n"))
    print(f"\033[1;32m{center_text('1. List servers the bot is in.')}\033[0m")
    print(f"\033[1;32m{center_text('2. Get an invite link to a server.')}\033[0m")
    print(f"\033[1;32m{center_text('3. Purge all servers except whitelisted ones.')}\033[0m")
    print(f"\033[1;32m{center_text('4. Whitelist a server.')}\033[0m")
    print(f"\033[1;32m{center_text('5. Remove a server from whitelist.')}\033[0m")
    print(f"\033[1;32m{center_text('6. Create a role in a server.')}\033[0m")
    print(f"\033[1;32m{center_text('7. Refresh the data.')}\033[0m")
    print(f"\033[1;32m{center_text('8. Exit.')}\033[0m\n")
    print(f"\033[31m{center_text('---------------------------------------------------------------------------')}\033[0m")
    print(center_text(""))

async def refresh_data():
    clear_screen()
    print(f"\033[1;36m{center_text('Refreshing data...')}\033[0m")
    await bot.change_presence(activity=nextcord.Game(name="Refreshing..."))
    guilds = [guild async for guild in bot.fetch_guilds()]
    print(f"\033[1;36m{center_text(f'Refreshed data: {len(guilds)} servers.')}\033[0m")
    await bot.change_presence(activity=None)

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
            await get_invite_link()
        elif choice == "3":
            await purge_servers()
        elif choice == "4":
            await whitelist_server()
        elif choice == "5":
            await remove_from_whitelist()
        elif choice == "6":
            await create_role()
        elif choice == "7":
            await refresh_data()
        elif choice == "8":
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

async def whitelist_server():
    clear_screen()
    print(f"\n\033[1;36m{center_text('Servers the bot is in:')}\033[0m")
    for i, guild in enumerate(bot.guilds):
        print(center_text(f"{i + 1}. {guild.name}"))
    try:
        server_number = int(input(f"\033[1;36m{center_text('Enter the number of the server to whitelist (or 0 to cancel): ')}\033[0m"))
        if server_number == 0:
            print(f"\033[1;36m{center_text('Action cancelled.')}\033[0m")
            return
        selected_guild = bot.guilds[server_number - 1]
        confirm = input(f"\033[1;36m{center_text(f'Are you sure you want to whitelist {selected_guild.name}? (yes/no): ')}\033[0m").lower()
        if confirm == "yes":
            whitelisted_servers = load_whitelisted_servers()
            if any(guild_id == selected_guild.id for guild_id, _ in whitelisted_servers):
                print(f"\033[1;36m{center_text(f'{selected_guild.name} is already whitelisted.')}\033[0m")
                return
            sanitized_name = re.sub(r'[^a-zA-Z0-9 ]', '', selected_guild.name)
            with open("whitelisted_servers.txt", "a") as whitelist_file:
                whitelist_file.write(f"{selected_guild.id} - {sanitized_name}\n")
            print(f"\033[1;36m{center_text(f'{selected_guild.name} has been whitelisted.')}\033[0m")
        else:
            print(f"\033[1;36m{center_text('Action cancelled.')}\033[0m")
    except (ValueError, IndexError):
        print(f"\033[1;36m{center_text('Invalid input. Please try again.')}\033[0m")
        
async def remove_from_whitelist():
    clear_screen()
    print(f"\n\033[1;36m{center_text('Whitelisted servers:')}\033[0m")
    whitelisted_servers = load_whitelisted_servers()
    if not whitelisted_servers:
        print(f"\033[1;36m{center_text('No whitelisted servers.')}\033[0m")
        return
    for i, (guild_id, guild_name) in enumerate(whitelisted_servers):
        print(center_text(f"{i + 1}. {guild_name}"))
    try:
        server_number = int(input(f"\033[1;36m{center_text('Enter the number of the server to remove from whitelist (or 0 to cancel): ')}\033[0m"))
        if server_number == 0:
            print(f"\033[1;36m{center_text('Action cancelled.')}\033[0m")
            return
        selected_guild = whitelisted_servers[server_number - 1]
        confirm = input(f"\033[1;36m{center_text(f'Are you sure you want to remove {selected_guild[1]} from whitelist? (yes/no): ')}\033[0m").lower()
        if confirm == "yes":
            whitelisted_servers.remove(selected_guild)
            save_whitelisted_servers(whitelisted_servers)
            print(f"\033[1;36m{center_text(f'{selected_guild[1]} has been removed from whitelist.')}\033[0m")
        else:
            print(f"\033[1;36m{center_text('Action cancelled.')}\033[0m")
    except (ValueError, IndexError):
        print(f"\033[1;36m{center_text('Invalid input. Please try again.')}\033[0m")

def load_whitelisted_servers():
    whitelisted_servers = []
    if os.path.exists("whitelisted_servers.txt"):
        with open("whitelisted_servers.txt", "r") as whitelist_file:
            lines = whitelist_file.readlines()
            for line in lines:
                line = line.strip()
                if line and " - " in line:
                    guild_id, guild_name = line.split(" - ")
                    whitelisted_servers.append((int(guild_id), guild_name))
    return whitelisted_servers

def save_whitelisted_servers(whitelisted_servers):
    with open("whitelisted_servers.txt", "w") as whitelist_file:
        for guild_id, guild_name in whitelisted_servers:
            whitelist_file.write(f"{guild_id} - {guild_name}\n")

async def purge_servers():
    whitelisted_servers = load_whitelisted_servers()
    clear_screen()
    print(f"\n\033[1;36m{center_text('Purging servers, keeping whitelisted ones...')}\033[0m")
    for guild in bot.guilds:
        if not any(guild.id == whitelisted_id for whitelisted_id, _ in whitelisted_servers):
            await guild.leave()
            print(f"\033[1;36m{center_text(f'Left server: {guild.name}')}\033[0m")
        else:
            print(f"\033[1;36m{center_text(f'Keeping server: {guild.name}')}\033[0m")

async def create_role():
    clear_screen()
    print(f"\n\033[1;36m{center_text('Servers the bot is in:')}\033[0m")
    for i, guild in enumerate(bot.guilds):
        print(center_text(f"{i + 1}. {guild.name}"))
    try:
        server_number = int(input(f"\033[1;36m{center_text('Enter the number of the server to create role in: ')}\033[0m"))
        selected_guild = bot.guilds[server_number - 1]
        role_name = input(f"\033[1;36m{center_text('Enter the role name: ')}\033[0m")
        role_color = input(f"\033[1;36m{center_text('Enter the role color (hex format): ')}\033[0m")
        user_id = int(input(f"\033[1;36m{center_text('Enter the user ID to assign the role: ')}\033[0m"))
        
        role = await selected_guild.create_role(name=role_name, color=nextcord.Color(int(role_color, 16)), reason="Role creation via bot")
        member = selected_guild.get_member(user_id)
        if member:
            await member.add_roles(role)
            print(f"\033[1;36m{center_text(f'Role {role_name} created and assigned to user {member.name}.')}\033[0m")
        else:
            print(f"\033[1;36m{center_text('User not found in the server.')}\033[0m")
    except (ValueError, IndexError):
        print(f"\033[1;36m{center_text('Invalid input. Please try again.')}\033[0m")

intents = nextcord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    clear_screen()
    print(f"\033[1;36m{center_text(f'Logged in as: {bot.user}')}\033[0m")
    await main_menu()

with open("token.txt", "r") as token_file:
    bot_token = token_file.read().strip()

bot.run(bot_token)
