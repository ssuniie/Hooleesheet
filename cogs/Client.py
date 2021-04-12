import discord
from discord.ext import commands

import os

CLIENT_NAME = os.environ['CLIENT_NAME']


class Client(commands.Cog):
    def __init__(self, client):
        self.client = client

    # When client is online.
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{CLIENT_NAME} on duty!')

        await self.client.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.listening,
                name='ah help'
            )
        )

    # When client is joins the server.
    @ commands.Cog.listener()
    async def on_guild_join(self, guild):
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                embed = discord.Embed(
                    title=f'{CLIENT_NAME} on duty!',
                    description=(
                        'ขอบพระทัยที่รับน้อนมาเลี้ยงนะงับ :pray:\n'
                        + 'เริ่มต้นใช้งานด้วยการพิมพ์ ah help นะงับ'
                    ),
                    color=0xf77eff
                )
                await channel.send(embed=embed)
            break


def setup(client):
    client.add_cog(Client(client))
