import discord
from discord.ext import commands

import pytz
from hentai import Hentai, Format


class Hentai(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def doujin(self, ctx, doujin_id=None):
        doujin = Hentai(doujin_id)

        current_doujin_upload_date = doujin.upload_date
        new_timezone_upload_date = current_doujin_upload_date.astimezone(
            pytz.timezone('Asia/Bangkok'))

        embed = discord.Embed(title=f'{doujin.title(Format.Pretty)}')
        embed.set_author(
            name='nHentai',
            icon_url='https://i.kym-cdn.com/entries/icons/facebook/000/026/029/8P68F-_I_400x400.jpg'
        )
        embed.set_thumbnail(url=doujin.cover)
        embed.add_field(
            name='English Name :flag_gb:',
            value=doujin.title(Format.English),
            inline=False
        )
        embed.add_field(
            name='Japanese Name :flag_jp:',
            value=doujin.title(Format.Japanese),
            inline=False
        )
        for artist in doujin.artist:
            embed.add_field(
                name='Artist',
                value=f'[{artist.name}]({artist.url})'
            )
        embed.add_field(
            name='Upload Date',
            value=new_timezone_upload_date.strftime("%d/%m/%Y")
        )
        embed.add_field(
            name='URL',
            value=f'[{doujin.url}]({doujin.url})',
            inline=False
        )
        embed.set_footer(
            icon_url=ctx.author.avatar_url,
            text=f'Requested by {ctx.author}'
        )
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Hentai(client))
