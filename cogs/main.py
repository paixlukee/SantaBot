import discord
from discord.ext import commands
from datetime import datetime
import requests
import random
import math
import time
import schedule
import randomimg
import randomsong
from discord.ext.commands import errors, converter
from random import randint
from random import choice as rnd
import aiohttp
import asyncio
import json
import os
import config
from pymongo import MongoClient
import pymongo

client = MongoClient(config.mongo_client)
db = client['siri']


class Main(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    def task():
        futuredate = datetime.strptime('Dec 25 2019  0:00', '%b %d %Y %H:%M')
        nowdate = datetime.now()
        count = int((futuredate-nowdate).total_seconds())
        days = round(count/86400)
        posts = db.utility.find_one({"utility": "santaconf"})
        for x in posts['channel']:
            channel = bot.get_channel(int(x))
            embed = discord.Embed(colour=0x9c0101, description=f"There are currently **{days}** until Christmas!")
            if x in posts['images']:
                embed.set_image(url=rnd(randomimg.imgs))
            else: 
                pass
            #await channel.send(embed=embed)

    schedule.every().day.at("04:17").do(task)

    while True:
        schedule.run_pending()
        time.sleep(1)

    @commands.command(aliases=['countdown', 'christmascountdown'])
    async def cc(self, ctx):
        futuredate = datetime.strptime('Dec 25 2019  0:00', '%b %d %Y %H:%M')
        nowdate = datetime.now()
        count = int((futuredate-nowdate).total_seconds())
        days = count//86400
        hours = (count-days*86400)//3600
        minutes = (count-days*86400-hours*3600)//60
        seconds = count-days*86400-hours*3600-minutes*60
        embed = discord.Embed(colour=0x9c0101, description=f"There are...\n**{days}** days\n**{hours}** hours\n**{minutes}** minutes\n**{seconds}** seconds\n... until Christmas!")
        embed.set_author(icon_url=ctx.me.avatar_url_as(format='png'), name="Countdown to Christmas")
        await ctx.send(embed=embed)

    @commands.command()
    async def heartbeats(self, ctx):
        futuredate = datetime.strptime('Dec 25 2019  0:00', '%b %d %Y %H:%M')
        nowdate = datetime.now()
        count = int((futuredate-nowdate).total_seconds())
        heartbeats = count//60*80
        fm = format(heartbeats, ",d")
        embed = discord.Embed(colour=0x9c0101, description=f"Your heart will beat around **{fm}** times until Christmas!")
        embed.set_author(icon_url=ctx.me.avatar_url_as(format='png'), name="Countdown to Christmas")
        await ctx.send(embed=embed)

    @commands.command()
    async def image(self, ctx):
        r = rnd(randomimg.imgs)
        embed = discord.Embed(colour=0x9c0101)
        embed.set_author(icon_url=ctx.me.avatar_url_as(format='png'), name="Santa")
        embed.set_image(url=r)
        await ctx.send(embed=embed)

    @commands.command()
    async def song(self, ctx):
        r = rnd(randomsong.songs)
        embed = discord.Embed(colour=0x9c0101, description=f":musical_note: I'm listening to {r}! :musical_note:")
        await ctx.send(embed=embed)

    @commands.command()
    async def setcc(self, ctx):
        if ctx.author.guild_permissions.manage_guild or ctx.author.guild_permissions.manage_channels:
            user = db.utility.find_one({"utility": "santaconf"})
            def check(m):
                return m.author == ctx.message.author
            embed = discord.Embed(colour=0x9c0101, description="Hello, and thank you for using **Santa**.\n\n Which channel would you like the countdown to be in? Reply to this message with the [channel tag](https://i.imgur.com/AtgvL36.gif) within **1 minute**. To cancel setup, reply with **cancel**.")
            await ctx.send(embed=embed)
            ch = await self.bot.wait_for('message', check=check, timeout=60)
            if ch.content.lower() == 'cancel':
                await ctx.send("Setup canceled.")
            else:
                try:
                    chnlcheck = ch.content.replace("<#", "").replace(">","")
                    channel = ctx.guild.get_channel(chnlcheck).id
                    db.utility.update_one({"utility": "santaconf"}, {"$push":{"channels": channel}})
                    embed = discord.Embed(colour=0x9c0101, description="Nice! Would you like to have random images added to the daily countdown message? Only reply with **yes** or **no**.\n\nExample:")
                    embed.set_image(url="https://i.imgur.com/WAAaAf5.png")
                    await ctx.send(embed=embed)
                    an = await self.bot.wait_for('message', check=check, timeout=60)
                    if an.content.lower() == 'yes':
                        db.utility.update_one({"utility": "santaconf"}, {"$push":{"channels": channel}})
                        embed = discord.Embed(colour=0x9c0101, description="And... done! Setup has been completed and I will post a countdown message in that channel every day at 12:00 AM EST.\n\nTo remove this, do `&remcc`.")
                        embed.set_footer(icon_url=ctx.me.avatar_url_as(format='png'), text='Ho ho ho.')
                        await ctx.send(embed=embed)
                    elif an.content.lower() == 'no':
                        embed = discord.Embed(colour=0x9c0101, description="And... done! Setup has been completed and I will post a countdown message in that channel every day at 12:00 AM EST.\n\nTo remove this, do `&remcc`.")
                        embed.set_footer(icon_url=ctx.me.avatar_url_as(format='png'), text='Ho ho ho.')
                        await ctx.send(embed=embed)
                    else:
                        await ctx.send('Setup failed. Only respond with yes or no. Do `&setcc` to restart setup.')
                except:
                    await ctx.send("Setup failed. Only respond with the channel tag (https://i.imgur.com/AtgvL36.gif). Do `&setcc` to restart setup.")
        else:
            await ctx.send("You need `manage_server` or `manage_channels` to use this command.")

    @commands.command()
    async def remcc(self, ctx):
        if ctx.author.guild_permissions.manage_guild or ctx.author.guild_permissions.manage_channels:
            user = db.utility.find_one({"utility": "santaconf"})
            def check(m):
                return m.author == ctx.message.author
            embed = discord.Embed(colour=0x9c0101, description="Hello, and thank you for using **Santa**.\n\n Which channel would you like to remove? Reply to this message with the [channel tag](https://i.imgur.com/AtgvL36.gif) within **1 minute**. To cancel, reply with **cancel**.")
            await ctx.send(embed=embed)
            ch = await self.bot.wait_for('message', check=check, timeout=60)
            if ch.content.lower() == 'cancel':
                await ctx.send("Setup canceled.")
            else:
                try:
                    chnlcheck = ch.content.replace("<#", "").replace(">","")
                    channel = ctx.guild.get_channel(chnlcheck).id
                    db.utility.update_one({"utility": "santaconf"}, {"$push":{"channels": channel}})
                    embed = discord.Embed(colour=0x9c0101, description="Channel removed from Christmas Countdown reminders.")                 
                    await ctx.send(embed=embed)
                except:
                    await ctx.send("Setup failed. Only respond with the channel tag (https://i.imgur.com/AtgvL36.gif). Do `&setcc` to restart setup.")
        else:
            await ctx.send("You need `manage_server` or `manage_channels` to use this command.")


def setup(bot):
    bot.add_cog(Main(bot))
