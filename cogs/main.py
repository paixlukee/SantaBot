import discord
from discord.ext import commands
from datetime import datetime
import requests
import random
import math
import time
from discord.ext.commands import errors, converter
from random import choice, randint
from random import choice, randint as rnd
import aiohttp
import asyncio
import json
import os
import config
from pymongo import MongoClient
import pymongo


class Main:
    def __init__(self, bot):
        self.bot = bot

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
        await ctx.send(embed=cc)

    @commands.command()
    async def heartbeats(self, ctx):
        futuredate = datetime.strptime('Dec 25 2019  0:00', '%b %d %Y %H:%M')
        nowdate = datetime.now()
        count = int((futuredate-nowdate).total_seconds())
        heartbeats = count//60*80
        embed = discord.Embed(colour=0x9c0101, description=f"Your heart will beat around **{format(heartbeats, ",d")}** times until Christmas!")
        embed.set_author(icon_url=ctx.me.avatar_url_as(format='png'), name="Countdown to Christmas")
        await ctx.send(embed=cc)



def setup(bot):
    bot.add_cog(Main(bot))
