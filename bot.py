import discord
from discord.ext import commands

import praw
import os

# ! Intents Setting
intents = discord.Intents.all()

# * Client Infomations
client = commands.Bot(
    command_prefix='ah ',
    intents=intents,
    case_insensitive=True
)
CLIENT_NAME = os.environ['CLIENT_NAME']
TOKEN = os.environ['CLIENT_TOKEN']

# * remove commands from client.
client.remove_command('help')


# ! Load all Cogs file
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


# ! run the client / Required TOKEN
client.run(TOKEN)
