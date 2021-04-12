import discord
from discord.ext import commands

import math
import asyncio
import random


class Mod(commands.Cog):
    def __init__(self, client):
        self.client = client

    # thanos command
    @commands.command()
    @commands.cooldown(1, 60 * 60, commands.BucketType.guild)
    async def thanos(self, ctx, time_in_second=None):
        if ctx.author is ctx.guild.owner:
            voice_channel = ctx.author.voice.channel
            total_unlucky_members = math.ceil(len(voice_channel.members) / 2)
            list_of_unlucky_members = []

            while total_unlucky_members != 0:
                u = random.choice(voice_channel.members)
                if u.bot:
                    continue
                if u is ctx.guild.owner:
                    await ctx.send('การสุ่มครั้งนี้ มีเจ้าของเซิฟอยู่ด้วย แต่เจ้าของเซิฟไม่เป็นไร')
                    continue

                if u not in list_of_unlucky_members:
                    list_of_unlucky_members.append(u)
                    total_unlucky_members -= 1
                    continue
                else:
                    print(f'{u} is already in unlucky member list')
                    pass

            unlucky_members_name = ''
            for user in list_of_unlucky_members:
                unlucky_members_name += f'{user.name} '

            embed = discord.Embed(
                title=f'สรุปบัญชีคนโดนดีดนิ้ว {total_unlucky_members} คน)',
                description=unlucky_members_name
            )

            if time_in_second is None:
                time_in_second = 20
                pass

            msg = await ctx.send('คนที่กำลังโดนดีดนิ้วในตอนนี้: ')
            for user in list_of_unlucky_members:
                await msg.edit(content=f'คนที่กำลังโดนดีดนิ้วในตอนนี้: {user.name}')
                await user.edit(mute=True, deafen=True)
                await asyncio.sleep(time_in_second)
                await user.edit(mute=False, deafen=False)

            await ctx.send(embed=embed)

    # detect cooldown error of thanos command
    @thanos.error
    async def command_name_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            m, s = divmod(int(error.retry_after), 60)
            await ctx.send(f'ช้าก่อนอานนท์! นายสามารถดีดนิ้วอีกรอบได้อีก {m} นาที {s} วินาที')

    # kick command
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reasons=None):
        await member.kick(reason=reasons)
        await member.send(
            f'คุณถูกเตะออกจาก {ctx.guild.name}'
            + f'เหตุผล: {reasons}'
        )


def setup(client):
    client.add_cog(Mod(client))
