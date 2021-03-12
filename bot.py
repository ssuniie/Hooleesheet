import discord
from discord.ext import commands

import datetime
from datetime import datetime

import json
import random
import praw
import os

# ! Intents Setting
intents = discord.Intents.all()

# * Client Infomations
client = commands.Bot(
    command_prefix='ah ',
    intents=intents
)
TOKEN = os.environ['CLIENT_TOKEN']
CLIENT_NAME = 'Aki Hanako'
reddit = praw.Reddit(
    client_id=os.environ['REDDIT_CLIENT_ID'],
    client_secret=os.environ['REDDIT_CLIENT_SECRET'],
    username=os.environ['REDDIT_USERNAME'],
    password=os.environ['REDDIT_PASSWORD'],
    user_agent=CLIENT_NAME,
    check_for_async=False
)

# * remove commands from client.
client.remove_command('help')


# * When client is online.
@client.event
async def on_ready():
    print(f'{CLIENT_NAME} on duty!')
    await client.change_presence(activity=discord.Game(name='ah help'))


# * When client is join.
@client.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            embed = discord.Embed(
                title=f'{CLIENT_NAME} on duty!',
                description=(
                    'ขอบพระทัยที่รับน้อนมาเลี้ยงนะงับ :pray:\n'
                    + 'เริ่มต้นใช้งานด้วยการพิมพ์ ah help นะงับ'
                ),
                color=0x6549DA
            )
            await channel.send(embed=embed)
        break


# * When users use help command (m!help)
@client.command()
async def help(ctx, arg=None):
    if arg == None:
        embed = discord.Embed(
            title='คำสั่งของน้อนทั้งหมด',
            color=0x6549DA)
        embed.add_field(name='help', value='`ah help`')
        embed.add_field(name='fun', value='`ah help fun`')
        embed.add_field(name='help', value='`ah help`')

    await ctx.send(embed=embed)


@client.command()
async def dick(ctx):
    size_random = random.randint(1, 10)
    await ctx.send(f"{ctx.author.name}'s dick size is 8"+'='*size_random+'D')


@client.command()
async def meme(ctx):
    memes_submissions = reddit.subreddit('memes').hot()
    post_to_pick = random.randint(1, 100)
    for i in range(0, post_to_pick):
        submission = next(x for x in memes_submissions if not x.stickied)

    embed = discord.Embed(
        title=submission.title
    )
    embed.set_image(url=submission.url)
    embed.timestamp = datetime.utcnow()
    embed.set_footer(text='r/meme')

    await ctx.send(embed=embed)


# ! run the client / Required TOKEN
client.run(TOKEN)
