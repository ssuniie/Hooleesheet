import discord
from discord.ext import commands
import praw
import random

from datetime import datetime
import os
import json

CLIENT_NAME = os.environ['CLIENT_NAME']
reddit = praw.Reddit(
    client_id=os.environ['REDDIT_CLIENT_ID'],
    client_secret=os.environ['REDDIT_CLIENT_SECRET'],
    username=os.environ['REDDIT_USERNAME'],
    password=os.environ['REDDIT_PASSWORD'],
    user_agent=os.environ['CLIENT_NAME'],
    check_for_async=False
)


class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    # dick command
    @commands.command(aliases=['penis'])
    async def dick(self, ctx):
        size_random = random.randint(1, 10)
        await ctx.send(f"{ctx.author.name}'s dick size is 8"+'='*size_random+'D')

    # magicball command
    @commands.command()
    async def magicball(self, ctx, *, question=None):
        if question is None:
            await ctx.send('อย่าลืมใส่คำถามด้วยหล่ะนะ!')
        else:
            with open('assets/json/magicball.json', encoding='utf-8') as f:
                all_answer = json.load(f)

            answer = random.choice(all_answer)

            embed = discord.Embed(
                title='ลูกแก้ววิเศษ',
                description=f'ลูกแก้ววิเศษนี้จะตอบคำถามให้ {ctx.author.name} เอง',
                color=0xf77eff
            )
            embed.add_field(
                name='คำถาม ที่เจ้าถามมา?',
                value=question
            )
            embed.add_field(
                name='คำตอบจากข้า',
                value=answer, inline=False
            )
            embed.timestamp = datetime.utcnow()

            await ctx.send(embed=embed)

    # meme command
    @commands.command(aliases=['memes'])
    async def meme(self, ctx):
        global submission
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


def setup(client):
    client.add_cog(Fun(client))
