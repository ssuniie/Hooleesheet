import discord
from discord.ext import commands

import math
import asyncio
import random


class Mod(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def thanos_execute(self, ctx, voice_channel, total_unlucky_members, time_in_second):
        print('Thanos Executed!')
        # create list and string of unlucky_members to store names and attributes
        list_of_unlucky_members = []
        unlucky_members_name = ''

        # command execute here!
        while total_unlucky_members != 0:
            # u = some random unlucky guys
            u = random.choice(voice_channel.members)

            # command will not add bot and ctx.guild.owner to list
            if u.bot:
                continue
            # if u is ctx.guild.owner:
            #     await ctx.send('การสุ่มครั้งนี้ มีเจ้าของเซิฟอยู่ด้วย แต่เจ้าของเซิฟไม่เป็นไร')
            #     continue

            # this if statement create for
            # to prevent duplicate users in list
            if u not in list_of_unlucky_members:
                list_of_unlucky_members.append(u)
                unlucky_members_name += f'{u.name} '
                total_unlucky_members -= 1

                print(f'{u} added to the list')
                continue
            else:
                print(f'{u} is already in unlucky member list')
                pass

        # message of total unlucky members
        embed = discord.Embed(
            title=f'สรุปบัญชีคนโดนดีดนิ้ว',
            description=f'ระยะเวลา: {time_in_second} วินาที\n'
            + f'จำนวนที่โดนผลจากการดีดนิ้วทั้งหมด: {total_unlucky_members} คน'

        )
        embed.add_field(
            name='ผู้โชคร้ายทั้งหมด',
            value=total_unlucky_members
        )

        # message thats show who is getting execute right now!
        msg = await ctx.send('คนที่กำลังโดนผลจากการดีดนิ้วในครั้งนี้: ')

        # mute every lucky members
        for user in list_of_unlucky_members:
            await msg.edit(content=f'คนที่กำลังโดนผลจากการดีดนิ้วในครั้งนี้: {user.name}')
            await user.edit(mute=True, deafen=True)

        # send summary message
        await ctx.send(embed=embed)

        # countdown starts here!
        await asyncio.sleep(time_in_second)

        # unmute every unlucky members
        for user in list_of_unlucky_members:
            await user.edit(mute=False, deafen=False)

    # Thanos Command
    @commands.command()
    @commands.cooldown(1, 60 * 60, commands.BucketType.guild)
    async def thanos(self, ctx, time_in_second=None):
        # command will execute if ctx.author is ctx.guild.owner
        if ctx.author is ctx.guild.owner:
            # get voice channel from guild.owner
            voice_channel = ctx.author.voice.channel

            # get amount of unlucky_members in total
            # unlucky_members will be half of voice channel in total users
            total_unlucky_members = math.ceil(len(voice_channel.members) / 2)

            # define the final time (default is 20 seconds, maximum is 120 seconds)
            if time_in_second is None:
                time_in_second = 20
                pass
            elif time_in_second > 120:
                time_in_second = 120
                pass

            task = await asyncio.create_task(thanos_execute(ctx, voice_channel, total_unlucky_members, time_in_second))
            await asyncio.run(task)

    # detect cooldown error of thanos command
    @thanos.error
    async def command_name_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            m, s = divmod(int(error.retry_after), 60)
            await ctx.send(f'ช้าก่อนอานนท์! นายสามารถดีดนิ้วอีกรอบได้อีก {m} นาที {s} วินาที')

    # Kick Command
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reasons=None):
        await member.kick(reason=reasons)
        await member.send(
            f'คุณถูกเตะออกจาก {ctx.guild.name}'
            + f'เหตุผล: {reasons}'
        )

    # Ban Command
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reasons=None):
        await member.ban(reason=reasons)
        await member.send(
            f'คุณถูกแบนออกจาก {ctx.guild.name}'
            + f'เหตุผล: {reasons}'
        )

    # Unban Command
    @commands.command()
    async def unban(self, ctx, *, user):
        banned_users = await ctx.guild.bans()
        user_name, user_tagid = user.split('#')

        for ban_entry in banned_users:
            user = ban_entry.users

            if (user.name, user.discriminator) == (user_name, user_tagid):
                await ctx.guild.unban(user)
                await ctx.send(f'{ctx.author.mention} ได้ปลดแบน {user.name}#{user.discriminator} เรียบร้อยแล้ว!')


def setup(client):
    client.add_cog(Mod(client))
